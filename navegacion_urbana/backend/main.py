import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.graph_loader import load_city_graph, graph_to_adjacency, get_osm_node
from src.dijkstra import dijkstra, reconstruct_path
from src.astar import astar

app = FastAPI(title="Navegación Urbana API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

G = None
adj = None
coords = None
graph_loaded = False


class RouteRequest(BaseModel):
    origin_lat: float
    origin_lon: float
    dest_lat: float
    dest_lon: float


class NodeInfo(BaseModel):
    lat: float
    lon: float


@app.on_event("startup")
async def startup():
    global G, adj, coords, graph_loaded
    city = os.getenv("CITY", "Miraflores, Lima, Peru")
    G = load_city_graph(city=city, network_type="drive")
    adj, coords = graph_to_adjacency(G)
    graph_loaded = True
    print(f"API lista — {len(adj)} nodos, {sum(len(v) for v in adj.values())} aristas")


@app.get("/api/graph-info")
def graph_info():
    if not graph_loaded:
        return {"status": "loading"}
    return {
        "status": "ready",
        "nodes": len(adj),
        "edges": sum(len(v) for v in adj.values()),
        "coords": {str(k): {"lat": v[0], "lon": v[1]} for k, v in list(coords.items())[:2]},
    }


@app.post("/api/route")
def find_route(req: RouteRequest):
    if not graph_loaded:
        return {"error": "Graph not loaded yet"}

    source = get_osm_node(G, req.origin_lat, req.origin_lon)
    target = get_osm_node(G, req.dest_lat, req.dest_lon)

    if source not in adj or target not in adj:
        return {"error": "Coordinates not in graph"}

    t0 = time.perf_counter()
    dist_d, prev_d, nodes_d = dijkstra(adj, source, target)
    t1 = time.perf_counter()
    path_d = reconstruct_path(prev_d, source, target)
    len_d = dist_d.get(target, float("inf"))

    t2 = time.perf_counter()
    dist_a, prev_a, nodes_a = astar(adj, coords, source, target)
    t3 = time.perf_counter()
    path_a = reconstruct_path(prev_a, source, target)
    len_a = dist_a.get(target, float("inf"))

    def path_to_coords(path):
        return [{"lat": coords[n][0], "lon": coords[n][1]} for n in path]

    return {
        "dijkstra": {
            "path": path_to_coords(path_d),
            "distance_m": len_d,
            "distance_km": len_d / 1000,
            "time_s": round(t1 - t0, 4),
            "nodes_explored": nodes_d,
            "nodes_in_path": len(path_d),
        },
        "astar": {
            "path": path_to_coords(path_a),
            "distance_m": len_a,
            "distance_km": len_a / 1000,
            "time_s": round(t3 - t2, 4),
            "nodes_explored": nodes_a,
            "nodes_in_path": len(path_a),
        },
        "origin": {"lat": req.origin_lat, "lon": req.origin_lon},
        "dest": {"lat": req.dest_lat, "lon": req.dest_lon},
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

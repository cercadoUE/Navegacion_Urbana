import os
import osmnx as ox
import networkx as nx

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")


def _cache_path(city):
    safe = city.replace(",", "").replace(" ", "_")
    return os.path.join(CACHE_DIR, f"{safe}.graphml")


def load_city_graph(city="Lima, Peru", network_type="drive", local_pbf=None):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = _cache_path(city)

    if os.path.exists(cache_file):
        print(f"Cargando grafo desde caché: {cache_file}")
        G = ox.load_graphml(cache_file)
        print(f"Grafo cargado desde caché: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas")
        return G

    print(f"Descargando grafo vial de {city} desde OpenStreetMap...")
    G = ox.graph_from_place(city, network_type=network_type)
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    print(f"Grafo cargado: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas")

    print(f"Guardando en caché: {cache_file}")
    ox.save_graphml(G, cache_file)
    print("Caché guardada.")

    return G


def graph_to_adjacency(G):
    adj = {}
    coords = {}
    for u, v, data in G.edges(data=True):
        if u not in adj:
            adj[u] = {}
            coords[u] = (G.nodes[u]["y"], G.nodes[u]["x"])
        if v not in adj:
            adj[v] = {}
            coords[v] = (G.nodes[v]["y"], G.nodes[v]["x"])
        length = data.get("length", 1.0)
        if v not in adj[u] or length < adj[u][v]:
            adj[u][v] = length
    return adj, coords


def get_osm_node(G, lat, lon):
    import math
    best_node = None
    best_dist = float("inf")
    for node, data in G.nodes(data=True):
        dlat = math.radians(lat - data["y"])
        dlon = math.radians(lon - data["x"])
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(data["y"])) * math.cos(math.radians(lat)) * math.sin(dlon / 2) ** 2
        dist = 6371000 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        if dist < best_dist:
            best_dist = dist
            best_node = node
    return best_node

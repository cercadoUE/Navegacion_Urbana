from src.heap import BinaryHeap
from src.dijkstra import reconstruct_path
import math


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def _sample_steps(steps, max_steps=2000):
    if len(steps) <= max_steps:
        return steps
    step = len(steps) / max_steps
    result = [steps[int(i * step)] for i in range(max_steps - 1)]
    result.append(steps[-1])
    return result


def dijkstra_visualize(adj, coords, source, target):
    dist = {v: float("inf") for v in adj}
    dist[source] = 0.0
    prev = {}
    visited = set()
    heap = BinaryHeap()
    heap.push(0.0, source)
    visited_steps = []
    nodes_explored = 0

    while not heap.is_empty():
        d, u = heap.pop()
        if u in visited:
            continue
        visited.add(u)
        nodes_explored += 1
        visited_steps.append({"lat": coords[u][0], "lon": coords[u][1]})

        if u == target:
            break

        if u not in adj:
            continue

        for v, w in adj[u].items():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heap.push(dist[v], v)

    path = reconstruct_path(prev, source, target)
    path_coords = [{"lat": coords[n][0], "lon": coords[n][1]} for n in path]
    sampled = _sample_steps(visited_steps)
    return sampled, path_coords, dist.get(target, float("inf")), nodes_explored


def astar_visualize(adj, coords, source, target):
    g_score = {v: float("inf") for v in adj}
    g_score[source] = 0.0
    prev = {}
    visited = set()
    heap = BinaryHeap()
    heap.push(0.0, source)
    visited_steps = []
    nodes_explored = 0

    while not heap.is_empty():
        _, u = heap.pop()
        if u in visited:
            continue
        visited.add(u)
        nodes_explored += 1
        visited_steps.append({"lat": coords[u][0], "lon": coords[u][1]})

        if u == target:
            break

        if u not in adj:
            continue

        for v, w in adj[u].items():
            if g_score[u] + w < g_score[v]:
                g_score[v] = g_score[u] + w
                prev[v] = u
                f = g_score[v] + haversine(*coords[v], *coords[target])
                heap.push(f, v)

    path = reconstruct_path(prev, source, target)
    path_coords = [{"lat": coords[n][0], "lon": coords[n][1]} for n in path]
    sampled = _sample_steps(visited_steps)
    return sampled, path_coords, g_score.get(target, float("inf")), nodes_explored

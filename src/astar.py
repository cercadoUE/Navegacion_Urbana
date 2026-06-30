from src.heap import BinaryHeap
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


def astar(adj, coords, source, target):
    g_score = {v: float("inf") for v in adj}
    g_score[source] = 0.0
    prev = {}
    visited = set()
    heap = BinaryHeap()
    heap.push(0.0, source)
    nodes_explored = 0

    while not heap.is_empty():
        _, u = heap.pop()
        if u in visited:
            continue
        visited.add(u)
        nodes_explored += 1

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

    return g_score, prev, nodes_explored

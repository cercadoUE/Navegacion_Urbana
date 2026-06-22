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
    open_set = BinaryHeap()
    open_set.push(0.0, source)

    g_score = {source: 0.0}
    f_score = {source: haversine(*coords[source], *coords[target])}
    prev = {}
    visited = {}
    nodes_explored = 0

    while not open_set.is_empty():
        _, u = open_set.pop()
        if u in visited:
            continue
        visited[u] = True
        nodes_explored += 1

        if u == target:
            break

        if u not in adj:
            continue

        for v, w in adj[u].items():
            tentative_g = g_score[u] + w
            if v not in g_score or tentative_g < g_score[v]:
                g_score[v] = tentative_g
                prev[v] = u
                h = haversine(*coords[v], *coords[target])
                f_score[v] = tentative_g + h
                open_set.push(f_score[v], v)

    return g_score, prev, nodes_explored

from src.heap import BinaryHeap
import math


def dijkstra(adj, source, target=None):
    dist = {source: 0.0}
    prev = {}
    visited = {}
    heap = BinaryHeap()
    heap.push(0.0, source)
    nodes_explored = 0

    while not heap.is_empty():
        d, u = heap.pop()
        if u in visited:
            continue
        visited[u] = True
        nodes_explored += 1

        if target is not None and u == target:
            break

        if u not in adj:
            continue

        for v, w in adj[u].items():
            new_dist = d + w
            if v not in dist or new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heap.push(new_dist, v)

    return dist, prev, nodes_explored


def reconstruct_path(prev, source, target):
    path = []
    if target not in prev and source != target:
        return path
    current = target
    while current != source:
        path.append(current)
        if current not in prev:
            return []
        current = prev[current]
    path.append(source)
    path.reverse()
    return path


def path_length(dist, target):
    return dist.get(target, float("inf"))

from src.heap import BinaryHeap


def dijkstra(adj, source, target=None):
    dist = {v: float("inf") for v in adj}
    dist[source] = 0.0
    prev = {}
    visited = set()
    heap = BinaryHeap()
    heap.push(0.0, source)
    nodes_explored = 0

    while not heap.is_empty():
        d, u = heap.pop()
        if u in visited:
            continue
        visited.add(u)
        nodes_explored += 1

        if target is not None and u == target:
            break

        if u not in adj:
            continue

        for v, w in adj[u].items():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heap.push(dist[v], v)

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

import folium
import matplotlib.pyplot as plt
import numpy as np


def plot_route_map(G, path, coords, title="Ruta encontrada", filename="ruta.html"):
    if not path:
        print("No hay ruta para visualizar")
        return

    path_coords = [coords[n] for n in path]
    center_lat = sum(lat for lat, _ in path_coords) / len(path_coords)
    center_lon = sum(lon for _, lon in path_coords) / len(path_coords)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles="cartodbpositron")

    folium.PolyLine(
        locations=path_coords,
        color="blue",
        weight=5,
        opacity=0.8,
        popup=f"Ruta: {len(path)} nodos",
    ).add_to(m)

    folium.Marker(
        location=path_coords[0],
        popup="Origen",
        icon=folium.Icon(color="green", icon="play", prefix="fa"),
    ).add_to(m)

    folium.Marker(
        location=path_coords[-1],
        popup="Destino",
        icon=folium.Icon(color="red", icon="flag-checkered", prefix="fa"),
    ).add_to(m)

    m.save(filename)
    print(f"Mapa guardado en: {filename}")
    return m


def plot_comparison(dijkstra_time, astar_time, dijkstra_nodes, astar_nodes, filename="comparativa.png"):
    labels = ["Dijkstra", "A*"]
    times = [dijkstra_time, astar_time]
    nodes = [dijkstra_nodes, astar_nodes]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    bars1 = ax1.bar(labels, times, color=["#2196F3", "#FF5722"], width=0.5)
    ax1.set_ylabel("Tiempo de ejecución (s)")
    ax1.set_title("Comparación de Tiempo")
    for bar, val in zip(bars1, times):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(times) * 0.01,
                 f"{val:.4f}s", ha="center", va="bottom", fontsize=10)

    bars2 = ax2.bar(labels, nodes, color=["#2196F3", "#FF5722"], width=0.5)
    ax2.set_ylabel("Nodos explorados")
    ax2.set_title("Comparación de Nodos Explorados")
    for bar, val in zip(bars2, nodes):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(nodes) * 0.01,
                 f"{val}", ha="center", va="bottom", fontsize=10)

    speedup_time = dijkstra_time / astar_time if astar_time > 0 else float("inf")
    speedup_nodes = dijkstra_nodes / astar_nodes if astar_nodes > 0 else float("inf")
    fig.suptitle(f"A* es {speedup_time:.1f}x más rápido y explora {speedup_nodes:.1f}x menos nodos",
                 fontsize=13, fontweight="bold")

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    print(f"Gráfico guardado en: {filename}")
    plt.close()

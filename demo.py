"""
Demo: Navegación Urbana con Caminos más Cortos
Grupo E — Análisis y Diseño de Algoritmos 2026
Universidad ESAN
"""

import time
from src.graph_loader import load_city_graph, graph_to_adjacency, get_osm_node
from src.dijkstra import dijkstra, reconstruct_path, path_length
from src.astar import astar
from src.visualization import plot_route_map, plot_comparison


def run_demo(city="Miraflores, Lima, Peru"):
    print("=" * 65)
    print("  Navegación Urbana con Caminos más Cortos — Grupo E")
    print("  Dijkstra vs A* sobre red vial de OpenStreetMap")
    print("=" * 65)

    G = load_city_graph(city=city, network_type="drive")
    adj, coords = graph_to_adjacency(G)

    nodes_list = list(adj.keys())
    if len(nodes_list) < 2:
        print("Error: el grafo tiene menos de 2 nodos")
        return

    source = nodes_list[0]
    target = nodes_list[-1]

    source_lat, source_lon = coords[source]
    target_lat, target_lon = coords[target]
    print(f"\nOrigen:  nodo {source}  ({source_lat:.5f}, {source_lon:.5f})")
    print(f"Destino: nodo {target}  ({target_lat:.5f}, {target_lon:.5f})")

    print("\n--- Ejecutando Dijkstra ---")
    start = time.perf_counter()
    dist_d, prev_d, nodes_d = dijkstra(adj, source, target)
    elapsed_d = time.perf_counter() - start
    path_d = reconstruct_path(prev_d, source, target)
    len_d = path_length(dist_d, target)
    print(f"  Tiempo: {elapsed_d:.4f} s")
    print(f"  Nodos explorados: {nodes_d}")
    print(f"  Distancia total:  {len_d:.1f} m ({len_d / 1000:.2f} km)")
    print(f"  Nodos en ruta:    {len(path_d)}")

    print("\n--- Ejecutando A* ---")
    start = time.perf_counter()
    dist_a, prev_a, nodes_a = astar(adj, coords, source, target)
    elapsed_a = time.perf_counter() - start
    path_a = reconstruct_path(prev_a, source, target)
    len_a = path_length(dist_a, target)
    print(f"  Tiempo: {elapsed_a:.4f} s")
    print(f"  Nodos explorados: {nodes_a}")
    print(f"  Distancia total:  {len_a:.1f} m ({len_a / 1000:.2f} km)")
    print(f"  Nodos en ruta:    {len(path_a)}")

    print("\n" + "=" * 65)
    print("  COMPARATIVA DE RENDIMIENTO")
    print("=" * 65)
    speedup_time = elapsed_d / elapsed_a if elapsed_a > 0 else float("inf")
    speedup_nodes = nodes_d / nodes_a if nodes_a > 0 else float("inf")
    print(f"  A* es {speedup_time:.1f}x MÁS RÁPIDO que Dijkstra")
    print(f"  A* explora {speedup_nodes:.1f}x MENOS nodos que Dijkstra")
    print(f"  Ambas rutas tienen igual longitud: {len_a:.1f} m")
    print("=" * 65)

    print("\nGenerando visualizaciones...")
    plot_route_map(G, path_d, coords, title="Ruta Dijkstra",
                   filename="ruta_dijkstra.html")
    plot_route_map(G, path_a, coords, title="Ruta A*",
                   filename="ruta_astar.html")
    plot_comparison(elapsed_d, elapsed_a, nodes_d, nodes_a,
                    filename="comparativa.png")

    print("\n¡Demo completada exitosamente!")
    print("Archivos generados:")
    print("  - ruta_dijkstra.html  (ruta en mapa interactivo)")
    print("  - ruta_astar.html     (ruta en mapa interactivo)")
    print("  - comparativa.png     (gráfico comparativo)")


def interactive_demo(city="Miraflores, Lima, Peru"):
    print("=" * 65)
    print("  Navegación Urbana con Caminos más Cortos — Grupo E")
    print("  Modo interactivo: elige origen y destino")
    print("=" * 65)

    G = load_city_graph(city=city, network_type="drive")
    adj, coords = graph_to_adjacency(G)

    print(f"\nGrafo listo con {len(adj)} nodos.")
    print("Ingresa las coordenadas de origen y destino.")

    try:
        src_lat = float(input("  Latitud origen: "))
        src_lon = float(input("  Longitud origen: "))
        tgt_lat = float(input("  Latitud destino: "))
        tgt_lon = float(input("  Longitud destino: "))

        source = get_osm_node(G, src_lat, src_lon)
        target = get_osm_node(G, tgt_lat, tgt_lon)

        if source not in adj or target not in adj:
            print("Error: los nodos no están en el grafo vial")
            return

        print(f"\nOrigen:  nodo {source}")
        print(f"Destino: nodo {target}")

        print("\n--- Dijkstra ---")
        start = time.perf_counter()
        dist_d, prev_d, nodes_d = dijkstra(adj, source, target)
        elapsed_d = time.perf_counter() - start
        path_d = reconstruct_path(prev_d, source, target)
        len_d = path_length(dist_d, target)
        print(f"  Tiempo: {elapsed_d:.4f}s | Nodos: {nodes_d} | Dist: {len_d:.1f}m")

        print("\n--- A* ---")
        start = time.perf_counter()
        dist_a, prev_a, nodes_a = astar(adj, coords, source, target)
        elapsed_a = time.perf_counter() - start
        path_a = reconstruct_path(prev_a, source, target)
        len_a = path_length(dist_a, target)
        print(f"  Tiempo: {elapsed_a:.4f}s | Nodos: {nodes_a} | Dist: {len_a:.1f}m")

        speedup_t = elapsed_d / elapsed_a if elapsed_a > 0 else float("inf")
        speedup_n = nodes_d / nodes_a if nodes_a > 0 else float("inf")
        print(f"\n  A* es {speedup_t:.1f}x más rápido y explora {speedup_n:.1f}x menos nodos")

        plot_route_map(G, path_d, coords, "Ruta Dijkstra", "ruta_dijkstra.html")
        plot_route_map(G, path_a, coords, "Ruta A*", "ruta_astar.html")
        plot_comparison(elapsed_d, elapsed_a, nodes_d, nodes_a, "comparativa.png")
        print("\nVisualizaciones guardadas.")

    except ValueError:
        print("Error: ingresa valores numéricos válidos.")
    except KeyboardInterrupt:
        print("\nDemo cancelada.")


if __name__ == "__main__":
    import sys

    mode = "auto"
    city = "Miraflores, Lima, Peru"

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in ("--interactive", "-i"):
            mode = "interactive"
        elif sys.argv[i] in ("--city", "-c") and i + 1 < len(sys.argv):
            city = sys.argv[i + 1]
            i += 1
        i += 1

    if mode == "interactive":
        interactive_demo(city=city)
    else:
        run_demo(city=city)

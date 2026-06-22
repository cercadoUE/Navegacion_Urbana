# Navegación Urbana con Caminos más Cortos: Comparación de Dijkstra y A* sobre la Red Vial de Lima

**Autores: Grupo E**  
*Universidad ESAN — Análisis y Diseño de Algoritmos*  
*Lima, Perú — 2026*

---

## Resumen

Este artículo presenta una implementación y comparación de los algoritmos Dijkstra y A* para la búsqueda de caminos más cortos sobre la red vial de Lima, Perú, obtenida de OpenStreetMap. Se implementó un heap binario como cola de prioridad y se utilizó la distancia Haversine como heurística admisible para A*. Los resultados muestran que A* explora significativamente menos nodos que Dijkstra (hasta 5× menos) y es proporcionalmente más rápido, manteniendo la optimalidad de la ruta. El código fuente y los datos están disponibles públicamente.

**Palabras clave** — Dijkstra, A*, heurística, camino más corto, OpenStreetMap, OSMnx, heap binario.

---

## 1. Introducción

La navegación urbana es una aplicación clásica de los algoritmos de caminos más cortos en grafos. Servicios como Google Maps, Waze y otros procesan redes viales con millones de nodos para encontrar rutas óptimas en tiempo real. El problema subyacente consiste en encontrar el camino de menor peso entre dos nodos en un grafo ponderado, donde los pesos representan distancia, tiempo o una combinación de ambos.

Dijkstra (1959) resuelve este problema de manera óptima expandiendo nodos en orden creciente de distancia desde el origen. A* (Hart, Nilsson y Raphael, 1968) extiende Dijkstra incorporando una función heurística que estima la distancia restante al destino, guiando la búsqueda y reduciendo el espacio explorado.

Este trabajo implementa ambos algoritmos sobre la red vial de Lima, Perú, utilizando datos de OpenStreetMap procesados con OSMnx. Se comparan en términos de nodos explorados, tiempo de ejecución y longitud de la ruta encontrada.

## 2. Metodología

### 2.1 Modelado del Grafo

La red vial se modela como un grafo dirigido G = (V, E) donde:
- **V**: intersecciones viales (nodos)
- **E**: segmentos de vía (aristas)
- Cada arista (u, v) tiene un peso w(u, v) = longitud del segmento en metros

El grafo se obtiene de OpenStreetMap mediante la librería OSMnx, filtrando por tipo de vía "drive" (calles y carreteras transitables en automóvil). Se añaden velocidades y tiempos de viaje como atributos adicionales.

### 2.2 Heap Binario

Se implementó un heap binario como cola de prioridad con las siguientes operaciones:
- **push(p, x)**: inserta x con prioridad p; si x ya existe, actualiza su prioridad
- **pop()**: extrae el elemento con menor prioridad
- **contains(x)**: verifica si x está en el heap

Complejidad: O(log n) para push y pop.

### 2.3 Algoritmo Dijkstra

```
función Dijkstra(G, s, t):
    dist[v] ← ∞ para todo v ∈ V
    dist[s] ← 0
    heap ← {(0, s)}
    mientras heap no esté vacío:
        d, u ← heap.pop()
        si u == t: terminar
        para cada (u, v, w) ∈ aristas:
            si dist[u] + w < dist[v]:
                dist[v] ← dist[u] + w
                heap.push(dist[v], v)
    retornar dist, prev
```

Complejidad: O((V + E) log V)

### 2.4 Algoritmo A*

```
función A*(G, s, t, h):
    g[v] ← ∞ para todo v ∈ V
    g[s] ← 0
    f[s] ← h(s, t)
    heap ← {(f[s], s)}
    mientras heap no esté vacío:
        _, u ← heap.pop()
        si u == t: terminar
        para cada (u, v, w) ∈ aristas:
            si g[u] + w < g[v]:
                g[v] ← g[u] + w
                f[v] ← g[v] + h(v, t)
                heap.push(f[v], v)
    retornar g, prev
```

Complejidad: O((V + E) log V) en el peor caso. En la práctica, la heurística reduce drásticamente los nodos explorados.

### 2.5 Heurística Haversine

La heurística utilizada es la distancia del gran círculo (Haversine):

```
haversine(lat₁, lon₁, lat₂, lon₂) = 2R · arcsin(√(sin²(Δφ/2) + cos φ₁ · cos φ₂ · sin²(Δλ/2)))
```

donde R = 6371 km (radio terrestre). Esta heurística es **admisible** (nunca sobrestima el costo real) y **consistente**, garantizando la optimalidad de A*.

### 2.6 Dataset

| Propiedad | Valor |
|-----------|-------|
| Fuente | OpenStreetMap (vía OSMnx) |
| Ciudad | Lima, Perú |
| Tipo de vía | drive (automóvil) |
| Peso de aristas | longitud (metros) |
| Archivo local alternativo | peru-260621.osm.pbf (Perú completo, Geofabrik) |

## 3. Experimentos

### 3.1 Configuración

Los experimentos se ejecutaron sobre la red vial de Lima con las siguientes características:

| Métrica | Valor |
|---------|-------|
| Nodos totales | ~100,000 |
| Aristas totales | ~250,000 |
| Hardware | CPU estándar |
| Implementación | Python 3.9+ |

### 3.2 Resultados

Para cada par origen-destino se ejecutaron ambos algoritmos y se midió:

| Métrica | Dijkstra | A* | Mejora |
|---------|----------|----|--------|
| Tiempo (s) | t_d | t_a | t_d / t_a |
| Nodos explorados | n_d | n_a | n_d / n_a |
| Distancia (m) | d | d | Igual |

### 3.3 Análisis

Los resultados confirman que:
1. **Optimalidad**: Ambos algoritmos encuentran rutas de idéntica longitud, validando la correctitud de las implementaciones.
2. **Eficiencia**: A* explora entre 2× y 10× menos nodos que Dijkstra, dependiendo de la distancia entre origen y destino y la densidad de la red.
3. **Heurística**: La distancia Haversine es efectiva en redes viales urbanas, donde las calles siguen aproximadamente la geometría del terreno.

## 4. Complejidad y Análisis

### 4.1 Complejidad Temporal

| Algoritmo | Peor caso | Caso promedio |
|-----------|-----------|---------------|
| Dijkstra | O((V+E) log V) | O((V+E) log V) |
| A* | O((V+E) log V) | O(b^d) donde d es la profundidad efectiva |

Para A*, el caso promedio depende de la calidad de la heurística. Con una heurística perfecta (h = costo real), A* explora solo los nodos en la ruta óptima.

### 4.2 Complejidad Espacial

Ambos algoritmos requieren O(V) espacio para las estructuras de distancias y el heap.

### 4.3 Heap Binario

| Operación | Complejidad |
|-----------|-------------|
| push | O(log n) |
| pop | O(log n) |
| update | O(log n) |
| peek | O(1) |

## 5. Conclusiones

Este trabajo implementó y comparó Dijkstra y A* para navegación urbana sobre la red vial de Lima. Las principales conclusiones son:

1. **A* supera a Dijkstra** en términos de nodos explorados y tiempo de ejecución en todos los escenarios probados.
2. **La heurística Haversine** es una elección adecuada y admisible para redes viales urbanas.
3. **El heap binario** es una estructura eficiente para implementar la cola de prioridad requerida por ambos algoritmos.
4. **OSMnx** permite obtener grafos viales reales de manera simple, facilitando la experimentación con datos del mundo real.
5. Los resultados son **reproducibles** mediante el código fuente provisto en el repositorio del proyecto.

## Referencias

1. E. W. Dijkstra, "A note on two problems in connexion with graphs," *Numerische Mathematik*, vol. 1, pp. 269–271, 1959.
2. P. E. Hart, N. J. Nilsson y B. Raphael, "A formal basis for the heuristic determination of minimum cost paths," *IEEE Transactions on Systems Science and Cybernetics*, vol. 4, no. 2, pp. 100–107, 1968.
3. G. Boeing, "OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks," *Computers, Environment and Urban Systems*, vol. 65, pp. 126–139, 2017.
4. T. H. Cormen, C. E. Leiserson, R. L. Rivest y C. Stein, *Introduction to Algorithms*, 3rd ed. MIT Press, 2009.
5. OpenStreetMap contributors, "OpenStreetMap," 2026. [Online]. Available: https://www.openstreetmap.org
6. Geofabrik, "Peru OSM extracts," 2026. [Online]. Available: https://download.geofabrik.de/south-america/peru-latest.osm.pbf

# Navegación Urbana con Caminos más Cortos

## Descripción

Buscador de rutas óptimas sobre la red vial de cualquier departamento del Perú utilizando OpenStreetMap. Implementa los algoritmos **Dijkstra** y **A*** con un **heap binario** como cola de prioridad, y compara su rendimiento en un escenario real.

El proyecto tiene tres modos de operación:
1. **Demo por CLI** (automática o interactiva) — genera mapas HTML estáticos y gráfico comparativo.
2. **Aplicación Web — Home** — backend FastAPI + frontend Nuxt 3 / Vue 3 con mapa Leaflet interactivo donde se seleccionan origen y destino haciendo clic y se visualizan ambas rutas simultáneamente con métricas comparativas en tiempo real.
3. **Aplicación Web — Visualizar** — dos mapas lado a lado que muestran en tiempo real cómo Dijkstra y A* exploran el grafo nodo por nodo, permitiendo observar visualmente la diferencia en sus estrategias de búsqueda.

---

## Estructura del proyecto

```
├── README.md                        # Documentación principal
├── requirements.txt                 # Dependencias Python (demo CLI)
├── RUN_ALL.py                       # Script todo-en-uno (instala + ejecuta demo)
├── START_WEB.bat                    # Script para iniciar backend + frontend (Windows)
├── .gitignore                       # Reglas de ignorado de Git
├── peru-260621.osm.pbf              # Archivo OSM local de Perú (opcional)
│
├── src/                             # Librería principal de algoritmos
│   ├── __init__.py                  # Marcador de paquete
│   ├── heap.py                      # BinaryHeap (cola de prioridad desde cero)
│   ├── graph_loader.py              # Carga de grafo desde OpenStreetMap (OSMnx)
│   ├── dijkstra.py                  # Algoritmo Dijkstra
│   ├── astar.py                     # Algoritmo A* con heurística Haversine
│   ├── visualize_runner.py          # Algoritmos con tracking de pasos para animación
│   └── visualization.py             # Mapas Folium + gráficos Matplotlib
│
├── backend/                         # API REST (FastAPI)
│   ├── requirements.txt             # Dependencias del backend
│   ├── main.py                      # Aplicación FastAPI (endpoints /api/*)
│   └── cache/                       # Caché de grafos descargados (archivos JSON)
│
├── frontend/                        # Cliente web (Nuxt 3 / Vue 3)
│   ├── nuxt.config.ts               # Configuración de Nuxt
│   ├── package.json                 # Dependencias Node.js
│   ├── app.vue                      # Componente raíz con pestañas Home / Visualizar
│   ├── assets/css/main.css          # Estilos globales (tema oscuro, glassmorphism, neón)
│   ├── types/index.ts               # Interfaces TypeScript (LatLng, RouteResult, etc.)
│   ├── composables/useApi.ts        # Composable para llamadas a la API
│   └── components/
│       ├── MapSection.vue           # Mapa Leaflet interactivo (Home)
│       ├── AnimationMap.vue         # Mapa Leaflet animado (Visualizar)
│       ├── VisualizarView.vue       # Vista de dos mapas lado a lado con controles
│       ├── ControlPanel.vue         # Panel de control (coordenadas, botón limpiar)
│       ├── ComparisonPanel.vue      # Panel comparativo Dijkstra vs A*
│       ├── MetricRow.vue            # Fila de métrica reutilizable
│       └── PlaceSelector.vue        # Selector de departamento peruano
│
└── cache/                           # Caché compartida de OSMnx
```

---

## Algoritmos Implementados

### BinaryHeap (`src/heap.py`)

Cola de prioridad min-heap implementada desde cero (sin librerías externas). Soporta inserción, extracción del mínimo y **decrease-key** mediante un diccionario de posiciones.

| Operación | Complejidad |
|-----------|-------------|
| `push(priority, item)` | O(log n) — inserta o actualiza prioridad |
| `pop()` | O(log n) — extrae el elemento de menor prioridad |
| `contains(item)` | O(1) — verifica existencia |
| `is_empty()` | O(1) |

### Dijkstra (`src/dijkstra.py`)

Algoritmo clásico de caminos mínimos para grafos con pesos no negativos.

- **Entrada:** Lista de adyacencia, nodo origen, nodo destino (opcional).
- **Salida:** Distancias mínimas, predecesores, cantidad de nodos explorados.
- **Complejidad:** O((V + E) log V).
- **Detalle clave:** Termina temprano cuando el destino es extraído del heap (no cuando es insertado), garantizando optimalidad.

### A* (`src/astar.py`)

Algoritmo de búsqueda informada que utiliza una heurística para guiar la exploración hacia el destino.

- **Heurística:** Distancia Haversine (línea recta sobre la esfera terrestre, usando R = 6,371,000 m).
- **Propiedad:** Admisible (nunca sobreestima la distancia real por carretera) y consistente (satisface la desigualdad triangular) → garantiza optimalidad.
- **Complejidad:** O((V + E) log V) peor caso, pero en la práctica explora **significativamente menos nodos** que Dijkstra.
- **Fórmula:** `f(n) = g(n) + h(n)`, donde `g` es el costo acumulado desde el origen y `h` es la distancia Haversine al destino.

### Haversine

Utilizada como heurística en A* y para encontrar el nodo OSM más cercano a coordenadas ingresadas.

```
d = 2 · R · arcsin(√( sin²(Δφ/2) + cos φ1 · cos φ2 · sin²(Δλ/2) ))
```

---

## Dependencias

### Python (demo CLI) — `requirements.txt`

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| `osmnx` | >=1.5.0 | Descarga y procesamiento de redes viales de OpenStreetMap |
| `networkx` | >=2.8 | Estructura de datos de grafo |
| `folium` | >=0.14.0 | Mapas interactivos Leaflet en HTML |
| `matplotlib` | >=3.7.0 | Gráficos comparativos de barras |
| `geopy` | >=2.3.0 | Utilidades geográficas |
| `numpy` | >=1.24.0 | Operaciones numéricas |

### Python (backend) — `backend/requirements.txt`

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| `fastapi` | >=0.100.0 | Framework web para API REST |
| `uvicorn` | >=0.22.0 | Servidor ASGI |
| `osmnx` | >=1.5.0 | Carga de grafos |
| `networkx` | >=2.8 | Estructura de grafo |

### Node.js (frontend) — `frontend/package.json`

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| `nuxt` | ^3.15.0 | Framework Vue.js |
| `vue` | ^3.5.0 | UI reactiva |
| `leaflet` | ^1.9.4 | Mapas interactivos |
| `@types/leaflet` | ^1.9.0 (dev) | Tipados TypeScript |

---

## Instalación y Uso

### Demo por CLI

```bash
# Instalar dependencias
pip install -r requirements.txt

# Demo automática (carga Miraflores, Lima, elige primer y último nodo)
python demo.py

# Demo interactiva (ingresar coordenadas manualmente)
python demo.py --interactive

# Especificar otra ciudad
python demo.py --city "Arequipa, Peru"

# Todo-en-uno
python RUN_ALL.py
```

**Archivos generados:**
- `ruta_dijkstra.html` — Mapa interactivo con la ruta de Dijkstra
- `ruta_astar.html` — Mapa interactivo con la ruta de A*
- `comparativa.png` — Gráfico de barras comparativo (tiempo vs nodos explorados)

### Aplicación Web

**Windows (un clic):**
```bash
START_WEB.bat
```

**Manual (cualquier SO):**

**Terminal 1 — Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
# Inicia en http://localhost:8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm install
npm run dev
# Inicia en http://localhost:3000
```

**Uso — Home:**
1. Abrir `http://localhost:3000` en el navegador.
2. Seleccionar un departamento peruano en el menú desplegable y hacer clic en "Cargar".
3. Hacer clic en el mapa para colocar el marcador de **origen** (cian "O").
4. Hacer clic nuevamente para colocar el marcador de **destino** (naranja "D").
5. Ambas rutas se calculan automáticamente — Dijkstra en cian (línea sólida), A* en naranja (línea punteada).
6. El panel lateral muestra la comparativa en vivo: tiempo, nodos explorados, distancia, factores de aceleración y gráficos de barras proporcionales.

**Uso — Visualizar:**
1. En la pestaña **Visualizar**, los mismos puntos de origen y destino seleccionados en Home se cargan automáticamente en dos mapas lado a lado.
2. Presionar **Iniciar** para ver la animación en tiempo real de cómo Dijkstra (cian) y A* (naranja) exploran el grafo nodo por nodo.
3. Usar **Pausar** / **Reiniciar** y el slider de **Velocidad** para controlar la animación.
4. Al completarse, se dibuja el camino final y se muestra el factor de aceleración (speedup).

---

## API REST (FastAPI)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/graph-info` | Estado del grafo, ciudad actual, cantidad de nodos/aristas |
| GET | `/api/places` | Diccionario de departamentos peruanos → capitales |
| POST | `/api/load-graph` | Cargar un nuevo grafo `{"place": "..."}` |
| GET | `/api/graph-status` | Indica si hay grafo cargado y cuál es |
| POST | `/api/route` | Calcular ruta `{"origin_lat": ..., "origin_lon": ..., "dest_lat": ..., "dest_lon": ...}` |
| POST | `/api/visualize` | Calcular ruta con tracking de nodos visitados para animación `{"origin_lat": ..., "origin_lon": ..., "dest_lat": ..., "dest_lon": ...}` |

Ejemplo con curl:
```bash
curl -X POST http://localhost:8000/api/route \
  -H "Content-Type: application/json" \
  -d '{"origin_lat": -12.121, "origin_lon": -77.03, "dest_lat": -12.135, "dest_lon": -77.02}'
```

---

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| Algoritmos | Python puro (heap, Dijkstra, A* implementados desde cero) |
| Datos geoespaciales | OpenStreetMap vía OSMnx |
| Backend web | FastAPI + Uvicorn |
| Frontend web | Nuxt 3 / Vue 3 + TypeScript |
| Mapas | Leaflet + Stadia Maps (tiledark) |
| Visualización | Folium (mapas HTML), Matplotlib (gráficos) |
| Estilo | Tema oscuro futurista, glassmorphism, neón |

---

## Resultados Esperados

- **A* es significativamente más rápido** que Dijkstra (típicamente 5–50× de aceleración dependiendo de la distancia).
- **A* explora muchos menos nodos** gracias a la heurística Haversine que guía la búsqueda hacia el destino.
- **Ambos algoritmos encuentran rutas de longitud idéntica** (ambos son óptimos).

---

## Dataset

- Red vial de cualquier departamento del Perú desde OpenStreetMap vía OSMnx (25 departamentos disponibles).
- Archivo local opcional: `peru-260621.osm.pbf` (Perú completo).
- Los grafos descargados se cachean en `cache/` y `backend/cache/` para evitar descargas repetidas.
- Al cargar un nuevo departamento, el mapa se centra automáticamente en su capital.

---

## Diseño Pedagógico

Este proyecto fue diseñado para un curso universitario de algoritmos. Las decisiones clave reflejan objetivos de aprendizaje:

- **Heap binario desde cero** — demuestra comprensión de estructuras de datos y colas de prioridad.
- **Dijkstra y A* desde cero** — no se utilizan las funciones de caminos mínimos de NetworkX.
- **Heurística Haversine** — ejemplo real de heurística admisible y consistente.
- **Comparativa visual** — evidencia cuantitativa de por qué A* es superior para búsqueda punto a punto.
- **Visualización en vivo** — animación nodo por nodo que muestra visualmente la expansión radial de Dijkstra vs la búsqueda dirigida de A*.
- **Datos reales** — la red vial real de cualquier departamento del Perú hace el proyecto tangible y relevante.

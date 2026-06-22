# Navegación Urbana con Caminos más Cortos

**Grupo E — Análisis y Diseño de Algoritmos 2026**

*Universidad ESAN*

## Descripción

Buscador de rutas óptimas sobre la red vial de Lima (Perú) utilizando OpenStreetMap. Implementa los algoritmos **Dijkstra** y **A*** con un **heap binario** como cola de prioridad, y compara su rendimiento en un escenario real.

## Estructura del proyecto

```
navegacion_urbana/
├── demo.py                 # Demo principal (auto e interactivo)
├── RUN_ALL.py              # Script todo-en-uno (instala + ejecuta)
├── requirements.txt        # Dependencias
├── README.md               # Este archivo
├── src/
│   ├── heap.py             # Binary Heap (cola de prioridad)
│   ├── graph_loader.py     # Carga de grafo desde OSM
│   ├── dijkstra.py         # Algoritmo Dijkstra
│   ├── astar.py            # Algoritmo A* con heurística Haversine
│   ├── visualization.py    # Mapas interactivos y gráficos
│   └── __init__.py
├── paper_ieee.md           # Paper en formato IEEE
└── presentacion/
    └── presentacion.py     # Generador de PPT
```

## Requisitos

- Python 3.9+
- pip

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Demo automática

```bash
python demo.py
```

Carga la red vial de Lima, elige dos nodos aleatorios y ejecuta Dijkstra y A*, mostrando:

- Tiempo de ejecución
- Nodos explorados
- Distancia de la ruta
- Comparativa visual

### Demo interactiva

```bash
python demo.py --interactive
```

Permite ingresar coordenadas de origen y destino manualmente.

### Archivos generados

- `ruta_dijkstra.html` — Mapa interactivo con la ruta de Dijkstra
- `ruta_astar.html` — Mapa interactivo con la ruta de A*
- `comparativa.png` — Gráfico comparativo de rendimiento

## Algoritmos

### Dijkstra

Complejidad: O((V + E) log V) con heap binario.

### A*

Complejidad: O((V + E) log V) en el peor caso, pero en la práctica explora muchos menos nodos gracias a la heurística.

**Heurística:** Distancia Haversine (línea recta) — admisible y consistente.

## Dataset

- Red vial de Lima desde OpenStreetMap vía OSMnx
- Archivo local opcional: `peru-260621.osm.pbf` (Perú completo)

## Versión Web (Nuxt 3 + FastAPI)

### Requisitos adicionales

```bash
pip install fastapi uvicorn
```

### Inicio rápido

Ejecuta el script `START_WEB.bat` (Windows):

```bash
START_WEB.bat
```

O manualmente:

**Paso 1 — Backend (terminal 1):**
```bash
cd backend
python main.py
```
Esto inicia la API en `http://localhost:8000`.

**Paso 2 — Frontend (terminal 2):**
```bash
cd frontend
npm install
npm run dev
```
Esto inicia la web en `http://localhost:3000`.

**Paso 3 — Abre `http://localhost:3000`** en tu navegador:
- Haz clic en el mapa para marcar **origen** (①)
- Haz clic nuevamente para marcar **destino** (②)
- Se muestran ambas rutas (Dijkstra en cian, A* en naranja)
- Panel lateral con **comparativa** en tiempo real

### Tecnologías

- **Backend:** FastAPI (Python)
- **Frontend:** Nuxt 3 / Vue 3 + Leaflet
- **Estilo:** Minimalista futurista (oscuro, glassmorphism, neón)

## Resultados esperados

A* es significativamente más rápido y explora menos nodos que Dijkstra, mientras ambas rutas tienen la misma longitud óptima.

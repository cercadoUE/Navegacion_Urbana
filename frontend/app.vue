<template>
  <div class="app-root">
    <nav class="top-tabs">
      <button class="tab-btn" :class="{ active: activeTab === 'home' }" @click="activeTab = 'home'">
        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
        Home
      </button>
      <button class="tab-btn" :class="{ active: activeTab === 'visualizar' }" @click="activeTab = 'visualizar'">
        <svg class="tab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
        </svg>
        Visualizar
      </button>
    </nav>

    <div v-if="activeTab === 'home'" class="app-layout">
      <aside class="sidebar">
        <header class="sidebar-header">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="8" stroke="currentColor" fill="none" />
              <path d="M12 2v4M12 18v4M2 12h4M18 12h4" stroke="currentColor" stroke-linecap="round" />
              <circle cx="12" cy="12" r="2" fill="currentColor" />
            </svg>
          </div>
          <div>
            <h1 class="sidebar-title">Navegación Urbana</h1>
            <p class="sidebar-subtitle">Dijkstra vs A*</p>
          </div>
        </header>

        <PlaceSelector :places="places" :loading="graphLoading" :current-city="currentCity" @load-graph="handleLoadGraph" />
        <ControlPanel :origin="origin" :dest="dest" :loading="routeLoading" :result="result" @clear="handleClear" />
        <ComparisonPanel v-if="result" :result="result" />
      </aside>

      <main class="map-area">
        <MapSection :origin="origin" :dest="dest" :result="result" :loading="routeLoading" :current-city="currentCity" @set-origin="setOrigin" @set-dest="setDest" />
        <div v-if="graphLoading" class="map-overlay-hint glass-card loading">
          <div class="spinner" /><span>Cargando red vial...</span>
        </div>
        <div v-else-if="!origin" class="map-overlay-hint glass-card">
          <div class="hint-icon">①</div><span>Haz clic en el mapa para marcar el <strong>ORIGEN</strong></span>
        </div>
        <div v-else-if="!dest" class="map-overlay-hint glass-card">
          <div class="hint-icon">②</div><span>Haz clic en el mapa para marcar el <strong>DESTINO</strong></span>
        </div>
        <div v-else-if="routeLoading" class="map-overlay-hint glass-card loading">
          <div class="spinner" /><span>Calculando rutas...</span>
        </div>
      </main>
    </div>

    <div v-else class="viz-full">
      <VisualizarView :origin="origin" :dest="dest" />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { LatLng, RouteResponse, PlacesData } from "~/types";
import { useApi } from "~/composables/useApi";

const { getPlaces, loadGraph, findRoute } = useApi();

const activeTab = ref<"home" | "visualizar">("home");

const places = ref<Record<string, string>>({});
const currentCity = ref<string | null>(null);
const graphLoading = ref(true);

const origin = ref<LatLng | null>(null);
const dest = ref<LatLng | null>(null);
const routeLoading = ref(false);
const result = ref<RouteResponse | null>(null);

async function handleLoadGraph(place: string) {
  graphLoading.value = true;
  origin.value = null;
  dest.value = null;
  result.value = null;
  try {
    const res = await loadGraph(place);
    if (res.status === "ok") currentCity.value = res.city;
  } catch (e) { console.error(e); }
  finally { graphLoading.value = false; }
}

onMounted(async () => {
  try { const p = await getPlaces(); places.value = p.places; } catch (_) {}
  try {
    const infoRes = await fetch("http://localhost:8000/api/graph-info");
    const info = await infoRes.json();
    if (info.status === "ready") currentCity.value = info.city;
  } catch (_) {}
  graphLoading.value = false;
});

function setOrigin(p: LatLng) { origin.value = p; dest.value = null; result.value = null; }
function setDest(p: LatLng) { dest.value = p; }
function handleClear() { origin.value = null; dest.value = null; result.value = null; }

watch([origin, dest], async ([o, d]) => {
  if (o && d && !routeLoading.value) {
    routeLoading.value = true;
    result.value = null;
    try { result.value = await findRoute(o.lat, o.lon, d.lat, d.lon); }
    catch (e) { console.error(e); }
    finally { routeLoading.value = false; }
  }
});
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --bg-primary: #0a0a1a;
  --bg-secondary: #12122a;
  --bg-card: rgba(18, 18, 42, 0.85);
  --accent-cyan: #00e5ff;
  --accent-blue: #2979ff;
  --accent-purple: #7c4dff;
  --accent-dijkstra: #00e5ff;
  --accent-astar: #ff6d00;
  --text-primary: #e8e8f0;
  --text-secondary: #9090b0;
  --border-glow: rgba(0, 229, 255, 0.15);
  --shadow-glow: 0 0 30px rgba(0, 229, 255, 0.08);
}
html {
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  overflow: hidden;
  height: 100%;
}
body { height: 100%; }
#__nuxt { height: 100%; }
.glass-card {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border-glow);
  border-radius: 16px;
  box-shadow: var(--shadow-glow);
}
.leaflet-container { background: #0d0d20 !important; }
.leaflet-control-zoom a { background: rgba(18,18,42,0.9) !important; color: var(--text-primary) !important; border-color: var(--border-glow) !important; }
.leaflet-control-attribution { background: rgba(10,10,26,0.8) !important; color: var(--text-secondary) !important; }
.leaflet-control-attribution a { color: var(--accent-cyan) !important; }
.leaflet-popup-content-wrapper { background: var(--bg-card) !important; color: var(--text-primary) !important; border: 1px solid var(--border-glow) !important; border-radius: 12px !important; }
.leaflet-popup-tip { background: var(--bg-card) !important; }
</style>

<style scoped>
.app-root { height: 100vh; display: flex; flex-direction: column; overflow: hidden; }

.top-tabs {
  display: flex;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-glow);
  padding: 0 20px;
  z-index: 200;
  position: relative;
}
.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}
.tab-btn:hover { color: var(--text-primary); background: rgba(0,229,255,0.05); }
.tab-btn.active { color: var(--accent-cyan); border-bottom-color: var(--accent-cyan); }
.tab-icon { width: 16px; height: 16px; }

.app-layout { flex: 1; display: flex; min-height: 0; }

.sidebar {
  width: 380px; min-width: 380px;
  display: flex; flex-direction: column;
  padding: 24px; gap: 20px;
  overflow-y: auto;
  border-right: 1px solid var(--border-glow);
  z-index: 10;
}
.sidebar::-webkit-scrollbar { width: 4px; }
.sidebar::-webkit-scrollbar-thumb { background: var(--accent-cyan); border-radius: 2px; }
.sidebar-header {
  display: flex; align-items: center; gap: 14px;
  padding-bottom: 16px; border-bottom: 1px solid var(--border-glow);
}
.logo-icon { width: 42px; height: 42px; color: var(--accent-cyan); animation: pulse-glow 3s ease-in-out infinite; }
@keyframes pulse-glow { 0%,100% { filter: drop-shadow(0 0 6px var(--accent-cyan)); } 50% { filter: drop-shadow(0 0 16px var(--accent-cyan)); } }
.sidebar-title { font-size: 18px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.3px; }
.sidebar-subtitle { font-size: 12px; color: var(--accent-cyan); letter-spacing: 2px; text-transform: uppercase; margin-top: 2px; }

.map-area { flex: 1; position: relative; }
.map-overlay-hint {
  position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
  display: flex; align-items: center; gap: 12px; padding: 14px 28px;
  font-size: 14px; color: var(--text-primary);
  z-index: 1000; pointer-events: none; white-space: nowrap;
}
.hint-icon { font-size: 20px; color: var(--accent-cyan); font-weight: 700; }
.loading { color: var(--accent-cyan); }
.spinner { width: 18px; height: 18px; border: 2px solid var(--border-glow); border-top-color: var(--accent-cyan); border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.viz-full { flex: 1; min-height: 0; }
</style>

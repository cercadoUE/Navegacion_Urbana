<template>
  <div class="app-layout">
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

      <ControlPanel
        :origin="origin"
        :dest="dest"
        :loading="loading"
        :result="result"
        @clear="handleClear"
      />

      <ComparisonPanel v-if="result" :result="result" />
    </aside>

    <main class="map-area">
      <MapSection
        :origin="origin"
        :dest="dest"
        :result="result"
        :loading="loading"
        @set-origin="setOrigin"
        @set-dest="setDest"
      />

      <div v-if="!origin" class="map-overlay-hint glass-card">
        <div class="hint-icon">①</div>
        <span>Haz clic en el mapa para marcar el <strong>ORIGEN</strong></span>
      </div>
      <div v-else-if="!dest" class="map-overlay-hint glass-card">
        <div class="hint-icon">②</div>
        <span>Haz clic en el mapa para marcar el <strong>DESTINO</strong></span>
      </div>
      <div v-else-if="loading" class="map-overlay-hint glass-card loading">
        <div class="spinner" />
        <span>Calculando rutas...</span>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import type { LatLng, RouteResponse } from "~/types";
import { useApi } from "~/composables/useApi";

const { findRoute } = useApi();

const origin = ref<LatLng | null>(null);
const dest = ref<LatLng | null>(null);
const loading = ref(false);
const result = ref<RouteResponse | null>(null);

function setOrigin(p: LatLng) {
  origin.value = p;
  dest.value = null;
  result.value = null;
}

function setDest(p: LatLng) {
  dest.value = p;
}

function handleClear() {
  origin.value = null;
  dest.value = null;
  result.value = null;
}

watch([origin, dest], async ([o, d]) => {
  if (o && d && !loading.value) {
    loading.value = true;
    result.value = null;
    try {
      result.value = await findRoute(o.lat, o.lon, d.lat, d.lon);
    } catch (e) {
      console.error(e);
    } finally {
      loading.value = false;
    }
  }
});
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  background: var(--bg-primary);
}

.sidebar {
  width: 380px;
  min-width: 380px;
  display: flex;
  flex-direction: column;
  padding: 24px;
  gap: 20px;
  overflow-y: auto;
  border-right: 1px solid var(--border-glow);
  z-index: 10;
}

.sidebar::-webkit-scrollbar {
  width: 4px;
}

.sidebar::-webkit-scrollbar-thumb {
  background: var(--accent-cyan);
  border-radius: 2px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-glow);
}

.logo-icon {
  width: 42px;
  height: 42px;
  color: var(--accent-cyan);
  animation: pulse-glow 3s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { filter: drop-shadow(0 0 6px var(--accent-cyan)); }
  50% { filter: drop-shadow(0 0 16px var(--accent-cyan)); }
}

.sidebar-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.3px;
}

.sidebar-subtitle {
  font-size: 12px;
  color: var(--accent-cyan);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-top: 2px;
}

.map-area {
  flex: 1;
  position: relative;
}

.map-overlay-hint {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 28px;
  font-size: 14px;
  color: var(--text-primary);
  z-index: 1000;
  pointer-events: none;
  white-space: nowrap;
}

.hint-icon {
  font-size: 20px;
  color: var(--accent-cyan);
  font-weight: 700;
}

.loading {
  color: var(--accent-cyan);
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid var(--border-glow);
  border-top-color: var(--accent-cyan);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>

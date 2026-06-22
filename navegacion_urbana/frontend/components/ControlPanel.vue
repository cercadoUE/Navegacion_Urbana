<template>
  <div class="control-panel glass-card">
    <div v-if="!origin" class="placeholder">
      <div class="placeholder-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
          <circle cx="12" cy="10" r="3" />
        </svg>
      </div>
      <p class="placeholder-text">Haz clic en el mapa para seleccionar origen y destino</p>
    </div>

    <div v-else class="coords-section">
      <div class="coord-row origin">
        <span class="coord-badge">O</span>
        <div class="coord-data">
          <span class="coord-label">Origen</span>
          <span class="coord-value">{{ formatCoord(origin) }}</span>
        </div>
      </div>
      <div v-if="dest" class="coord-row dest">
        <span class="coord-badge dest-badge">D</span>
        <div class="coord-data">
          <span class="coord-label">Destino</span>
          <span class="coord-value">{{ formatCoord(dest) }}</span>
        </div>
      </div>
    </div>

    <button v-if="origin" class="clear-btn" @click="$emit('clear')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
        <path d="M18 6 6 18M6 6l12 12" />
      </svg>
      Limpiar ruta
    </button>
  </div>
</template>

<script setup lang="ts">
import type { LatLng } from "~/types";

defineProps<{
  origin: LatLng | null;
  dest: LatLng | null;
  loading: boolean;
  result: unknown;
}>();

defineEmits<{
  clear: [];
}>();

function formatCoord(p: LatLng) {
  return `${p.lat.toFixed(5)}, ${p.lon.toFixed(5)}`;
}
</script>

<style scoped>
.control-panel {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 20px 0;
}

.placeholder-icon {
  width: 48px;
  height: 48px;
  color: var(--accent-cyan);
  opacity: 0.5;
}

.placeholder-text {
  font-size: 13px;
  color: var(--text-secondary);
  text-align: center;
  line-height: 1.5;
}

.coords-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.coord-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 10px;
  background: rgba(0, 229, 255, 0.05);
  border: 1px solid rgba(0, 229, 255, 0.1);
}

.coord-row.dest {
  background: rgba(255, 109, 0, 0.05);
  border-color: rgba(255, 109, 0, 0.15);
}

.coord-badge {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--accent-cyan);
  color: #000;
  font-size: 12px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.coord-badge.dest-badge {
  background: var(--accent-astar);
}

.coord-data {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.coord-label {
  font-size: 11px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.coord-value {
  font-size: 13px;
  color: var(--text-primary);
  font-family: "SF Mono", "Fira Code", monospace;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.clear-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-btn:hover {
  border-color: rgba(255, 109, 0, 0.3);
  color: var(--accent-astar);
  background: rgba(255, 109, 0, 0.05);
}
</style>

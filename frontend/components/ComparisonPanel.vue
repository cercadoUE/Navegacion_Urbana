<template>
  <div class="comparison-panel glass-card">
    <h3 class="panel-title">Comparativa</h3>

    <div class="comparison-grid">
      <div class="algo-card dijkstra">
        <div class="algo-header">
          <span class="algo-dot" />
          <span class="algo-name">Dijkstra</span>
        </div>
        <div class="metric-list">
          <MetricRow label="Tiempo" :value="`${result.dijkstra.time_s}s`" small />
          <MetricRow label="Nodos explorados" :value="formatNum(result.dijkstra.nodes_explored)" small />
          <MetricRow label="Distancia" :value="`${result.dijkstra.distance_km.toFixed(2)} km`" small />
        </div>
      </div>

      <div class="algo-card astar">
        <div class="algo-header">
          <span class="algo-dot astar-dot" />
          <span class="algo-name">A*</span>
        </div>
        <div class="metric-list">
          <MetricRow label="Tiempo" :value="`${result.astar.time_s}s`" small />
          <MetricRow label="Nodos explorados" :value="formatNum(result.astar.nodes_explored)" small />
          <MetricRow label="Distancia" :value="`${result.astar.distance_km.toFixed(2)} km`" small />
        </div>
      </div>
    </div>

    <div class="speedup-section">
      <div class="speedup-row">
        <span class="speedup-label">Velocidad</span>
        <span class="speedup-value">
          {{ speedupTimes }}<small>x</small>
        </span>
      </div>
      <div class="speedup-row">
        <span class="speedup-label">Nodos explorados</span>
        <span class="speedup-value">
          {{ speedupNodes }}<small>x menos</small>
        </span>
      </div>
    </div>

    <div class="bar-chart">
      <div class="bar-group">
        <span class="bar-label">Tiempo</span>
        <div class="bars">
          <div class="bar-wrapper">
            <div
              class="bar dijkstra-bar"
              :style="{ width: timePercentD + '%' }"
            >
              {{ result.dijkstra.time_s.toFixed(3) }}s
            </div>
          </div>
          <div class="bar-wrapper">
            <div
              class="bar astar-bar"
              :style="{ width: timePercentA + '%' }"
            >
              {{ result.astar.time_s.toFixed(3) }}s
            </div>
          </div>
        </div>
      </div>
      <div class="bar-group">
        <span class="bar-label">Nodos</span>
        <div class="bars">
          <div class="bar-wrapper">
            <div
              class="bar dijkstra-bar"
              :style="{ width: nodesPercentD + '%' }"
            >
              {{ formatNum(result.dijkstra.nodes_explored) }}
            </div>
          </div>
          <div class="bar-wrapper">
            <div
              class="bar astar-bar"
              :style="{ width: nodesPercentA + '%' }"
            >
              {{ formatNum(result.astar.nodes_explored) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { RouteResponse } from "~/types";

const props = defineProps<{
  result: RouteResponse;
}>();

const speedupTimes = computed(() => {
  const r = props.result;
  if (r.astar.time_s === 0) return "∞";
  return (r.dijkstra.time_s / r.astar.time_s).toFixed(1);
});

const speedupNodes = computed(() => {
  const r = props.result;
  if (r.astar.nodes_explored === 0) return "∞";
  return (r.dijkstra.nodes_explored / r.astar.nodes_explored).toFixed(1);
});

const timePercentD = computed(() => {
  const r = props.result;
  const max = Math.max(r.dijkstra.time_s, r.astar.time_s);
  return max > 0 ? (r.dijkstra.time_s / max) * 100 : 0;
});

const timePercentA = computed(() => {
  const r = props.result;
  const max = Math.max(r.dijkstra.time_s, r.astar.time_s);
  return max > 0 ? (r.astar.time_s / max) * 100 : 0;
});

const nodesPercentD = computed(() => {
  const r = props.result;
  const max = Math.max(r.dijkstra.nodes_explored, r.astar.nodes_explored);
  return max > 0 ? (r.dijkstra.nodes_explored / max) * 100 : 0;
});

const nodesPercentA = computed(() => {
  const r = props.result;
  const max = Math.max(r.dijkstra.nodes_explored, r.astar.nodes_explored);
  return max > 0 ? (r.astar.nodes_explored / max) * 100 : 0;
});

function formatNum(n: number) {
  return n.toLocaleString();
}
</script>

<style scoped>
.comparison-panel {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.panel-title {
  font-size: 13px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.comparison-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.algo-card {
  padding: 14px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.algo-card.dijkstra {
  background: rgba(0, 229, 255, 0.04);
  border-color: rgba(0, 229, 255, 0.12);
}

.algo-card.astar {
  background: rgba(255, 109, 0, 0.04);
  border-color: rgba(255, 109, 0, 0.12);
}

.algo-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.algo-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-cyan);
  box-shadow: 0 0 8px var(--accent-cyan);
}

.algo-dot.astar-dot {
  background: var(--accent-astar);
  box-shadow: 0 0 8px var(--accent-astar);
}

.algo-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.metric-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.speedup-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 14px;
  background: rgba(0, 229, 255, 0.04);
  border: 1px solid rgba(0, 229, 255, 0.1);
  border-radius: 12px;
}

.speedup-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.speedup-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.speedup-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--accent-cyan);
}

.speedup-value small {
  font-size: 13px;
  font-weight: 400;
  opacity: 0.7;
}

.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.bar-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.bar-label {
  font-size: 11px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.bars {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.bar-wrapper {
  height: 24px;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 6px;
  overflow: hidden;
}

.bar {
  height: 100%;
  border-radius: 6px;
  display: flex;
  align-items: center;
  padding: 0 8px;
  font-size: 11px;
  font-weight: 600;
  color: #000;
  white-space: nowrap;
  transition: width 0.6s ease;
  min-width: fit-content;
}

.dijkstra-bar {
  background: linear-gradient(90deg, var(--accent-cyan), #00b0ff);
}

.astar-bar {
  background: linear-gradient(90deg, var(--accent-astar), #ff9100);
}
</style>

<template>
  <div class="viz-container">
    <div class="viz-controls">
      <button class="viz-btn" :disabled="!canStart || animating" @click="startViz">
        <span class="btn-icon">&#9654;</span> Iniciar
      </button>
      <button class="viz-btn" :disabled="!animating" @click="pauseViz">
        <span class="btn-icon">&#10074;&#10074;</span> Pausar
      </button>
      <button class="viz-btn" :disabled="!hasData" @click="resetViz">
        <span class="btn-icon">&#8635;</span> Reiniciar
      </button>
      <div class="speed-control">
        <label>Velocidad</label>
        <input type="range" min="10" max="200" v-model.number="speed" class="speed-slider" />
        <span class="speed-label">{{ speed }}ms</span>
      </div>
      <div class="viz-status" v-if="!hasData && !loading && canStart">
        Presiona Iniciar para visualizar
      </div>
      <div class="viz-status loading" v-if="loading">
        <div class="spinner-sm" />
        Calculando...
      </div>
      <div class="viz-status" v-if="!canStart && !loading">
        Selecciona origen y destino en Home
      </div>
    </div>

    <div class="viz-progress">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: overallProgress + '%', background: overallProgress < 100 ? 'var(--accent-cyan)' : '#00e676' }" />
      </div>
      <div class="progress-labels">
        <span style="color:#00e5ff">Dijkstra: {{ Math.round(progressD * 100) }}%</span>
        <span style="color:#ff6d00">A*: {{ Math.round(progressA * 100) }}%</span>
      </div>
    </div>

    <div class="viz-maps">
      <div class="viz-map-wrapper">
        <div class="viz-map-header" style="background:#006064">
          <span class="algo-badge">DIJKSTRA</span>
          <span v-if="metricsD" class="algo-metrics">{{ metricsD.nodes_explored }} nodos · {{ metricsD.time_s }}s</span>
        </div>
        <div class="viz-map-body">
          <AnimationMap ref="mapD" color="#00e5ff" :visited="data?.dijkstra.visited ?? []" :path="data?.dijkstra.path ?? []" :origin="origin" :dest="dest" @animation-end="onDijkstraEnd" @animation-progress="(p: number) => progressD = p" />
        </div>
      </div>
      <div class="viz-map-wrapper">
        <div class="viz-map-header" style="background:#bf360c">
          <span class="algo-badge">A*</span>
          <span v-if="metricsA" class="algo-metrics">{{ metricsA.nodes_explored }} nodos · {{ metricsA.time_s }}s</span>
        </div>
        <div class="viz-map-body">
          <AnimationMap ref="mapA" color="#ff6d00" :visited="data?.astar.visited ?? []" :path="data?.astar.path ?? []" :origin="origin" :dest="dest" @animation-end="onAstarEnd" @animation-progress="(p: number) => progressA = p" />
        </div>
      </div>
    </div>

    <div v-if="dDone && aDone && hasData" class="viz-complete">
      <span>&#10003; A* fue {{ speedup }}x más rápido que Dijkstra</span>
    </div>
    <div v-if="error" class="viz-error">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import type { LatLng, VisualizeResponse } from "~/types";
import { useApi } from "~/composables/useApi";

const props = defineProps<{
  origin: LatLng | null;
  dest: LatLng | null;
}>();

const { visualizeRoute } = useApi();

const data = ref<VisualizeResponse | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);
const animating = ref(false);
const speed = ref(50);
const progressD = ref(0);
const progressA = ref(0);
const dDone = ref(false);
const aDone = ref(false);

const mapD = ref<any>(null);
const mapA = ref<any>(null);

const metricsD = computed(() => data.value?.dijkstra ?? null);
const metricsA = computed(() => data.value?.astar ?? null);
const hasData = computed(() => data.value !== null);
const canStart = computed(() => props.origin !== null && props.dest !== null);
const overallProgress = computed(() => (progressD.value + progressA.value) * 50);
const speedup = computed(() => {
  if (!data.value) return "—";
  return (data.value.dijkstra.time_s / data.value.astar.time_s).toFixed(1);
});

watch([() => props.origin, () => props.dest], async ([o, d]) => {
  resetViz();
  data.value = null;
  error.value = null;
  if (o && d) {
    loading.value = true;
    try {
      data.value = await visualizeRoute(o.lat, o.lon, d.lat, d.lon);
    } catch (e) {
      error.value = "Error al obtener datos";
    } finally {
      loading.value = false;
    }
  }
}, { immediate: true });

function startViz() {
  if (!data.value) return;
  dDone.value = false;
  aDone.value = false;
  progressD.value = 0;
  progressA.value = 0;
  animating.value = true;
  mapD.value?.startAnimation(speed.value);
  mapA.value?.startAnimation(speed.value);
}

function pauseViz() {
  animating.value = false;
  mapD.value?.pauseAnimation();
  mapA.value?.pauseAnimation();
}

function resetViz() {
  animating.value = false;
  dDone.value = false;
  aDone.value = false;
  progressD.value = 0;
  progressA.value = 0;
  mapD.value?.resetAnimation();
  mapA.value?.resetAnimation();
}

function onDijkstraEnd() {
  dDone.value = true;
  progressD.value = 1;
  if (dDone.value && aDone.value) animating.value = false;
}

function onAstarEnd() {
  aDone.value = true;
  progressA.value = 1;
  if (dDone.value && aDone.value) animating.value = false;
}

watch(speed, () => {
  if (animating.value) { pauseViz(); startViz(); }
});
</script>

<style scoped>
.viz-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  background: var(--bg-primary);
}

.viz-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-glow);
  z-index: 100;
  flex-wrap: wrap;
}

.viz-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  border: 1px solid var(--border-glow);
  border-radius: 8px;
  background: var(--bg-card);
  color: var(--text-primary);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}
.viz-btn:hover:not(:disabled) { background: rgba(0,229,255,0.1); border-color: var(--accent-cyan); }
.viz-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-icon { font-size: 11px; }

.speed-control {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: var(--text-secondary);
}
.speed-slider { width: 70px; accent-color: var(--accent-cyan); }
.speed-label { font-size: 11px; color: var(--text-secondary); min-width: 32px; }

.viz-status {
  font-size: 11px;
  color: var(--text-secondary);
  margin-left: auto;
}
.viz-status.loading {
  color: var(--accent-cyan);
  display: flex;
  align-items: center;
  gap: 6px;
}
.spinner-sm {
  width: 12px; height: 12px;
  border: 2px solid var(--border-glow);
  border-top-color: var(--accent-cyan);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.viz-progress {
  padding: 4px 16px 0;
}
.progress-bar {
  height: 3px;
  background: rgba(255,255,255,0.08);
  border-radius: 2px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s;
}
.progress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 9px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.viz-maps {
  flex: 1;
  display: flex;
  gap: 0;
  min-height: 0;
}

.viz-map-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border-glow);
}
.viz-map-wrapper:last-child { border-right: none; }

.viz-map-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 5px 12px;
}
.algo-badge {
  font-size: 11px;
  font-weight: 700;
  color: white;
  letter-spacing: 1px;
}
.algo-metrics {
  font-size: 10px;
  color: rgba(255,255,255,0.7);
}

.viz-map-body {
  flex: 1;
  min-height: 0;
}

.viz-complete {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  padding: 6px 16px;
  background: rgba(0,230,118,0.15);
  border: 1px solid rgba(0,230,118,0.3);
  border-radius: 8px;
  color: #00e676;
  font-size: 12px;
  font-weight: 600;
  z-index: 1000;
  pointer-events: none;
}

.viz-error {
  padding: 6px 16px;
  background: rgba(255,0,0,0.1);
  color: #ff5252;
  font-size: 11px;
  text-align: center;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>

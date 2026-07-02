<template>
  <ClientOnly>
    <div ref="mapContainer" class="anim-map-container" />
    <template #fallback>
      <div class="anim-loading"><div class="spinner" /><span>Cargando mapa...</span></div>
    </template>
  </ClientOnly>
</template>

<script setup lang="ts">
import type { LatLng } from "~/types";

const props = defineProps<{
  label: string;
  color: string;
  visited: LatLng[];
  path: LatLng[];
  origin?: LatLng | null;
  dest?: LatLng | null;
}>();

const emit = defineEmits<{
  "animation-end": [];
  "animation-progress": [fraction: number];
}>();

const mapContainer = ref<HTMLDivElement>();
const map = ref<any>(null);
const visitedLayer = ref<any>(null);
const pathLayer = ref<any>(null);
const markerLayer = ref<any>(null);
const animInterval = ref<ReturnType<typeof setInterval> | null>(null);
const currentIndex = ref(0);

const DARK_TILES = "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png";

function createIcon(color: string, label: string) {
  const L = (window as any).L;
  return L.divIcon({
    className: "custom-marker",
    html: `<div style="width:24px;height:24px;background:${color};border:2px solid white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;color:white;box-shadow:0 0 12px ${color}80;">${label}</div>`,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  });
}

onMounted(async () => {
  const L = await import("leaflet");
  (window as any).L = L.default || L;

  map.value = L.map(mapContainer.value!, {
    center: [-12.121, -77.03],
    zoom: 14,
    zoomControl: true,
    attributionControl: false,
  });

  L.tileLayer(DARK_TILES, {
    maxZoom: 19,
    attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>',
  }).addTo(map.value);

  visitedLayer.value = L.layerGroup().addTo(map.value);
  pathLayer.value = L.layerGroup().addTo(map.value);
  markerLayer.value = L.layerGroup().addTo(map.value);

  if (props.origin) addMarker(props.origin, "#00e5ff", "O");
  if (props.dest) addMarker(props.dest, "#ff6d00", "D");
});

function resetAnimation() {
  currentIndex.value = 0;
  if (animInterval.value) {
    clearInterval(animInterval.value);
    animInterval.value = null;
  }
  visitedLayer.value?.clearLayers();
  markerLayer.value?.clearLayers();
  pathLayer.value?.clearLayers();
}

function startAnimation(speed: number = 50) {
  resetAnimation();
  if (!props.visited || props.visited.length === 0) return;

  if (props.origin) {
    addMarker(props.origin, "#00e5ff", "O");
  }
  if (props.dest) {
    addMarker(props.dest, "#ff6d00", "D");
  }

  const L = (window as any).L;
  const batchSize = Math.max(1, Math.floor(props.visited.length / 200));

  animInterval.value = setInterval(() => {
    const end = Math.min(currentIndex.value + batchSize, props.visited.length);
    for (let i = currentIndex.value; i < end; i++) {
      const p = props.visited[i];
      const circle = L.circleMarker([p.lat, p.lon], {
        radius: 2.5,
        color: props.color,
        fillColor: props.color,
        fillOpacity: 0.7,
        opacity: 0.5,
        weight: 1,
      });
      visitedLayer.value.addLayer(circle);
    }
    currentIndex.value = end;
    emit("animation-progress", currentIndex.value / props.visited.length);

    if (currentIndex.value >= props.visited.length) {
      if (animInterval.value) {
        clearInterval(animInterval.value);
        animInterval.value = null;
      }
      drawPath();
      fitBounds();
      emit("animation-end");
    }
  }, speed);
}

function pauseAnimation() {
  if (animInterval.value) {
    clearInterval(animInterval.value);
    animInterval.value = null;
  }
}

function drawPath() {
  const L = (window as any).L;
  pathLayer.value.clearLayers();
  if (!props.path || props.path.length < 2) return;

  const coords = props.path.map((c) => [c.lat, c.lon]);
  const pl = L.polyline(coords, {
    color: props.color,
    weight: 4,
    opacity: 0.9,
    dashArray: props.color === "#ff6d00" ? "10, 6" : undefined,
  });
  pathLayer.value.addLayer(pl);
}

function fitBounds() {
  const L = (window as any).L;
  const all = [...props.visited, ...props.path];
  if (all.length) {
    const bounds = L.latLngBounds(all.map((c: any) => [c.lat, c.lon]));
    map.value.fitBounds(bounds, { padding: [40, 40] });
  }
}

function addMarker(p: LatLng, color: string, label: string) {
  const L = (window as any).L;
  const m = L.marker([p.lat, p.lon], { icon: createIcon(color, label) });
  markerLayer.value.addLayer(m);
}

function setProgress(fraction: number) {
  if (!props.visited || props.visited.length === 0) return;
  resetAnimation();
  if (fraction <= 0) return;

  if (props.origin) addMarker(props.origin, "#00e5ff", "O");
  if (props.dest) addMarker(props.dest, "#ff6d00", "D");

  const L = (window as any).L;
  const end = Math.floor(props.visited.length * fraction);
  for (let i = 0; i < end; i++) {
    const p = props.visited[i];
    const circle = L.circleMarker([p.lat, p.lon], {
      radius: 2.5,
      color: props.color,
      fillColor: props.color,
      fillOpacity: 0.7,
      opacity: 0.5,
      weight: 1,
    });
    visitedLayer.value.addLayer(circle);
  }
  currentIndex.value = end;

  if (fraction >= 1 && props.path) {
    drawPath();
    fitBounds();
    emit("animation-end");
  }
}

watch(() => [props.origin, props.dest], () => {
  markerLayer.value?.clearLayers();
  if (props.origin) addMarker(props.origin, "#00e5ff", "O");
  if (props.dest) addMarker(props.dest, "#ff6d00", "D");
}, { deep: true });

onUnmounted(() => {
  map.value?.remove();
});

defineExpose({ startAnimation, pauseAnimation, resetAnimation, setProgress });
</script>

<style scoped>
.anim-map-container {
  width: 100%;
  height: 100%;
  border-radius: 12px;
  overflow: hidden;
}
.anim-loading {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background: var(--bg-primary);
  color: var(--text-secondary);
  font-size: 13px;
}
.spinner {
  width: 20px; height: 20px;
  border: 2px solid var(--border-glow);
  border-top-color: var(--accent-cyan);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>

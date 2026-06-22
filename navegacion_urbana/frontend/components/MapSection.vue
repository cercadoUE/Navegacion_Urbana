<template>
  <ClientOnly>
    <div ref="mapContainer" class="map-container" />
    <template #fallback>
      <div class="map-loading">
        <div class="spinner" />
        <span>Cargando mapa...</span>
      </div>
    </template>
  </ClientOnly>
</template>

<script setup lang="ts">
import type { LatLng, RouteResponse } from "~/types";

const props = defineProps<{
  origin: LatLng | null;
  dest: LatLng | null;
  result: RouteResponse | null;
  loading: boolean;
}>();

const emit = defineEmits<{
  "set-origin": [p: LatLng];
  "set-dest": [p: LatLng];
}>();

const mapContainer = ref<HTMLDivElement>();
const map = ref<any>(null);
const markers = ref<any[]>([]);
const polylines = ref<any[]>([]);

const DARK_TILES = "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png";

function createIcon(color: string, label: string) {
  const L = (window as any).L;
  return L.divIcon({
    className: "custom-marker",
    html: `
      <div style="
        width: 28px; height: 28px;
        background: ${color};
        border: 2px solid white;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 12px; font-weight: 800; color: white;
        box-shadow: 0 0 16px ${color}80;
      ">${label}</div>
    `,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });
}

onMounted(async () => {
  const L = await import("leaflet");
  (window as any).L = L.default || L;

  map.value = L.map(mapContainer.value!, {
    center: [-12.121, -77.03],
    zoom: 15,
    zoomControl: true,
    attributionControl: true,
  });

  L.tileLayer(DARK_TILES, {
    maxZoom: 19,
    attribution:
      '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>',
  }).addTo(map.value);

  map.value.on("click", (e: any) => {
    const { lat, lng } = e.latlng;
    if (!props.origin) {
      emit("set-origin", { lat, lon: lng });
    } else if (!props.dest) {
      emit("set-dest", { lat, lon: lng });
    }
  });
});

watch(
  () => [props.origin, props.dest, props.result],
  () => {
    if (!map.value) return;
    clearLayers();
    const L = (window as any).L;

    if (props.origin) addMarker(props.origin, "#00e5ff", "O");
    if (props.dest) addMarker(props.dest, "#ff6d00", "D");

    if (props.result) {
      addRoute(props.result.dijkstra.path, "#00e5ff", "Dijkstra");
      addRoute(props.result.astar.path, "#ff6d00", "A*");

      const allCoords = [
        ...props.result.dijkstra.path,
        ...props.result.astar.path,
        props.result.origin,
        props.result.dest,
      ];
      if (allCoords.length) {
        const bounds = L.latLngBounds(
          allCoords.map((c: any) => [c.lat, c.lon])
        );
        map.value.fitBounds(bounds, { padding: [50, 50] });
      }
    }
  },
  { deep: true }
);

function addMarker(p: LatLng, color: string, label: string) {
  const L = (window as any).L;
  const m = L.marker([p.lat, p.lon], { icon: createIcon(color, label) }).addTo(
    map.value
  );
  markers.value.push(m);
}

function addRoute(path: LatLng[], color: string, label: string) {
  const L = (window as any).L;
  const coords = path.map((c) => [c.lat, c.lon]);
  const pl = L.polyline(coords, {
    color,
    weight: 4,
    opacity: 0.85,
    dashArray: color === "#ff6d00" ? "10, 6" : undefined,
  }).addTo(map.value);
  pl.bindPopup(`<strong>${label}</strong><br>${path.length} nodos`);
  polylines.value.push(pl);
}

function clearLayers() {
  markers.value.forEach((m: any) => m.remove());
  polylines.value.forEach((p: any) => p.remove());
  markers.value = [];
  polylines.value = [];
}

onUnmounted(() => {
  map.value?.remove();
});
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
}

.map-loading {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  background: var(--bg-primary);
  color: var(--text-secondary);
  font-size: 14px;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--border-glow);
  border-top-color: var(--accent-cyan);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>

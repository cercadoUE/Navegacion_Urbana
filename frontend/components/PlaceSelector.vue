<template>
  <div class="place-selector glass-card">
    <h3 class="selector-title">Ubicación</h3>

    <div class="select-row">
      <label class="select-label">Departamento</label>
      <select v-model="selectedDept" class="futuristic-select" @change="onDeptChange">
        <option value="" disabled>Seleccionar...</option>
        <option v-for="(districts, dept) in places" :key="dept" :value="dept">
          {{ dept }}
        </option>
      </select>
    </div>

    <div v-if="selectedDept" class="select-row">
      <label class="select-label">Distrito</label>
      <select v-model="selectedDistrict" class="futuristic-select">
        <option value="" disabled>Seleccionar...</option>
        <option v-for="d in currentDistricts" :key="d" :value="d">
          {{ formatDistrict(d) }}
        </option>
      </select>
    </div>

    <button
      class="load-btn"
      :disabled="!selectedDistrict || loading"
      @click="handleLoad"
    >
      <span v-if="loading" class="btn-spinner" />
      <span v-else class="btn-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
          <path d="M21 12a9 9 0 1 1-9-9" />
          <path d="M12 3v6h6" />
        </svg>
      </span>
      {{ loading ? 'Cargando...' : 'Cargar grafo' }}
    </button>

    <div v-if="currentCity" class="current-city">
      <span class="city-dot" />
      <span class="city-name">{{ formatDistrict(currentCity) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PlacesData } from "~/types";

const props = defineProps<{
  places: Record<string, string[]>;
  loading: boolean;
  currentCity: string | null;
}>();

const emit = defineEmits<{
  "load-graph": [place: string];
}>();

const selectedDept = ref("");
const selectedDistrict = ref("");

const currentDistricts = computed(() => {
  if (!selectedDept.value || !props.places[selectedDept.value]) return [];
  return props.places[selectedDept.value];
});

function onDeptChange() {
  selectedDistrict.value = "";
}

function handleLoad() {
  if (selectedDistrict.value) {
    emit("load-graph", selectedDistrict.value);
  }
}

function formatDistrict(d: string) {
  return d.replace(/, Peru$/, "").replace(/, (Lima|Peru)$/, "");
}

watch(() => props.currentCity, (city) => {
  if (city) {
    for (const [dept, districts] of Object.entries(props.places)) {
      for (const d of districts) {
        if (d === city) {
          selectedDept.value = dept;
          selectedDistrict.value = d;
          return;
        }
      }
    }
  }
});
</script>

<style scoped>
.place-selector {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.selector-title {
  font-size: 13px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.select-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.select-label {
  font-size: 11px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.futuristic-select {
  width: 100%;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(0, 229, 255, 0.15);
  border-radius: 10px;
  color: var(--text-primary);
  font-size: 13px;
  font-family: inherit;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2300e5ff' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  transition: border-color 0.2s;
}

.futuristic-select:focus {
  outline: none;
  border-color: var(--accent-cyan);
  box-shadow: 0 0 12px rgba(0, 229, 255, 0.15);
}

.futuristic-select option {
  background: #1a1a3a;
  color: var(--text-primary);
}

.load-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--accent-cyan), #0091ea);
  color: #000;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.load-btn:hover:not(:disabled) {
  box-shadow: 0 0 20px rgba(0, 229, 255, 0.3);
  transform: translateY(-1px);
}

.load-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0, 0, 0, 0.2);
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.btn-icon {
  display: flex;
}

.current-city {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: rgba(0, 229, 255, 0.06);
  border: 1px solid rgba(0, 229, 255, 0.1);
  border-radius: 8px;
}

.city-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00e676;
  box-shadow: 0 0 8px #00e676;
}

.city-name {
  font-size: 12px;
  color: var(--text-primary);
  font-weight: 500;
}
</style>

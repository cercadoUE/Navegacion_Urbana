<template>
  <div class="metric-row">
    <span class="metric-label">{{ label }}</span>
    <span class="metric-value" :class="{ small }">{{ value }}</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string;
  value: string;
  small?: boolean;
}>();
</script>

<style scoped>
.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.metric-label {
  font-size: 11px;
  color: var(--text-secondary);
}

.metric-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  font-family: "SF Mono", "Fira Code", monospace;
}

.metric-value.small {
  font-size: 12px;
}
</style>

<template>
  <export-btn
    label="Отчет текущие цены"
    type="current"
    filter-product
    filter-task
    filter-date-from
    filter-date-to
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import ExportBtn from './ExportBtn.vue'

</script>
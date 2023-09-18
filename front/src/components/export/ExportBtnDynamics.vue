<template>
  <export-btn
    label="Отчет динамика"
    type="dynamics"
    filter-product
    filter-task
    filter-date-from
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import ExportBtn from './ExportBtn.vue'

</script>
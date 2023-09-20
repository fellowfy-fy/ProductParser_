<template>
  <export-btn
    label="Отчет по отличиям"
    type="differences"
    filter-product
    filter-task
    filter-date-from
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import ExportBtn from './ExportBtn.vue'

</script>
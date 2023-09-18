<template>
  <q-page padding>
    <export-list>
      <export-btn-current />
      <export-btn-dynamics />
    </export-list>
  </q-page>
</template>

<script setup lang="ts">
import ExportList from '../../components/export/ExportList.vue'
import ExportBtnDynamics from '../../components/export/ExportBtnDynamics.vue'
import ExportBtnCurrent from '../../components/export/ExportBtnCurrent.vue'

</script>
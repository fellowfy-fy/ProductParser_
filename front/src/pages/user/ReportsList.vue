<template>
  <q-page padding>
    <export-list>
      <export-btn-current />
      <export-btn-dynamics />
      <export-btn-differences />
      <export-btn-variations />
      <export-btn-competitors />
    </export-list>
  </q-page>
</template>

<script setup lang="ts">
import ExportBtnDifferences from '../../components/export/ExportBtnDifferences.vue'
import ExportBtnVariations from '../../components/export/ExportBtnVariations.vue'
import ExportBtnCompetitors from '../../components/export/ExportBtnCompetitors.vue'
import ExportList from '../../components/export/ExportList.vue'
import ExportBtnDynamics from '../../components/export/ExportBtnDynamics.vue'
import ExportBtnCurrent from '../../components/export/ExportBtnCurrent.vue'

</script>
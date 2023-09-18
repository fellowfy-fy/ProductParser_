<template>
  <q-page padding>
    <div class="row column justify-start items-start q-gutter-y-md">
      <export-btn-current />
      <export-btn-dynamics />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import ExportBtnDynamics from '../../components/export/ExportBtnDynamics.vue'
import ExportBtnCurrent from '../../components/export/ExportBtnCurrent.vue'

</script>
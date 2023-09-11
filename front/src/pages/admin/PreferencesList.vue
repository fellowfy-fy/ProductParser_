<template>
  <q-page padding>
    <fast-table
      :columns="tableColumns"
      :data="data"
      :load="loadData"
      @row-click="onRowClick"
    />
  </q-page>
</template>

<script setup lang="ts">
import FastTable from '../../components/form/FastTable.vue'
import { computed } from 'vue';
import { QTableProps } from 'quasar';
import { GlobalPreference } from "src/client"
import { useRouter } from 'vue-router';
import { usePreferencesStore } from 'src/stores/preferences';

const router = useRouter()

const store = usePreferencesStore()

const data = computed(() => store.preferences)

const tableColumns = [
  {
    name: 'id',
    label: 'ID',
    field: 'identifier',
    required: true,
    sortable: true,
    style: 'width: 20px'
  },
  {
    name: 'verbose_name',
    label: 'Название',
    field: 'verbose_name',
    required: true,
    sortable: true,
  },
  {
    name: 'value',
    label: 'Значение',
    field: 'value',
    required: true,
    sortable: true,
  },
] as QTableProps["columns"]

function loadData(payload: object){
  const prom = store.loadPreferences(payload)
  return prom
}

function onRowClick(e, data: GlobalPreference){
  void router.push({
    name: 'admin_preference', params: {id: data.identifier}
  })
}

</script>
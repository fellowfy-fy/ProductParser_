<template>
  <q-page padding>
    <q-table
      v-model:pagination="tablePagination"
      title="Настройки"
      :rows="data || []"
      :columns="tableColumns"
      :loading="loading"
      :rows-per-page-options="[5, 10, 20, 50]"
      row-key="id"
      binary-state-sort
      flat
      bordered
      @request="onRequest"
      @row-click="onRowClick"
    >
      <template #top-right>
        <q-input
          v-model="filters.search"
          borderless
          dense
          debounce="300"
          placeholder="Поиск"
        >
          <template #append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
    </q-table>
  </q-page>
</template>

<script setup lang="ts">
import { Ref, computed, onMounted, ref, watch } from 'vue';
import { promiseSetLoading } from 'src/Modules/StoreCrud';
import { QTableProps } from 'quasar';
import { GlobalPreference } from "src/client"
import { useRouter } from 'vue-router';
import { usePreferencesStore } from 'src/stores/preferences';

const router = useRouter()

const store = usePreferencesStore()

const loading = ref(false)
const filters = ref({
  search: ''
})
const tablePagination:Ref<QTableProps["pagination"]> = ref({
  rowsPerPage: 20
})

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

function loadData(){
  const payload = {
    search: filters.value.search,
    page: tablePagination.value.page || 1,
    pageSize: tablePagination.value?.rowsPerPage || 20,
    ordering:  (tablePagination.value?.descending? '-':'')+String(tablePagination.value?.sortBy)
  }

  const prom = store.loadPreferences(payload)

  promiseSetLoading(prom, loading)
  void prom.then((resp) => {
    if (tablePagination.value){
      tablePagination.value.rowsNumber = resp.count
    }
  })
}


const onRequest = (data:{pagination: QTableProps["pagination"]}) => {
  tablePagination.value = data.pagination
  loadData()
}

function onRowClick(e, data: GlobalPreference){
  void router.push({
    name: 'admin_preference', params: {id: data.identifier}
  })
}



onMounted(() => {
  loadData()
})

watch(filters, () => {
  loadData()
}, {deep: true})

</script>
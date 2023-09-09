<template>
  <q-page padding>
    <q-card
      class="row q-mb-lg"
      flat
      bordered
    >
      <q-card-section>
        <q-btn
          label="Создать"
          color="positive"
          icon="add"
          size="sm"
          unelevated
          @click="onCreateNew"
        />
      </q-card-section>
    </q-card>

    <q-table
      v-model:pagination="tablePagination"
      title="Парсеры"
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
      <template #body-cell-is_active="props">
        <q-td>
          <q-badge
            v-if="props.value"
            color="positive"
          >
            Да
          </q-badge>
          <q-badge
            v-else
            color="negative"
          >
            Нет
          </q-badge>
        </q-td>
      </template>
    </q-table>
  </q-page>
</template>

<script setup lang="ts">
import { Ref, computed, onMounted, ref, watch } from 'vue';
import { promiseSetLoading } from 'src/Modules/StoreCrud';
import { QTableProps } from 'quasar';
import { ParseTask } from "src/client"
import { useRouter } from 'vue-router';
import { useTasksStore } from 'src/stores/tasks';

const router = useRouter()

const store = useTasksStore()

const loading = ref(false)
const filters = ref({
  search: ''
})
const tablePagination:Ref<QTableProps["pagination"]> = ref({})

const data = computed(() => store.parseSettings)

const tableColumns = [
  {
    name: 'id',
    label: 'ID',
    field: 'id',
    required: true,
    sortable: true,
    style: 'width: 20px'
  },
  {
    name: 'domain',
    label: 'Домен',
    field: 'domain',
    align: 'left',
    sortable: true,
  },
  // {
  //   name: 'created_at',
  //   label: 'Дата создания',
  //   field: 'created_at',
  //   format(val: string){
  //     return formatDateTime(val)
  //   },
  //   sortable: true,
  //   style: 'width:100px'
  // }
] as QTableProps["columns"]

function loadData(){
  const payload = {
    search: filters.value.search,
    page: tablePagination.value.page || 1,
    pageSize: tablePagination.value?.rowsPerPage || 20,
    ordering:  (tablePagination.value?.descending? '-':'')+String(tablePagination.value?.sortBy)
  }

  const prom = store.loadParseSettings(payload)

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

function onRowClick(e, data: ParseTask){
  void router.push({
    name: 'admin_parse_setting', params: {id: data.id}
  })
}

function onCreateNew(){
  void router.push({
    name: 'admin_parse_setting', params: {id: 'new'}
  })
}


onMounted(() => {
  loadData()
})

watch(filters, () => {
  loadData()
}, {deep: true})

</script>
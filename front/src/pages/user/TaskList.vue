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
      title="Задачи"
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
      <template #body-cell-status="props">
        <q-td>
          <task-status-badge :status="props.value" />
        </q-td>
      </template>
    </q-table>
  </q-page>
</template>

<script setup lang="ts">
import TaskStatusBadge from '../../components/task/TaskStatusBadge.vue'
import { Ref, computed, onMounted, ref, watch } from 'vue';
import { useTasksStore } from 'src/stores/tasks';
import { promiseSetLoading } from 'src/Modules/StoreCrud';
import { QTableProps } from 'quasar';
import { ParseTask, ShortUser } from "src/client"
import {formatDateTime} from 'src/Modules/utils'
import { useRouter } from 'vue-router';
import { TaskStatus, userReadable } from 'src/Modules/StaticTranslate';

const router = useRouter()

const store = useTasksStore()

const loading = ref(false)
const filters = ref({
  search: ''
})
const tablePagination:Ref<QTableProps["pagination"]> = ref({})

const data = computed(() => store.parseTasks)

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
    name: 'name',
    label: 'Название',
    field: 'name',
    align: 'left',
    sortable: true,
  },
  {
    name: 'status',
    label: 'Статус',
    field: 'status',
    align: 'left',
    // format(val:number) {
    //     return TaskStatus.get(val) || val
    // },
    sortable: true,
  },
  {
    name: 'author',
    label: 'Автор',
    field: 'author',
    align: 'left',
    format(val:ShortUser) {
        return userReadable(val)
    },
    sortable: true,
  },
  {
    name: 'created_at',
    label: 'Создан',
    field: 'created_at',
    format(val: string){
      return formatDateTime(val)
    },
    sortable: true,
    style: 'width:100px'
  }
] as QTableProps["columns"]

function loadData(){
  const payload = {
    search: filters.value.search,
    page: tablePagination.value.page || 1,
    pageSize: tablePagination.value?.rowsPerPage || 20,
    ordering:  (tablePagination.value?.descending? '-':'')+String(tablePagination.value?.sortBy)
  }

  const prom = store.loadParseTasks(payload)

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
    name: 'user_task', params: {id: data.id}
  })
}

function onCreateNew(){
  void router.push({
    name: 'user_task', params: {id: 'new'}
  })
}


onMounted(() => {
  loadData()
})

watch(filters, () => {
  loadData()
}, {deep: true})

</script>
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
      title="Пользователи"
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
import { promiseSetLoading } from 'src/modules/StoreCrud';
import { QTableProps } from 'quasar';
import { ParseTask, ShortUser } from "src/client"
import {formatDateTime} from 'src/modules/utils'
import { useRouter } from 'vue-router';
import { TaskStatus, userReadable } from 'src/modules/StaticTranslate';
import { useAuthStore } from 'src/stores/auth';

const router = useRouter()

const store = useAuthStore()

const loading = ref(false)
const filters = ref({
  search: ''
})
const tablePagination:Ref<QTableProps["pagination"]> = ref({})

const data = computed(() => store.users)

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
    name: 'username',
    label: 'Username',
    field: 'username',
    align: 'left',
    sortable: true,
  },
  {
    name: 'first_name',
    label: 'Имя',
    field: 'first_name',
    align: 'left',
    sortable: true,
  },
  {
    name: 'last_name',
    label: 'Фамилия',
    field: 'last_name',
    align: 'left',
    sortable: true,
  },
  {
    name: 'is_active',
    label: 'Активен',
    field: 'is_active',
    align: 'left',
    sortable: true,
  },
  {
    name: 'date_joined',
    label: 'Создан',
    field: 'date_joined',
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

  const prom = store.loadUsers(payload)

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
    name: 'admin_user', params: {id: data.id}
  })
}

function onCreateNew(){
  void router.push({
    name: 'admin_user', params: {id: 'new'}
  })
}


onMounted(() => {
  loadData()
})

watch(filters, () => {
  loadData()
}, {deep: true})

</script>
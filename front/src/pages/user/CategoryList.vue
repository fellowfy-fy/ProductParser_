<template>
  <q-page padding>
    <q-card
      class="row q-mb-lg"
      flat
      bordered
    >
      <q-card-section>
        <q-btn
          label="Создать новую"
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
      title="Категории"
      :rows="categories || []"
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
import { useProductsStore } from 'src/stores/products';
import { promiseSetLoading } from 'src/modules/StoreCrud';
import { QTableProps } from 'quasar';
import { Category } from "src/client"
import {formatDateTime} from 'src/modules/Utils'
import { useRouter } from 'vue-router';

const $router = useRouter()

const store = useProductsStore()

const loading = ref(false)
const filters = ref({
  search: ''
})
const tablePagination:Ref<QTableProps["pagination"]> = ref({})

const categories = computed(() => store.categories)

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
    name: 'created_at',
    label: 'Дата создания',
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
    page: tablePagination.value?.page || 1,
    pageSize: tablePagination.value?.rowsPerPage || 20,
    ordering:  (tablePagination.value?.descending? '-':'')+String(tablePagination.value?.sortBy)
  }

  const prom = store.loadCategories(payload)

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

function onRowClick(e, data: Category){
  void $router.push({
    name: 'user_category', params: {id: data.id}
  })
}

function onCreateNew(){
  void $router.push({
    name: 'user_category', params: {id: 'new'}
  })
}


onMounted(() => {
  loadData()
})

watch(filters, () => {
  loadData()
}, {deep: true})

</script>
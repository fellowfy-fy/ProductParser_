<template>
  <q-page padding>
    <q-card
      class="row q-mb-lg"
      flat
      bordered
    >
      <q-card-section>
        <q-btn
          label="Создать новый"
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
      title="Продукты"
      :rows="products || []"
      :columns="tableColumns"
      :loading="loading"
      :rows-per-page-options="[5, 10, 20, 50]"
      row-key="id"
      binary-state-sort
      flat
      bordered
      @request="onRequest"
      @row-click="onRowClick"
    />
  </q-page>
</template>

<script setup lang="ts">
import { Ref, computed, onMounted, ref, watch } from 'vue';
import { useProductsStore } from 'src/stores/products';
import { promiseSetLoading } from 'src/modules/StoreCrud';
import { QTableProps } from 'quasar';
import { Product } from "src/client"
import {formatDateTime} from 'src/modules/utils'
import { useRouter } from 'vue-router';

const $router = useRouter()

const store = useProductsStore()

const loading = ref(false)
const filters = ref({
  search: ''
})
const tablePagination:Ref<QTableProps["pagination"]> = ref({})

const products = computed(() => store.products)

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
    name: 'price',
    label: 'Цена',
    field: 'price',
    format(val: string) {
        return `${val.toLocaleString()}₽`
    },
    align: 'left',
    sortable: true,
    style: 'width:80px'
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

  const prom = store.loadProducts(payload)

  promiseSetLoading(prom, loading)
  void prom.then((resp) => {
    if (tablePagination.value){
      tablePagination.value.rowsNumber = resp.count
    }
  })
}


const onRequest = (data:{pagination: QTableProps["pagination"]}) => {
  console.debug("Pagination: ", data)
  tablePagination.value = data.pagination
  loadData()
}

function onRowClick(e, data: Product){
  void $router.push({
    name: 'user_product', params: {id: data.id}
  })
}

function onCreateNew(){
  void $router.push({
    name: 'user_product', params: {id: 'new'}
  })
}


onMounted(() => {
  loadData()
})

watch(filters, () => {
  loadData()
}, {deep: true})

</script>
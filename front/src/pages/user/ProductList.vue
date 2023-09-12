<template>
  <q-page padding>
    <q-card
      class="row q-mb-lg"
      flat
      bordered
    >
      <q-card-section class="row q-gutter-sm">
        <q-btn
          label="Создать"
          color="positive"
          icon="add"
          size="sm"
          unelevated
          @click="onCreateNew"
        />
        <products-import @update="loadData()" />
      </q-card-section>
    </q-card>

    <fast-table
      :filters="filters"
      title="Товары"
      :columns="tableColumns"
      :data="data"
      :load="loadData"
      :default-pagination="{sortBy: 'created_at',descending: true}"
      @row-click="onRowClick"
      @reset-filters="resetFilters()"
    >
      <template #filters>
        <user-select
          v-model="filters.author"
          label="Автор"
          :preload="false"
          dense
          clearable
        />
        <category-select
          v-model="filters.categories"
          :preload="false"
          dense
          clearable
        />
      </template>
    </fast-table>
  </q-page>
</template>

<script setup lang="ts">
import CategorySelect from '../../components/select/CategorySelect.vue'
import UserSelect from '../../components/select/UserSelect.vue'
import FastTable from '../../components/form/FastTable.vue'
import ProductsImport from '../../components/products/ProductsImport.vue'
import { computed, ref } from 'vue';
import { useProductsStore } from 'src/stores/products';
import { QTableProps } from 'quasar';
import { Product, CategoryShort } from "src/client"
import {formatDateTime} from 'src/Modules/Utils'
import { useRouter } from 'vue-router';

const $router = useRouter()

const store = useProductsStore()
const data = computed(() => store.products)

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
    name: 'categories',
    label: 'Категории',
    field: 'categories',
    format(val: CategoryShort[]) {
        return val.map((c) =>c.name).join(", ")
    },
    align: 'left',
    sortable: true,
    style: 'width:80px'
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

const defaultFilters = {
  author: null as number[] | null,
  categories: null as number[] | null,
}

const filters = ref(defaultFilters)

function resetFilters(){
  filters.value = defaultFilters
}

function loadData(payload: object){
  const prom = store.loadProducts(payload)
  return prom
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

</script>
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
      title="Товары"
      :table-columns="tableColumns"
      :data="data"
      :load="loadData"
      :default-pagination="{sortBy: 'created_at',descending: true}"
      @row-click="onRowClick"
    />
  </q-page>
</template>

<script setup lang="ts">
import FastTable from '../../components/form/FastTable.vue'
import ProductsImport from '../../components/products/ProductsImport.vue'
import { computed } from 'vue';
import { useProductsStore } from 'src/stores/products';
import { QTableProps } from 'quasar';
import { Product } from "src/client"
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
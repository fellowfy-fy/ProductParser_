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

    <fast-table
      title="Категории"
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
import { useProductsStore } from 'src/stores/products';
import { QTableProps } from 'quasar';
import { Category } from "src/client"
import {formatDateTime} from 'src/Modules/Utils'
import { useRouter } from 'vue-router';

const $router = useRouter()

const store = useProductsStore()
const data = computed(() => store.categories)

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

function loadData(payload: object){
  const prom = store.loadCategories(payload)
  return prom
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


</script>
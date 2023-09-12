<template>
  <q-page padding>
    <fast-table
      :filters="filters"
      title="История цен"
      :columns="tableColumns"
      :data="data"
      :load="loadData"
      :default-pagination="{sortBy: 'created_at',descending: true}"
      @reset-filters="resetFilters()"
    >
      <template #filters>
        <product-select
          v-model="filters.product"
          label="Товар"
          dense
          clearable
        />
        <parse-task-select
          v-model="filters.task"
          label="Задача"
          dense
          clearable
        />
        <parse-settings-select
          v-model="filters.parseSettings"
          label="Настройки"
          dense
          clearable
        />
        <!-- <user-select
          v-model="filters.author"
          label="Автор"
          :preload="false"
          dense
          clearable
        /> -->
      </template>
    </fast-table>
  </q-page>
</template>

<script setup lang="ts">
import ParseSettingsSelect from '../../components/select/ParseSettingsSelect.vue'
import ParseTaskSelect from '../../components/select/ParseTaskSelect.vue'
import ProductSelect from '../../components/select/ProductSelect.vue'
import FastTable from '../../components/form/FastTable.vue'
import { computed, ref } from 'vue';
import { ProductShort, ParseTaskShort, SiteParseSettingsShort } from 'src/client';
import { useProductsStore } from 'src/stores/products';
import { QTableProps } from 'quasar';
import {formatDateTime} from 'src/Modules/Utils'
import { useRouter } from 'vue-router';

const $router = useRouter()

const store = useProductsStore()
const data = computed(() => store.price_history)

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
    name: 'product',
    label: 'Продукт',
    field: 'product',
    format(val: ProductShort) {
        return val.name
    },
    align: 'left',
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
    name: 'task',
    label: 'Задача',
    field: 'task',
    format(val: ParseTaskShort) {
        return val?.name || '-'
    },
    align: 'left',
  },
  {
    name: 'settings',
    label: 'Настройки',
    field: 'parse_settings',
    format(val: SiteParseSettingsShort) {
        return val?.domain || '-'
    },
    align: 'left',
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
  product: null as number[] | null,
  task: null as number[] | null,
  parseSettings: null as number[] | null,
}

const filters = ref(defaultFilters)

function resetFilters(){
  filters.value = defaultFilters
}

function loadData(payload: object){
  const prom = store.loadPriceHistory(payload)
  return prom
}
</script>
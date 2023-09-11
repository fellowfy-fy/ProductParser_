<template>
  <q-table
    v-model:pagination="tablePagination"
    title="Настройки"
    :rows="data || []"
    :columns="columns"
    :loading="isLoading"
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
        v-model="search"
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
    <template
      v-for="(index, name) in $slots"
      #[name]="data"
    >
      <slot
        :name="name"
        v-bind="data"
      />
    </template>
  </q-table>
</template>

<script setup lang="ts">
import { QTableProps } from 'quasar';
import { promiseSetLoading } from 'src/Modules/StoreCrud';
import { PropType, Ref, computed, onMounted, ref, watch } from 'vue';


export type LoadFunction = (payload: object) => Promise<DRFResponse>

export interface DRFResponse {
  count?:number
  total_pages?:number
  results?: Array<object>
}

const props = defineProps({
  columns: {
    type: Object as PropType<QTableProps["columns"]>,
    required: true,
  },
  data: {
    type: Array,
    required: false,
    default: null,
  },
  load:{
    type: Function as PropType<LoadFunction>,
      required: false,
      default: null,
  },
  filters: {
    type: Object,
    default: null,
  },
  defaultPagination: {
    type: Object as PropType<QTableProps["pagination"]>,
    default: null,
  }
})

const emit = defineEmits(['row-click'])

const tablePagination:Ref<QTableProps["pagination"]> = ref({
  rowsPerPage: 20,
})
if (props.defaultPagination){
  Object.assign(tablePagination.value, props.defaultPagination)
}


const isLoading = ref(false)
const search = ref('')

const payload = computed(() => {
  const res = {
    search: search.value,
    page: tablePagination.value?.page || 1,
    pageSize: tablePagination.value?.rowsPerPage || 20,
    ordering:  (tablePagination.value?.descending? '-':'')+String(tablePagination.value?.sortBy)
  }
  if (props.filters){
    Object.assign(res, props.filters)
  }
  return res
})

function onRowClick(e, data: object){
  emit('row-click', e,data)
}

function loadData(){
  const prom = props.load(payload.value)
  promiseSetLoading(prom, isLoading)
  void prom.then((resp: DRFResponse) => {
    const count = resp.count
    if (tablePagination.value){
      tablePagination.value.rowsNumber = count
    }
  })
}

function onRequest(data:{pagination: QTableProps["pagination"]}){
  console.debug("FastTable - onRequest")
  tablePagination.value = data.pagination
  loadData()
}

onMounted(() => {
  if (!props.data){
    loadData()
  }
})

// watch(filters, () => {
//   loadData()
// }, {deep: true})

watch(search, () => loadData())

</script>
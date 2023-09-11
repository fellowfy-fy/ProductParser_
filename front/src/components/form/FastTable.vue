<template>
  <div class="row q-col-gutter-md wrap no-wrap-lg">
    <div class="col-grow">
      <q-table
        v-model:pagination="tablePagination"
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
        <template #top-right v-if="enableSearch">
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
          <q-btn
            v-if="isEnableFilters"
            label="Фильтры"
            class="q-ml-md btn-filters"
            color="primary"
            size="sm"
            icon="filter_alt"
            unelevated
            dense
            @click="showFilters = !showFilters"
          />
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
    </div>


    <transition
        appear
        enter-active-class="animated slideInRight"
        leave-active-class="animated slideOutRight"
      >
    <div
      v-if="isEnableFilters && showFilters"
      class="col-grow filters-wrapper"
    >
      <q-card
        flat
        bordered
      >
        <q-card-section>
          <slot name="filters_title">
            <h6 class="text-center q-my-sm">
              Фильтры
            </h6>
          </slot>


          <div class="q-gutter-y-md">
            <slot name="filters" />
          </div>
        </q-card-section>
        <q-card-actions align="around">
          <!-- <q-btn
            label="Поиск"
            icon="search"
            color="primary"
            size="sm"
            unelevated
            no-caps
          /> -->
          <q-btn
            type="reset"
            label="Сбросить"
            icon="delete"
            color="negative"
            size="sm"
            unelevated
            no-caps
            @click="resetFilters"
          />
        </q-card-actions>
      </q-card>
    </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { useLocalStorage } from '@vueuse/core';
import { QTableProps } from 'quasar';
import { promiseSetLoading } from 'src/Modules/StoreCrud';
import { PropType, Ref, computed, onMounted, ref, useSlots, watch } from 'vue';


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
  },
  alwaysInit: {
    type: Boolean,
    default: true,
  },
  enableFilters: {
    type: Boolean,
    default: true,
  },
  enableSearch: {
    type: Boolean,
    default: true,
  }
})

const slots = useSlots()

const emit = defineEmits(['row-click', 'reset-filters'])

const tablePagination:Ref<QTableProps["pagination"]> = ref({
  rowsPerPage: 20,
})
if (props.defaultPagination){
  Object.assign(tablePagination.value, props.defaultPagination)
}


const isLoading = ref(false)
const search = ref('')
const showFilters = useLocalStorage('showFilters', false)
const isEnableFilters = computed(() => props.enableFilters && Object.hasOwn(slots, "filters"))

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

function resetFilters(){
  emit('reset-filters')
}

function onRowClick(e, data: object){
  emit('row-click', e,data)
}

function loadData(){
  console.debug("Loading data... ", {payload: payload.value})

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
  if (!props.data || props.alwaysInit){
    loadData()
  }
})

watch(props.filters, () => {
  loadData()
}, {deep: true})

watch(search, () => loadData())

</script>

<style lang="scss" scoped>
.filters-wrapper{
  max-width: 300px;
}
</style>
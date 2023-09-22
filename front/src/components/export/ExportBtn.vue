<template>
  <base-dialog
    v-model="showModal"
    :title="label"
    no-backdrop-dismiss
  >
    <q-form
      class="q-gutter-y-md"
      @submit="generateExport()"
    >
      <template v-if="props.filterProduct">
        <products-select
          v-model="filters.products"
          :disable="Boolean(filters.task)"
          dense
          label="Товары"
          clearable
          emit-value
        />
      </template>
      <template v-if="props.filterTask">
        <task-select
          v-model="filters.task"
          :disable="Boolean(filters.products && filters.products.length>0)"
          dense
          label="Задача"
          clearable
        />
      </template>
      <template v-if="props.filterDateFrom && props.filterDateTo">
        <div class="text-center">
          <q-date
            v-model="filterDate"
            mask="YYYY-MM-DD"
            range
            flat
            bordered
          />
        </div>
      </template>
      <template v-else-if="props.filterDateFrom">
        <q-input
          v-model="filters.date_from"
          mask="YYYY-MM-DD"
          type="date"
          dense
          label="Дата отчета"
          outlined
        />
      </template>
      <template v-else-if="props.filterDateTo">
        <q-input
          v-model="filters.date_to"
          mask="YYYY-MM-DD"
          type="date"
          dense
          label="Дата 'до' отчета"
          outlined
        />
      </template>

      <div class="q-mt-md">
        <q-btn
          type="submit"
          label="Создать отчет"
          color="primary"
          no-caps
          :loading="loading"
        />
      </div>
    </q-form>
  </base-dialog>
  <q-btn
    :label="label"
    color="secondary"
    no-caps
    v-bind="$attrs"
    @click="showModal = true"
  />
</template>

<script setup lang="ts">
import ProductsSelect from '../select/ProductsSelect.vue'
import TaskSelect from '../select/TaskSelect.vue'
import ProductSelect from '../select/ProductSelect.vue'
import BaseDialog from '../common/BaseDialog.vue'
import { date, useQuasar } from "quasar"
import { notifySuccess } from "src/Modules/Notif"
import { promiseSetLoading } from "src/Modules/StoreCrud"
import { ExportRequest, TypeEnum } from "src/client"
import { useTasksStore } from "src/stores/tasks"
import { PropType, computed, onMounted, ref, watch } from "vue"

const props = defineProps({
  type: {
    type: String as PropType<TypeEnum>,
    default: TypeEnum.CURRENT,
  },
  label: {
    type: String,
    default: "Отчет",
  },
  filterTask: {
    type: Boolean,
    default: false,
  },
  filterProduct: {
    type: Boolean,
    default: false,
  },
  filterDateFrom: {
    type: Boolean,
    default: false,
  },
  filterDateTo: {
    type: Boolean,
    default: false,
  },
  preset: {
    type: Object,
    default: null,
  }
})

const $q = useQuasar()
const store = useTasksStore()

const loading = ref(false)
const showModal = ref(false)

const defaultFilters = {
  products: [],
  task: null,
  date_from: null as Date | null,
  date_to: null as Date | null,
}

const filters = ref(defaultFilters)

const filterDate = computed({
  get(){
  return {
    from: filters.value.date_from,
    to: filters.value.date_to
  }
}, set(val: {from: Date, to: Date}){
  filters.value.date_from = val.from
  filters.value.date_to = val.to
}})

const defaultYearMonth = computed(() => {
  return date.formatDate(new Date(), "YYYY.mm")
})


function generateExport() {
  const payload: ExportRequest = Object.assign({
    type: props.type,
  }, filters.value)

  $q.loading.show({
    message: "Генерация отчета...",
  })
  const prom = store.generateExport(payload)
  promiseSetLoading(prom, loading)


  void prom.then((resp) => {
    window.open(resp.path, '_blank');
    notifySuccess("Отчет успешно сгенерирован")

    // showModal.value = false;
  })

  prom.finally(() => {
    $q.loading.hide()
  })
}

function checkPreset(){
  filters.value = Object.assign({}, defaultFilters, props.preset)
}

onMounted(() => {
  checkPreset()
})

watch(showModal, (val) => {
  if (val){
    checkPreset()
  }
})
</script>

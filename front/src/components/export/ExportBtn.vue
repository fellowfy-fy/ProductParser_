<template>
  <base-dialog
    v-model="showModal"
    :title="label"
  >
    <q-form
      class="q-gutter-y-md"
      @submit="generateExport()"
    >
      <template v-if="props.filterProduct">
        <product-select
          v-model="filters.product"
          :disable="Boolean(filters.task)"
          dense
          label="Товар"
          clearable
        />
      </template>
      <template v-if="props.filterTask">
        <task-select
          v-model="filters.task"
          :disable="Boolean(filters.product)"
          dense
          label="Задача"
          clearable
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
import TaskSelect from '../select/TaskSelect.vue'
import ProductSelect from '../select/ProductSelect.vue'
import BaseDialog from '../common/BaseDialog.vue'
import { useQuasar } from "quasar"
import { notifySuccess } from "src/Modules/Notif"
import { promiseSetLoading } from "src/Modules/StoreCrud"
import { ExportRequest, TypeEnum } from "src/client"
import { useTasksStore } from "src/stores/tasks"
import { PropType, onMounted, ref, watch } from "vue"

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
  product: null,
  task: null,
  date_from: null,
  date_to: null,
}

const filters = ref(defaultFilters)


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

    showModal.value = false;
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

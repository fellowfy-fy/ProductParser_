<template>
  <q-page padding>
    <back-btn />

    <!-- <h4 class="q-my-sm q-mb-xl">
      {{ product?.name }}
    </h4> -->

    <base-form
      v-if="item"
      @submit="saveData"
    >
      <template #info>
        <q-input
          :model-value="TaskStatus.get(item.status) || item.status"
          label="Статус"
          outlined
          readonly
          dense
        />
        <q-input
          :model-value="userReadable(item.author)"
          label="Автор"
          outlined
          readonly
          dense
        />


        <q-input
          :model-value="formatDateTime(item.created_at)"
          label="Дата создания"
          outlined
          readonly
          dense
        />
        <q-input
          :model-value="formatDateTime(item.updated_at)"
          label="Дата редактирования"
          outlined
          readonly
          dense
        />
      </template>
      <q-input
        v-model="item.name"
        :rules="[ruleRequired]"
        hide-bottom-space
        label="Название"
        outlined
        required
      />



      <monitoring-mode-select v-model="item.monitoring_mode" />

      <period-select v-model="item.period" />
      <template v-if="item.period == 5">
        <q-input
          v-model="item.period_date1"
          :rules="[ruleRequired]"
          type="date"
          label="Дата"
          outlined
        />
      </template>
      <template v-else-if="item.period == 2">
        <q-input
          v-model="item.period_date1"
          :rules="[ruleRequired]"
          hide-bottom-space
          type="date"
          label="Дата 1"
          outlined
        />
        <q-input
          v-model="item.period_date2"
          :rules="[ruleRequired]"
          hide-bottom-space
          type="date"
          label="Дата 2"
          outlined
        />
      </template>

      <monitoring-type-select
        v-model="item.monitoring_type"
        :rules="[ruleRequired]"
        hide-bottom-space
      />

      <template v-if="item.monitoring_mode != 3">
        <work-mode-select v-model="item.work_mode" />
        <products-select v-model="item.products" />
      </template>

      <q-input
        v-model="item.urls"
        type="textarea"
        label="URL сайтов"
        outlined
        required
      />

      <template #actions>
        <form-actions
          class="q-mt-lg"
          :saving="saving"
          :deleting="deleting"
          :btn-delete="isExists"
          @delete="onDelete"
        />
      </template>
    </base-form>

    <q-inner-loading :showing="loading" />
  </q-page>
</template>

<script setup lang="ts">
import BaseForm from '../../components/form/BaseForm.vue'
import ProductsSelect from '../../components/select/ProductsSelect.vue'
import WorkModeSelect from '../../components/select/WorkModeSelect.vue'
import MonitoringTypeSelect from '../../components/select/MonitoringTypeSelect.vue'
import PeriodSelect from '../../components/select/PeriodSelect.vue'
import MonitoringModeSelect from 'src/components/select/MonitoringModeSelect.vue'
import BackBtn from "src/components/form/BackBtn.vue"
import FormActions from "src/components/form/FormActions.vue"
import { storeToRefs } from "pinia"
import { promiseSetLoading } from "src/modules/StoreCrud"
import { promiseFunc, notifyDeleted, notifySaved } from "src/modules/Notif"
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useTasksStore } from "src/stores/tasks"
import { TaskStatus, userReadable } from 'src/modules/StaticTranslate'
import { ruleRequired } from 'src/Modules/Globals'
import { formatDateTime } from 'src/modules/Utils'

const route = useRoute()
const router = useRouter()

const store = useTasksStore()
const { parseTask: item } = storeToRefs(store)
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)


const itemId = computed(() => route.params.id as unknown as string)

const isExists = computed(() => Boolean(item.value?.id))

const defaultData = {
  id: null,
  name: "",
  period: 'onetime',
  period_date1: null,
  period_date2: null,
}

function loadData() {
  if (itemId.value == "new") {
    item.value = Object.assign({}, defaultData)
    return
  }
  const prom = store.loadParseTask(parseInt(itemId.value))
  promiseSetLoading(prom, loading)
}

function saveData() {
  const exists = isExists.value
  const payload = Object.assign({}, item.value)

  payload.products_write = payload.products?.map(p => p.id)

  const prom = exists ? store.updateParseTask(payload.id, payload) : store.createParseTask(payload)

  promiseSetLoading(prom, saving)
  void prom.then((resp) => {
    if (!exists) {
      void router.replace({
        params: {
          id: resp.id,
        },
      })
    }

    promiseFunc(prom, notifySaved)
  })
}

function onDelete() {
  const prom = store.deleteParseTask(item.value.id)

  promiseSetLoading(prom, deleting)
  void prom.then(() => {
    notifyDeleted()
    router.go(-1)
  })
}

onMounted(() => loadData())
</script>

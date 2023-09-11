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
        <div>
          <key-value-info :data="infoData">
            <template #value-status="props">
              <task-status-badge :status="props.value" />
            </template>
          </key-value-info>
        </div>
        <is-urls-valid :urls="item.invalid_urls" />

        <q-stepper
          :model-value="step"
          class="q-mt-sm"
          color="info"
          vertical
          flat
          bordered
        >
          <q-step
            title="Создание задачи"
            icon="add_circle"
            :name="1"
            :done="isExists"
          />
          <q-step
            title="Утверждение задачи"
            icon="verified"
            :name="2"
            :done="isVerified"
          >
            <template v-if="isManager">
              Вы можете утвердить задачу

              <template v-if="isTaskManager">
                <q-badge
                  color="positive"
                  class="text-subtitle2"
                >
                  Вы руководитель этого сотрудника
                </q-badge>
              </template>
              <template v-else>
                <q-badge
                  color="negative"
                  class="text-subtitle2"
                >
                  Вы не руководитель этого сотрудника
                </q-badge>
              </template>
              <q-stepper-navigation>
                <q-btn
                  label="Утвердить"
                  color="primary"
                  :loading="changingStatus"
                  unelevated
                  no-caps
                  @click="changeStatus(6)"
                />
              </q-stepper-navigation>
            </template>
          </q-step>
          <q-step
            title="Настройка задачи"
            icon="tune"
            :name="3"
            :done="isSetup"
          >
            <template v-if="isAdmin">
              <template v-if="!isUrlsValid">
                <q-badge
                  color="warning"
                  class="text-subtitle2"
                >
                  Для завершения настройки требуется настройка парсеров
                </q-badge>
              </template>
              <q-stepper-navigation>
                <q-btn
                  label="Завершить настройку"
                  color="primary"
                  :loading="changingStatus"
                  :disable="!isUrlsValid"
                  unelevated
                  no-caps
                  @click="changeStatus(2)"
                />
              </q-stepper-navigation>
            </template>
          </q-step>
          <q-step
            title="Парсинг"
            icon="memory"
            :name="4"
          />
        </q-stepper>

        <div
          v-if="isAdmin && isExists"
          class="row justify-around"
        >
          <q-btn
            v-if="item.status != 3"
            label="Отменить задачу"
            icon="cancell"
            color="negative"
            :loading="changingStatus"
            unelevated
            no-caps
            @click="changeStatus(3)"
          />
          <q-btn
            v-else
            label="Восстановить задачу"
            icon="restart_alt"
            color="info"
            :loading="changingStatus"
            unelevated
            no-caps
            @click="changeStatus(6)"
          />
          <q-btn
            label="Протестировать задачу"
            icon="play_arrow"
            color="primary"
            :to="{name: 'user_task_test', params: {id: itemId}}"
            unelevated
            no-caps
          />
        </div>
      </template>

      <!-- Form -->
      <q-input
        v-model="item.name"
        :rules="[ruleRequired]"
        hide-bottom-space
        label="Название"
        outlined
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
        :rules="[ruleRequired]"
        type="textarea"
        label="URL сайтов"
        outlined
      />

      <q-toggle
        v-model="item.notifications_enable"
        label="Отправлять уведомления"
      />

      <template v-if="item.notifications_enable">
        <q-option-group
          v-model="item.notifications_target"
          :options="notificationsOptions"
          color="primary"
          type="checkbox"
        />
      </template>

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
import TaskStatusBadge from '../../components/task/TaskStatusBadge.vue'
import KeyValueInfo from '../../components/form/KeyValueInfo.vue'
import IsUrlsValid from '../../components/task/IsUrlsValid.vue'
import BaseForm from '../../components/form/BaseForm.vue'
import ProductsSelect from '../../components/select/ProductsSelect.vue'
import WorkModeSelect from '../../components/select/WorkModeSelect.vue'
import MonitoringTypeSelect from '../../components/select/MonitoringTypeSelect.vue'
import PeriodSelect from '../../components/select/PeriodSelect.vue'
import MonitoringModeSelect from 'src/components/select/MonitoringModeSelect.vue'
import BackBtn from "src/components/form/BackBtn.vue"
import FormActions from "src/components/form/FormActions.vue"
import { storeToRefs } from "pinia"
import { promiseSetLoading } from "src/Modules/StoreCrud"
import { promiseFunc, notifyDeleted, notifySaved, notifyTaskStatusUpdated } from "src/Modules/Notif"
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useTasksStore } from "src/stores/tasks"
import { userReadable } from 'src/Modules/StaticTranslate'
import { ruleRequired } from 'src/Modules/Globals'
import { formatDateTime } from 'src/Modules/Utils'
import { useAuthStore } from 'src/stores/auth'

const route = useRoute()
const router = useRouter()

const store = useTasksStore()

const storeAuth = useAuthStore()

const { parseTask: item } = storeToRefs(store)
const { isAdmin, isManager } = storeToRefs(storeAuth)
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const changingStatus = ref(false)


const itemId = computed(() => route.params.id as unknown as string)

const isExists = computed(() => Boolean(item.value?.id))

const isVerified = computed(() => Boolean(item.value?.status!=1))
const isSetup = computed(() => [1,6].indexOf(item.value?.status||1) === -1)
const isTaskManager = computed(() => item.value?.author?.manager == storeAuth.account?.id)

const isUrlsValid = computed(() => item.value?.urls && item.value.urls.length > 0)

const notificationsOptions = computed(() => [
  {
    label: "Цена увеличилась",
    value: "incr",
  },
  {
    label: "Цена уменьшилась",
    value: "decr",
  },
])

const step = computed(() => {
  if (isSetup.value){
    return 4
  } else if (isVerified.value){
    return 3;
  } else {
    return 2;
  }
})

const infoData = computed(() => {
  if (!item.value){
    return []
  }
  const i = item.value
  return [
    {
      label: "Статус",
      name: "status",
      value: i.status,
    },
    {
      label: "Автор",
      name: "author",
      value: userReadable(i.author),
    },
    {
      label: "Дата создания",
      name: "created_at",
      value: formatDateTime(i.created_at),
    },
    {
      label: "Дата редактирования",
      name: "updated_at",
      value: formatDateTime(i.updated_at),
    },
  ]
})

const defaultData = {
  id: null,
  name: "",
  period: 1,
  period_date1: null,
  period_date2: null,
  monitoring_mode: 1,
  work_mode: 1,
  notifications_enable: false,
  notifications_target: [],
  invalid_urls: [],
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

  payload.products_write = payload.products?.map(p => p.id) || []

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

function changeStatus(status: number){
  if (!item.value){
    return
  }
  const prom = store.updateParseTaskStatus(item.value.id, status)

  promiseSetLoading(prom, changingStatus)
  promiseFunc(prom, notifyTaskStatusUpdated)
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

<template>
  <q-page padding>
    <back-btn />

    <!-- <h4 class="q-my-sm q-mb-xl">
      {{ product?.name }}
    </h4> -->
    <div class="q-my-md">
      <q-btn
        label="Запустить тест"
        :loading="testing"
        icon="play_arrow"
        color="positive"
        unelevated
        no-caps
        @click="runTest"
      />
      <q-toggle
        v-model="params.test"
        label="Не сохранять товары"
      />
      <div class="text-subtitle2 q-mt-md">
        Время запроса: {{ timerValue }} сек.
      </div>
    </div>

    <div class="row q-gutter-y-md">
      <q-card
        class="col-12 col-md-6"
        flat
        bordered
      >
        <q-card-section>
          <h6 class="text-center q-mt-none q-mb-sm">
            Собранные товары
          </h6>
          <test-parsed-data
            v-if="item"
            :data="item?.data"
          />
        </q-card-section>
      </q-card>
      <q-card
        class="col-12 col-md-6"
        flat
        bordered
      >
        <q-card-section>
          <h6 class="text-center q-mt-none q-mb-sm">
            Логи
          </h6>
          <test-logs-data
            v-if="item"
            :data="item?.logs"
          />
        </q-card-section>
      </q-card>
    </div>

    <q-inner-loading :showing="loading" />
  </q-page>
</template>

<script setup lang="ts">
import TestParsedData from '../../components/task/TestParsedData.vue'
import TestLogsData from "../../components/task/TestLogsData.vue"
import BaseForm from "../../components/form/BaseForm.vue"
import BackBtn from "src/components/form/BackBtn.vue"
import { storeToRefs } from "pinia"
import { promiseSetLoading } from "src/modules/StoreCrud"
import { Ref, computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useTasksStore } from "src/stores/tasks"
import { useNow } from "@vueuse/core"

const route = useRoute()

const store = useTasksStore()

const { parseTaskTest: item } = storeToRefs(store)
const loading = ref(false)
const testing = ref(false)

const params = ref({
  test: true,
})


const started: Ref<Date | null> = ref(null)
const stopped: Ref<Date | null> = ref(null)
const now = useNow()

const timerValue = computed(() => {
  if (!started.value){
    return 0
  }
  let val: number
  if (stopped.value){
    val = stopped.value.getTime() - started.value.getTime()
  } else {
    val = now.value.getTime() - started.value.getTime()
  }


  return (val / 1000).toFixed(2)
})

const itemId = computed(() => route.params.id as unknown as string)

function loadData() {
  const prom = store.loadParseTask(parseInt(itemId.value))
  promiseSetLoading(prom, loading)
}

function runTest() {
  console.debug("Running test with params: ", params.value)
  const prom = store.runTestParseTask(parseInt(itemId.value), params.value.test || undefined)
  promiseSetLoading(prom, testing)

  started.value = new Date()
  stopped.value = null

  prom.finally(() => stopped.value = new Date())
}

onMounted(() => loadData())
</script>

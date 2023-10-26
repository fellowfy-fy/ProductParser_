<template>
  <q-page padding>
    <back-btn />

    <base-form
      v-if="item"
      @submit="saveData"
    >
      <template #info>
        <q-input
          :model-value="item.domain"
          label="Домен"
          outlined
          readonly
        />

        <h6 class="text-center q-my-sm">
          Полезные ссылки
        </h6>
        <div>
          <q-list
            dense
            bordered
          >
            <q-item
              href="https://www.w3schools.com/cssref/css_selectors.php"
              target="blank"
            >
              <q-item-section>
                Информация о CSS selector
              </q-item-section>
            </q-item>
            <q-item
              href="https://try.jsoup.org/"
              target="blank"
            >
              <q-item-section>
                Онлайн тестер CSS selector
              </q-item-section>
            </q-item>
            <q-item
              href="https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb/related"
              target="blank"
            >
              <q-item-section>
                Selector Gadget (расширение для поиска CSS selector)
              </q-item-section>
            </q-item>
            <q-item
              href="https://support.smartbear.com/alertsite/docs/monitors/api/endpoint/jsonpath.html"
              target="blank"
            >
              <q-item-section>
                Информация о JSONPath
              </q-item-section>
            </q-item>
            <q-item
              href="https://jsonpath.com/"
              target="blank"
            >
              <q-item-section>
                Онлайн тестер JSONPath
              </q-item-section>
            </q-item>
          </q-list>
        </div>
        <h6 class="text-center q-my-sm">
          Переменные
        </h6>
        <span class="text-subtitle1 text-center text-grey q-pt-xs q-mb-sm">(доступны во всех текстовых полях)</span>
        <div>
          <variables-task />
        </div>
      </template>

      <q-input
        v-model="item.url"
        :rules="[ruleRequired, ruleValidURL]"
        label="URL *"
        outlined
        hint="Адрес куда будет направлен запрос парсера"
      />
      <q-input
        v-model="item.url_match"
        label="URL задачи"
        outlined
        hint="Задачи с таким же адресом будут использовать этот парсер"
      />
      <q-input
        v-model="item.url_before"
        label="Посетить URL перед задачей"
        outlined
        hint="Открыть этот URL перед переходом к URL задаче. Помогает в обходе защиты от ботов."
      />
      <q-select
        v-model="item.parse_mode"
        label="Тип данных *"
        :rules="[ruleRequired]"
        :disable="item.use_selenium"
        hide-bottom-space
        :options="optionsParseMethod"
        options-dense
        map-options
        emit-value
        outlined
        hint="Тип данных который возвращает указанный URL"
      />
      <q-select
        v-model="item.request_method"
        label="HTTP метод *"
        :rules="[ruleRequired]"
        :disable="item.use_selenium"
        hide-bottom-space
        :options="optionsRequestMethod"
        options-dense
        map-options
        emit-value
        outlined
        hint="HTTP метод который следует использовать при запросе к указанному URL"
      />

      <q-input
        v-model="item.path_title"
        :rules="[ruleRequired]"
        hide-bottom-space
        label="Путь к названию товара"
        :hint="hintPath"
        outlined
      />
      <q-input
        v-model="item.path_price"
        :rules="[ruleRequired]"
        hide-bottom-space
        label="Путь к цене товара"
        :hint="hintPath"
        outlined
      />

      <q-input
        v-model="item.attribute_title"
        :rules="[ruleRequired]"
        hide-bottom-space
        label="Атрибут названия товара"
        :hint="hintAttribute"
        outlined
      />
      <q-input
        v-model="item.attribute_price"
        :rules="[ruleRequired]"
        hide-bottom-space
        label="Атрибут цены товара"
        :hint="hintAttribute"
        outlined
      />

      <q-toggle
        v-model="item.force_parser_url"
        label="Принудительно использовать URL парсера"
        name="force_parser_url"
      >
        <q-tooltip>
          <label>
            Использовать URL парсера вместо URL задачи.<br>
            Можно использвоать если URL задачи используется только для определения нужного парсера, а у парсера отличный URL запроса.
          </label>
        </q-tooltip>
      </q-toggle>
      <q-toggle
        v-model="item.use_selenium"
        label="Использовать драйвер Selenium"
      >
        <q-tooltip>
          <label>
            Использовать драйвер Selenium эмулирующий браузер Chrome.<br>
            Помогает в обходе блокировок, если требуется загрузка скриптов.<br>
            Если включено, нельзя использовать многие параметры запроса.
          </label>
        </q-tooltip>
      </q-toggle>

      <q-expansion-item
        label="Дополнительные параметры"
        dense
      >
        <div class="q-gutter-y-md">
          <q-input
            v-model="item.request_headers"
            :rules="[ruleValidJSON]"
            :disable="item.use_selenium"
            type="textarea"
            label="Заголовки запроса"
            outlined
          />
          <q-input
            v-model="item.request_data"
            :rules="[ruleValidJSON]"
            :disable="item.use_selenium"
            type="textarea"
            label="Данные запроса (POST body)"
            outlined
          />
        </div>
      </q-expansion-item>



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
import VariablesTask from '../../components/common/VariablesTask.vue'
import BaseForm from '../../components/form/BaseForm.vue'
import BackBtn from "src/components/form/BackBtn.vue"
import FormActions from "src/components/form/FormActions.vue"
import { storeToRefs } from "pinia"
import { promiseSetLoading } from "src/Modules/StoreCrud"
import { promiseFunc, notifyDeleted, notifySaved } from "src/Modules/Notif"
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { ruleRequired, ruleValidJSON, ruleValidURL } from 'src/Modules/Globals'
import { useTasksStore } from 'src/stores/tasks'

const route = useRoute()
const router = useRouter()

const store = useTasksStore()
const { parseSetting: item } = storeToRefs(store)
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)


const itemId = computed(() => route.params.id as unknown as string)
const isExists = computed(() => Boolean(item.value?.id))

const optionsParseMethod = [
  {
    "label": "HTML",
    "value": 1,
  },
  {
    "label": "JSON",
    "value": 2,
  },
]
const optionsRequestMethod = [
  {
    "label": "GET",
    "value": "GET",
  },
  {
    "label": "POST",
    "value": "POST",
  },
]

const defaultData = {
  id: null,
  domain: null,
  request_method: 'GET',
  parse_mode: 1,
  force_parser_url: false,
  request_headers: "null",
  request_data: "null",
}


const hintPath = computed(() => item.value?.parse_mode == 1? 'Путь в формате CSS selector ' : 'Путь в формате JSONPath')

const hintAttribute = "Не обязательное поле, обычно нужно для извлечения из <meta> тегов"

function loadData() {
  if (itemId.value == "new") {
    item.value = Object.assign({}, defaultData)
    return
  }
  const prom = store.loadParseSettingsItem(parseInt(itemId.value))
  promiseSetLoading(prom, loading)
}

function saveData() {
  const exists = isExists.value
  const payload = Object.assign({}, item.value)

  const prom = exists ? store.updateParseSettings(payload.id, payload) : store.createParseSettings(payload)

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
  const prom = store.deleteParseSettings(item.value.id)

  promiseSetLoading(prom, deleting)
  void prom.then(() => {
    notifyDeleted()
    router.go(-1)
  })
}

onMounted(() => loadData())
</script>

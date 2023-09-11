<template>
  <q-page padding>
    <back-btn />


    <base-form
      v-if="item"
      @submit="saveData"
    >
      <template #info>
        <div>
          <key-value-info :data="infoData" />
        </div>
        <template v-if="item.section === 'emails'">
          <h6 class="text-center q-my-sm">
            Переменные писем
          </h6>
          <div>
            <variables-email />
          </div>
        </template>
      </template>

      <h6 class="q-my-md">
        {{ item?.verbose_name }}
      </h6>
      <q-input
        v-model="item.value"
        :type="inputType"
        :hint="item.help_text"
        label="Значение"
        outlined
        :autogrow="inputType == 'textarea'"
      />

      <template #actions>
        <form-actions
          class="q-mt-lg"
          :saving="saving"
          :deleting="deleting"
          :btn-delete="false"
        />
      </template>
    </base-form>

    <q-inner-loading :showing="loading" />
  </q-page>
</template>

<script setup lang="ts">
import VariablesEmail from '../../components/common/VariablesEmail.vue'
import KeyValueInfo from '../../components/form/KeyValueInfo.vue'
import BaseForm from '../../components/form/BaseForm.vue'
import BackBtn from "src/components/form/BackBtn.vue"
import FormActions from "src/components/form/FormActions.vue"
import { storeToRefs } from "pinia"
import { promiseSetLoading } from "src/Modules/StoreCrud"
import { promiseFunc, notifySaved } from "src/Modules/Notif"
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import { usePreferencesStore } from 'src/stores/preferences'

const route = useRoute()

const store = usePreferencesStore()
const { preference: item } = storeToRefs(store)
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)


const itemId = computed(() => route.params.id as unknown as string)

const inputType = computed(() => {
  // if (item.value.)
  if (item.value){
    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
    const widgetClass = item.value.field.widget.class as string
    if (widgetClass == "Textarea"){
      return "textarea"
    } else if (widgetClass == "NumberInput"){
      return "number"
    }
  }
  return "text";
})

const infoData = computed(() => {
  return [
    {
      label: "Распознанный тип поля",
      value: inputType.value,
    },
    {
      label: "Тип поля",
      value: item.value?.field?.class as string,
    },
  ]
})


function loadData() {
  const prom = store.loadPreference(itemId.value)
  promiseSetLoading(prom, loading)
}

function saveData() {
  const payload = Object.assign({}, item.value)

  const prom = store.updatePreference(payload.identifier, payload)

  promiseSetLoading(prom, saving)
  void prom.then(() => {

    promiseFunc(prom, notifySaved)
  })
}


onMounted(() => loadData())
</script>

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
          <key-value-info :data="infoData" />
        </div>
      </template>
      <q-input
        v-model="item.name"
        label="Название"
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
import KeyValueInfo from '../../components/form/KeyValueInfo.vue'
import BackBtn from "../../components/form/BackBtn.vue"
import FormActions from "../../components/form/FormActions.vue"
import { storeToRefs } from "pinia"
import { promiseSetLoading } from "src/Modules/StoreCrud"
import { promiseFunc, notifyDeleted, notifySaved } from "src/Modules/Notif"
import { useProductsStore } from "src/stores/products"
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { formatDateTime } from "src/Modules/Utils"
import { userReadable } from "src/Modules/StaticTranslate"

const $route = useRoute()
const $router = useRouter()

const store = useProductsStore()
const { statusproduct: item } = storeToRefs(store)
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)

const itemId = computed(() => $route.params.id as unknown as string)

const isExists = computed(() => Boolean(item.value?.id))

const infoData = computed(() => {
  if (!item.value){
    return []
  }
  const i = item.value
  return [
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
  price: null,
}

function loadData() {
  if (itemId.value == "new") {
    item.value = Object.assign({}, defaultData)
    return
  }
  const prom = store.loadStatusProduct(parseInt(itemId.value))
  promiseSetLoading(prom, loading)
}

function saveData() {
  const exists = isExists.value
  const payload = Object.assign({}, item.value)

  const prom = exists ? store.updateStatusProduct(payload.id, payload) : store.createStatusProduct(payload)

  promiseSetLoading(prom, saving)
  void prom.then((resp) => {
    if (!exists) {
      void $router.replace({
        params: {
          id: resp.id,
        },
      })
    }

    promiseFunc(prom, notifySaved)
  })
}

function onDelete() {
  if (!item.value) return;
  const prom = store.deleteStatusProduct(item.value.id)

  promiseSetLoading(prom, deleting)
  void prom.then(() => {
    notifyDeleted()
    $router.go(-1)
  })
}

onMounted(() => loadData())
</script>

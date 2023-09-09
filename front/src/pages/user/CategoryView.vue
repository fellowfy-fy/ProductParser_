<template>
  <q-page padding>
    <back-btn />

    <!-- <h4 class="q-my-sm q-mb-xl">
      {{ product?.name }}
    </h4> -->

    <q-form
      v-if="item"
      class="row column q-gutter-y-md"
      style="max-width: 600px"
      @submit="saveData"
    >
      <q-input
        v-model="item.name"
        label="Название"
        outlined
        required
      />
      <q-input
        :model-value="formatDateTime(item.created_at)"
        label="Дата создания"
        outlined
        readonly
      />
      <q-input
        :model-value="formatDateTime(item.updated_at)"
        label="Дата редактирования"
        outlined
        readonly
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

      <form-actions
        class="q-mt-lg"
        :saving="saving"
        :deleting="deleting"
        :btn-delete="isExists"
        @delete="onDelete"
      />
    </q-form>

    <q-inner-loading :showing="loading" />
  </q-page>
</template>

<script setup lang="ts">
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
const { category: item } = storeToRefs(store)
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)

const itemId = computed(() => $route.params.id as unknown as string)

const isExists = computed(() => Boolean(item.value?.id))

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
  const prom = store.loadCategory(parseInt(itemId.value))
  promiseSetLoading(prom, loading)
}

function saveData() {
  const exists = isExists.value
  const payload = Object.assign({}, item.value)

  const prom = exists ? store.updateCategory(payload.id, payload) : store.createCategory(payload)

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
  const prom = store.deleteCategory(item.value.id)

  promiseSetLoading(prom, deleting)
  void prom.then(() => {
    notifyDeleted()
    $router.go(-1)
  })
}

onMounted(() => loadData())
</script>

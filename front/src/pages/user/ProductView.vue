<template>
  <q-page padding>
    <back-btn />

    <!-- <h4 class="q-my-sm q-mb-xl">
      {{ product?.name || 'Новый продукт' }}
    </h4> -->

    <q-form
      v-if="product"
      class="row column q-gutter-y-md"
      style="max-width: 600px"
      @submit="saveData"
    >
      <q-input
        v-model="product.name"
        label="Название"
        outlined
        required
      />

      <q-input
        v-model.number="product.price"
        type="number"
        label="Цена"
        outlined
        required
      />
      <q-input
        v-model="product.linked_id"
        label="Связь"
        outlined
      />
      <q-input
        v-model="product.synonyms"
        type="textarea"
        label="Синонимы"
        outlined
        autogrow
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
import { promiseSetLoading } from "src/modules/StoreCrud"
import { promiseFunc, notifyDeleted, notifySaved } from "src/modules/Notif"
import { useProductsStore } from "src/stores/products"
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"

const $route = useRoute()
const $router = useRouter()

const store = useProductsStore()
const { product } = storeToRefs(store)
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)

const productId = computed(() => $route.params.id as unknown as string)

const isExists = computed(() => Boolean(product.value?.id))

const defaultData = {
  id: null,
  name: "",
  price: null,
}

function loadData() {
  if (productId.value == "new") {
    product.value = Object.assign({}, defaultData)
    return
  }
  const prom = store.loadProduct(parseInt(productId.value))
  promiseSetLoading(prom, loading)
}

function saveData() {
  const exists = isExists.value
  const payload = Object.assign({}, product.value)

  const prom = exists ? store.updateProduct(payload.id, payload) : store.createProduct(payload)

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
  const prom = store.deleteProduct(product.value.id)

  promiseSetLoading(prom, deleting)
  void prom.then(() => {
    notifyDeleted()
    $router.go(-1)
  })
}

onMounted(() => loadData())
</script>

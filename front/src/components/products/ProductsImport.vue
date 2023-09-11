<template>
  <q-dialog v-model="showImport">
    <q-card style="width: 300px">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">
          Импорт продуктов
        </div>
        <q-space />
        <q-btn
          v-close-popup
          icon="close"
          flat
          round
          dense
        />
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-form
          id="products-import"
          @submit="onImport"
        >
          <q-file
            v-model="fileModel"
            class="q-my-md"
            :rules="[ruleRequired]"
            label="Файл"
            clearable
            outlined
          >
            <template #prepend>
              <q-icon name="attach_file" />
            </template>
          </q-file>
        </q-form>
      </q-card-section>

      <q-card-actions
        align="right"
        class="bg-white text-teal"
      >
        <q-btn
          type="submit"
          form="products-import"
          label="Импорт"
          flat
          :loading="isLoading"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-btn
    label="Импорт"
    color="primary"
    icon="upload"
    size="sm"
    unelevated
    @click="showImport = true"
  />
</template>

<script setup lang="ts">
import { ruleRequired } from "src/Modules/Globals"
import { promiseSetLoading } from "src/Modules/StoreCrud"
import { notifySuccess } from "src/Modules/Notif"
import { useProductsStore } from "src/stores/products"
import { Ref, ref } from "vue"

const emit = defineEmits(["update"])

const showImport = ref(false)
const store = useProductsStore()

const fileModel: Ref<File | null> = ref(null)
const isLoading = ref(false)

function onImport() {
  if (!fileModel.value) {
    return
  }
  const prom = store.importProducts(fileModel.value)
  promiseSetLoading(prom, isLoading)
  void prom.then((resp) => {
    emit("update")
    showImport.value = false
    fileModel.value = null
    notifySuccess(`Успешно импортировано товаров: ${resp.count}`)
  })
}
</script>

<template>
  <q-dialog v-model="showModal">
    <q-card style="width: 700px; max-width: 80vw;">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">
          Изменить пароль
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

      <q-card-section>
        <q-form
          class="q-gutter-y-md"
          @submit="onSubmit"
        >
          <q-toggle
            v-model="showPassword"
            label="Показать пароль"
          />
          <q-input
            v-model="password1"
            :type="fieldType"
            :rules="[ruleRequired, rulePasswordLength]"
            label="Пароль"
            placeholder="********"
            outlined
          />
          <q-input
            v-model="password2"
            :type="fieldType"
            :rules="[ruleRequired, rulePasswordMatch]"
            label="Повторите пароль"
            placeholder="********"
            outlined
          />
          <form-actions
            :btn-delete="false"
            :saving="isSaving"
          />
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>

  <q-btn
    label="Задать пароль"
    icon="key"
    color="primary"
    no-caps
    unelevated
    @click="showModal = true"
  />
</template>

<script setup lang="ts">
import FormActions from '../form/FormActions.vue'
import { ruleRequired } from "src/Modules/Globals"
import { notifySuccess } from "src/Modules/Notif"
import { promiseSetLoading } from "src/Modules/StoreCrud"
import { useAuthStore } from "src/stores/auth"
import { computed, ref } from "vue"

const props = defineProps({
  userId: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(["update"])

const store = useAuthStore()

const showModal = ref(false)
const showPassword = ref(false)
const isSaving = ref(false)

const password1 = ref("")
const password2 = ref("")

const rulePasswordLength = (val: string) => val.length >= 8 || "Пароль должен содержать не менее 8 символов"
const rulePasswordMatch = (val: string) => val == password1.value || "Пароли не совпадают"

const fieldType = computed(() => showPassword.value ? "text" : "password")

function resetForm(){
  password1.value = ""
  password2.value = ""
  showPassword.value = false
}

function onSubmit(){
  if (password1.value !== password2.value || !password1.value){
    return
  }
  const prom = store.setUserPassword(props.userId, password1.value)

  promiseSetLoading(prom, isSaving)
  void prom.then(() => {
    notifySuccess("Пароль успешно изменен")
    emit("update")
    resetForm()
    showModal.value = false
  })
}

</script>

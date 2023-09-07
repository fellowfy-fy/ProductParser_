<template>
  <q-page padding>
    <back-btn />

    <base-form
      v-if="item"
      @submit="saveData"
    >
      <template #info>
        <q-input
          :model-value="formatDateTime(item.date_joined)"
          label="Дата регистрации"
          outlined
          readonly
          dense
        />
      </template>

      <q-input
        v-model="item.username"
        :rules="[ruleRequired]"
        hide-bottom-space
        autocomplete="off"
        label="Username"
        outlined
      />
      <q-input
        v-model="item.first_name"
        hide-bottom-space
        label="Имя"
        outlined
      />
      <q-input
        v-model="item.last_name"
        hide-bottom-space
        label="Фамилия"
        outlined
      />
      <q-input
        v-model="item.middle_name"
        hide-bottom-space
        label="Отчество"
        outlined
      />
      <q-input
        v-model="item.email"
        :rules="[ruleRequired, ruleValidEmail]"
        type="email"
        autocomplete="off"
        hide-bottom-space
        label="Email"
        outlined
      />
      <user-role-select v-model="item.role" />
      <user-status-select v-model="item.is_active" />
      <template v-if="item.role == 1">
        <user-select
          v-model="item.manager"
          :params="{role: 2}"
          label="Непосредственный руководитель"
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
import UserSelect from '../../components/select/UserSelect.vue'
import UserRoleSelect from '../../components/select/UserRoleSelect.vue'
import UserStatusSelect from '../../components/select/UserStatusSelect.vue'
import BaseForm from '../../components/form/BaseForm.vue'
import BackBtn from "src/components/form/BackBtn.vue"
import FormActions from "src/components/form/FormActions.vue"
import { storeToRefs } from "pinia"
import { promiseSetLoading } from "src/modules/StoreCrud"
import { promiseFunc, notifyDeleted, notifySaved } from "src/modules/Notif"
import { computed, onMounted, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { formatDateTime } from 'src/modules/Utils'
import { useAuthStore } from 'src/stores/auth'
import { ruleRequired, ruleValidEmail } from 'src/Modules/Globals'

const route = useRoute()
const router = useRouter()

const store = useAuthStore()
const { user: item } = storeToRefs(store)
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)


const itemId = computed(() => route.params.id as unknown as string)

const isExists = computed(() => Boolean(item.value?.id))

const defaultData = {
  id: null,
  username: "",
  password: null,
  role: 1,
}

function loadData() {
  if (itemId.value == "new") {
    item.value = Object.assign({}, defaultData)
    return
  }
  const prom = store.loadUser(parseInt(itemId.value))
  promiseSetLoading(prom, loading)
}

function saveData() {
  const exists = isExists.value
  const payload = Object.assign({}, item.value)

  const prom = exists ? store.updateUser(payload.id, payload) : store.createUser(payload)

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
  const prom = store.deleteUser(item.value.id)

  promiseSetLoading(prom, deleting)
  void prom.then(() => {
    notifyDeleted()
    router.go(-1)
  })
}

onMounted(() => loadData())
</script>

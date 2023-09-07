<template>
  <q-select
    v-model="model"
    :loading="loading"
    :options="users"
    options-dense
    :option-label="userReadable"
    option-value="id"
    map-options
    emit-value
    outlined
    use-input
    v-bind="$attrs"
    style="max-width: 100%"
    @filter="onFilter"
  />
</template>

<script setup lang="ts">
import { Ref, computed, onMounted, ref } from "vue"
import { storeToRefs } from "pinia"
import { promiseSetLoading } from "src/modules/StoreCrud"
import { useAuthStore } from "src/stores/auth"
import { userReadable } from "src/modules/StaticTranslate"
import { CustomUser } from "src/client"

const props = defineProps({
  modelValue: {
    type: Number,
    required: true,
    default: undefined,
  },
  params: {
    type: Object,
    default: null,
  },
})

const $emit = defineEmits(["update:model-value"])

const store = useAuthStore()
const { users } = storeToRefs(store)

const loading = ref(false)
const search = ref("")

const cachedUser: Ref<CustomUser | null> = ref(null)

const model = computed({
  get() {
    return props.modelValue
  },
  set(val) {
    $emit("update:model-value", val)
  },
})

function checkValueLoaded() {
  if (!users.value || !props.modelValue) {
    return
  }
  if (cachedUser.value?.id == props.modelValue) {
    users.value.unshift(cachedUser.value)
    return
  }

  const info = users.value.find((u) => u.id == props.modelValue)
  if (!info) {
    const prom = store.loadUser(props.modelValue, true)

    void prom.then((user: CustomUser) => {
      cachedUser.value = user
      users.value?.unshift(user)
    })
  }
}

function loadData() {
  const payload = {
    search: search.value,
  }
  if (props.params) {
    Object.assign(payload, props.params)
  }
  const prom = store.loadUsers(payload)
  promiseSetLoading(prom, loading)
  void prom.then(() => void checkValueLoaded())
  return prom
}

function onFilter(value: string, update: CallableFunction) {
  if (!value && !search.value && users.value) {
    update()
    return
  }
  search.value = value
  update(() => {
    void loadData()
  })
}

onMounted(() => loadData())
</script>

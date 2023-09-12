<template>
  <q-select
    v-model="model"
    :loading="loading"
    :options="items || []"
    label="Настройки"
    options-dense
    option-label="domain"
    option-value="id"
    map-options
    outlined
    use-input
    emit-value
    v-bind="$attrs"
    style="max-width: 100%"
    @filter="onFilter"
  />
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { promiseSetLoading } from 'src/Modules/StoreCrud';
import { useTasksStore } from 'src/stores/tasks';

const props = defineProps({
  modelValue: {
    type: Number,
    required: true,
    default: undefined,
  },
})

const $emit = defineEmits(['update:model-value'])

const store = useTasksStore()
const {parseSettings: items} = storeToRefs(store)

const loading = ref(false)
const search = ref("")

const model = computed({
  get(){
    return props.modelValue
  },
  set(val){
    $emit('update:model-value', val)
  }
})

function loadData() {
  const payload = {
    search: search.value,
  }
  const prom = store.loadParseSettings(payload)
  promiseSetLoading(prom, loading)
  return prom;
}

function onFilter(value: string, update: CallableFunction){
  search.value = value
  update(() => {
    void loadData()
  })
}

onMounted(() => loadData())

</script>
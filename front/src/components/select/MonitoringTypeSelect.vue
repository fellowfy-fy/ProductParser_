<template>
  <q-select
    v-model="model"
    v-bind="$attrs"
    :options="options"
    label="Тип мониторинга"
    options-dense
    map-options
    emit-value
    multiple
    outlined
  />
</template>

<script setup lang="ts">
import { PropType, computed } from 'vue';


const props = defineProps({
  modelValue: {
    type: Array as PropType<string[]>,
    required: true,
  }
})

const emit = defineEmits(["update:model-value"])

const options = [
  {
    label: "Отчеты",
    value: "report",
  },
  {
    label: "Выгрузка",
    value: "export",
  },
]

const model = computed({
  get(){
    return props.modelValue
  },
  set(val){
    emit("update:model-value", val)
  }
})



</script>
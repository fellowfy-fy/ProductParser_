<template>
  <q-select
    v-model="model"
    v-bind="$attrs"
    :options="options"
    label="Вариант работы"
    options-dense
    map-options
    emit-value
    outlined
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';


const props = defineProps({
  modelValue: {
    type: Number,
    required: true,
  }
})

const emit = defineEmits(["update:model-value"])

const options = [
  {
    label: "Текущие цены",
    value: 1,
  },
  {
    label: "Динамика",
    value: 2,
  },
  {
    label: "Отличия",
    value: 3,
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
<template>
  <q-btn-toggle
    v-model="model"
    v-bind="$attrs"
    toggle-color="primary"
    color="grey-3"
    text-color="primary"
    :options="options"
    unelevated
    spread
    dense
    no-caps
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
    label: "Строгий мониторинг",
    value: 1,
  },
  {
    label: "Гибкий мониторинг",
    value: 2,
  },
  {
    label: "Получение каталогов",
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
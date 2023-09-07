<template>
  <q-select
    v-model="model"
    :options="options"
    label="Статус пользователя"
    options-dense
    map-options
    emit-value
    outlined
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue';


const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  }
})

const emit = defineEmits(["update:model-value"])

const options = [
  {
    label: "Активен",
    value: true,
  },
  {
    label: "Архив",
    value: false,
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
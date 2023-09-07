<template>
  <q-select
    v-model="model"
    :options="options"
    label="Роль пользователя"
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
    type: Number,
    required: true,
  }
})

const emit = defineEmits(["update:model-value"])

const options = [
  {
    label: "Сотрудник",
    value: 1,
  },
  {
    label: "Руководитель",
    value: 2,
  },
  {
    label: "Администратор",
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
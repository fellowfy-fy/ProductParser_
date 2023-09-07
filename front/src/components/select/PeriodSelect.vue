<template>
  <q-select
    v-model="model"
    v-bind="$attrs"
    :options="options"
    label="Периодичность мониторинга"
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
    label: "Ежедневно",
    value: 1,
  },
  {
    label: "Дважды в месяц",
    value: 2,
  },
  {
    label: "Раз в месяц",
    value: 3,
  },
  {
    label: "Ежеквартально",
    value: 4,
  },
  {
    label: "Единоразово",
    value: 5,
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
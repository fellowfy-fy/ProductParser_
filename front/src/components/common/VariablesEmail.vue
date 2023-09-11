<template>
  <key-value-info :data="data" />
</template>

<script setup lang="ts">
import KeyValueInfo from '../form/KeyValueInfo.vue'
const data = [
  {
    label: "Статус задачи",
    value: "{{status}}"
  },
  {
    label: "Автор задачи",
    value: "{{author}}"
  },
  {
    label: "Текущая цена",
    value: "{{price}}"
  },
  {
    label: "Цена изменена",
    value: "{{new_price}}"
  },
]
</script>
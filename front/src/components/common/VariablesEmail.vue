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
    label: "Старый статус задачи (только изменение статуса)",
    value: "{{old_status}}"
  },
  {
    label: "Автор задачи",
    value: "{{author}}"
  },
  {
    label: "Старая цена (только изменение цены)",
    value: "{{old_price}}"
  },
  {
    label: "Новая цена (только изменение цены)",
    value: "{{price}}"
  },
]
</script>
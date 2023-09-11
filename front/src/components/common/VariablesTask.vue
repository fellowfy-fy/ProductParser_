<template>
  <key-value-info :data="data" />
</template>

<script setup lang="ts">
import KeyValueInfo from '../form/KeyValueInfo.vue'
const data = [
  {
    label: "Название продукта",
    value: "{{product.name}}"
  },
  {
    label: "Цена продукта",
    value: "{{product.price}}"
  },
  {
    label: "URL парсера",
    value: "{{settings.url}}"
  },
  {
    label: "URL match парсера",
    value: "{{settings.url_match}}"
  },
  {
    label: "Путь к названию парсера",
    value: "{{settings.path_title}}"
  },
  {
    label: "Путь к цене парсера",
    value: "{{settings.part_price}}"
  },
]
</script>
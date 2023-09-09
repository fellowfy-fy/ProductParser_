<template>
  <q-markup-table
    flat
    bordered
    dense
  >
    <thead>
      <tr>
        <td>Название товара</td>
        <td>Цена</td>
      </tr>
    </thead>
    <tbody>
      <template
        v-for="(items) of data"
      >
        <tr
          v-for="item of items.parse_result"
          :key="item"
        >
          <td>
            {{ item.title }}
          </td>
          <td>
            {{ `${item.price.toLocaleString()}₽` }}
          </td>
        </tr>
      </template>
    </tbody>
  </q-markup-table>
</template>

<script setup lang="ts">
import { ProcessResult } from 'src/client';
import { PropType } from 'vue';


defineProps({
  data: {
    type: Array as PropType<ProcessResult[]>,
      required: true,
  }
})

</script>
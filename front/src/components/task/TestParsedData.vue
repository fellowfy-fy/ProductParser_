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
          v-for="(item, idx) of items.parse_result"
          :key="idx"
        >
          <td>
            {{ item.title }}
            <q-tooltip>
              Настройки парсера : {{ items.settings.domain }} (#{{ items.settings.id }})
              <br>
              Задача: {{ items.task.name }} (#{{ items.task.id }})
            </q-tooltip>
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
import { TestRunResultsData } from 'src/client';
import { PropType } from 'vue';


defineProps({
  data: {
    type: Array as PropType<TestRunResultsData[]>,
      required: true,
  }
})

</script>
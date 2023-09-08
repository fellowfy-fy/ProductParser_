<template>
  <q-markup-table
    flat
    bordered
    dense
    separator="cell"
  >
    <thead>
      <slot name="thead" />
    </thead>
    <tbody>
      <slot name="row-top" />
      <tr
        v-for="row of data"
        :key="row.label"
      >
        <td>
          {{ row.label }}
        </td>
        <td>
          <slot
            :name="'value-'+row.name"
            :row="row"
            :value="row.value"
          >
            {{ row.value }}
          </slot>
        </td>
      </tr>
      <slot name="row-bottom" />
    </tbody>
  </q-markup-table>
</template>

<script setup lang="ts">
import { PropType } from 'vue';


interface RowInfo {
  label: string;
  name: string;
  value?: string;
}

export type DataType = RowInfo[];

const props = defineProps({
  data: {
    type: Array as PropType<RowInfo[]>,
    required: true,
  }
})

</script>
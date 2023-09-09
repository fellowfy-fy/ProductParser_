<template>
  <q-badge :color="color">
    {{ name }}
  </q-badge>
</template>

<script setup lang="ts">
import { TaskStatus } from 'src/Modules/StaticTranslate';
import { computed } from 'vue';


const props = defineProps({
  status: {
    type: Number,
    default: 1
  }
})


const name = computed(() => TaskStatus.get(props.status))

const color = computed(() => {
  switch (props.status) {
    case 1:
      return 'info'
    case 2:
      return 'positive'
    case 3:
      return 'negative'
    case 4:
      return 'info'
    case 5:
      return 'warning'
    case 6:
      return 'accent'
    case 7:
      return 'negative'

    default:
      return 'info'
  }
})

</script>
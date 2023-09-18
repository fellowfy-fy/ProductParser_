<template>
  <div
    class="row items-start q-gutter-md"
    :class="[alignStart ? 'justify-start' : '', cls]"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps({
  alignStart: {
    type: Boolean,
    default: true
  },
  cls: {
    type: String,
    default: "",
  }
})
</script>
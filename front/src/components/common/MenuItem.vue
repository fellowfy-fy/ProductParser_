<template>
  <q-item
    clickable
    :to="to"
  >
    <q-item-section avatar>
      <q-icon
        :name="icon"
      />
    </q-item-section>
    <q-item-section>
      {{ label }}
    </q-item-section>
  </q-item>
</template>

<script setup lang="ts">
const props = defineProps({
  to: {
    type: Object,
    required: true,
  },
  icon: {
    type: String,
    default: "list_alt"
  },
  label: {
    type: String,
    default: "",
  }
})
</script>
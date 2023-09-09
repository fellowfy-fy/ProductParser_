<template>
  <q-item
    clickable
    :to="to"
    v-bind="$attrs"
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
defineProps({
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
<template>
  <q-form
    v-bind="$attrs"
    @submit="emit('submit', $event)"
  >
    <q-card
      flat
      bordered
    >
      <q-card-section class="row justify-around q-col-gutter-x-sm q-col-gutter-y-md">
        <!-- Form content -->
        <div
          class="col-12 col-md-6 col-lg-4 row column q-col-gutter-y-md"
          :class="contentClass"
        >
          <slot name="default" />
        </div>

        <!-- Aside info -->
        <div class="col-12 col-md-6 col-lg-4">
          <q-expansion-item
            label="Доп информация"
            default-opened
          >
            <div class="row column q-col-gutter-y-md">
              <slot name="info" />
            </div>
            <!-- TODO: last run background tasks info / logs -->
          </q-expansion-item>
        </div>
      </q-card-section>
      <q-card-actions justify="start">
        <div class="col-12 col-md-6">
          <!-- Actions -->
          <slot name="actions" />
        </div>
      </q-card-actions>
    </q-card>
  </q-form>
</template>

<script setup lang="ts">

const props = defineProps({
  contentClass: {
    type: String,
    default: ""
  }
})

const emit = defineEmits(["submit"])

</script>
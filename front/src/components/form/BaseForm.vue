<template>
  <q-form
    v-bind="$attrs"
    @submit="emit('submit', $event)"
  >
    <q-card
      flat
      bordered
    >
      <q-card-section class="row justify-start q-col-gutter-x-md q-col-gutter-y-md">
        <!-- Form content -->
        <div
          class="form-col col-12 col-md-6 col-lg-4 row column q-col-gutter-y-md"
          :class="contentClass"
        >
          <slot name="default" />
        </div>
        <q-space v-if="$q.screen.gt.md" />

        <!-- Aside info -->
        <div class="form-col col-12 col-md-6 col-lg-4">
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
        <q-space />
      </q-card-section>
      <q-card-actions justify="start">
        <div class="form-col col-12 col-md-6 col-lg-4">
          <!-- Actions -->
          <slot name="actions" />
        </div>
      </q-card-actions>
    </q-card>
  </q-form>
</template>

<script setup lang="ts">

defineProps({
  contentClass: {
    type: String,
    default: ""
  }
})

const emit = defineEmits(["submit"])

</script>

<style lang="scss" scoped>
.form-col{
  flex-grow: 1;
  max-width: 600px;
}
</style>
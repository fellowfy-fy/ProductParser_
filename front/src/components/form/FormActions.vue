<template>
  <div class="row justify-around">
    <slot name="before" />
    <q-btn
      v-if="btnSave"
      type="submit"
      label="Сохранить"
      color="positive"
      icon="save"
      unelevated
      no-caps
      :loading="saving"
      :disable="anyLoading"
      @click="$emit('save', $event)"
    />
    <slot name="center" />
    <q-btn
      v-if="btnDelete"
      label="Удалить"
      color="negative"
      icon="delete"
      unelevated
      no-caps
      :loading="deleting"
      :disable="anyLoading"
      @click="onDelete"
    />
    <slot name="after" />
  </div>
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar';
import { computed } from 'vue';


const props = defineProps({
  btnSave: {
    type: Boolean,
    default: true,
  },
  btnDelete: {
    type: Boolean,
    default: true,
  },
  deleteConfirm: {
    type: Boolean,
    default: true
  },
  saving: {
    type: Boolean,
    default: false,
  },
  deleting: {
    type: Boolean,
    default: false,
  },
})

const $emit = defineEmits(["save", "delete"])

const $q = useQuasar()

const anyLoading = computed(() => {
  return props.saving || props.deleting
})

function onDelete(e: Event){
  if (props.deleteConfirm){
    $q.dialog({
      message: "Вы уверены что хотите удалить этот объект?"
    }).onOk(() => {
      $emit('delete', e)
    })
  } else {
    $emit('delete', e)
  }
}

</script>
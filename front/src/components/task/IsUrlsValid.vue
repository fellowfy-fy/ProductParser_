<template>
  <div>
    <q-banner
      class="q-my-sm text-white"
      :class="bannerClass"
      inline-actions
      rounded
    >
      <template #avatar>
        <q-icon
          size="md"
          :name="icon"
          color="white"
        />
      </template>

      {{ text }}
    </q-banner>

    <q-list
      v-if="!isValid"
      bordered
      separator
      dense
    >
      <q-item
        v-for="url of urls"
        :key="url"
        v-ripple
      >
        <q-item-section>
          {{ url }}
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script setup lang="ts">
import {PropType, computed} from 'vue'

const props = defineProps({
  urls: {
    type: Array as PropType<string[]>,
    required: true
  }
})

const isValid = computed(() => !(props.urls && props.urls.length > 0))


const icon = computed(() => isValid.value? 'check_circle' : 'error')
const bannerClass = computed(() => isValid.value? 'bg-primary' : 'bg-warning')
const text = computed(() => isValid.value? 'Все парсеры настроены' : 'У некоторых URL нет парсеров:')

</script>
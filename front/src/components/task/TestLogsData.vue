<template>
  <div class="wrapper">
    <q-list dense>
      <q-expansion-item
        v-for="(item, idx) of data"
        :key="idx"
        group="task_logs"
        clickable
        dense
        @click="copyMessage(item.message)"
      >
        <template #header>
          <q-item-section avatar>
            <q-badge :color="logLevelColor(item.level)">
              {{ item.level }}
            </q-badge>
          </q-item-section>
          <q-item-section>
            <q-item-label
              class="text-grey-7"
              :lines="2"
            >
              {{ item.message }}
              {{ item.exception }}
            </q-item-label>
          </q-item-section>
          <q-item-section side>
            <q-item-label caption>
              {{ formatDateTimeSeconds(item.time) }}
            </q-item-label>
          </q-item-section>
        </template>

        <template #default>
          {{ item.message }}
        </template>
      </q-expansion-item>
    </q-list>
  </div>
</template>

<script setup lang="ts">
import { copyToClipboard } from 'quasar';
import { CachedLog } from 'src/client';
import { formatDateTimeSeconds } from 'src/Modules/utils';
import { PropType } from 'vue';


const props = defineProps({
  data: {
    type: Array as PropType<Array<CachedLog>>,
      required: true,
  }
})

function logLevelColor(level: string){
  switch (level) {
    case 'debug':
      return 'grey'
    case 'error':
      return 'negative'
    case 'warning':
      return 'warning'

    default:
      return 'info'
  }
}

function copyMessage(message: string){
  void copyToClipboard(message)
}

</script>

<style lang="scss" scoped>
.wrapper{
  height: 800px;
  max-height: 800px;
  width: 100%;
  overflow-y: auto;
}
</style>
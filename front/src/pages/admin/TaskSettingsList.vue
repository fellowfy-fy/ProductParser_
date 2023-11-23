<template>
  <q-page padding>
    <q-card
      class="row q-mb-lg"
      flat
      bordered
    >
      <q-card-section>
        <q-btn
          label="Создать"
          color="positive"
          icon="add"
          size="sm"
          unelevated
          @click="onCreateNew"
        />
      </q-card-section>
    </q-card>

    <fast-table
      title="Парсеры"
      :data="data"
      :load="loadData"
      :columns="tableColumns"
      @row-click="onRowClick"
    >
      <template #body-cell-is_active="props">
        <q-td>
          <q-badge
            v-if="props.value"
            color="positive"
          >
            Да
          </q-badge>
          <q-badge
            v-else
            color="negative"
          >
            Нет
          </q-badge>
        </q-td>
      </template>
    </fast-table>
  </q-page>
</template>

<script setup lang="ts">
import FastTable from '../../components/form/FastTable.vue'
import { computed } from 'vue';
import { QTableProps } from 'quasar';
import { ParseTask } from "src/client"
import { useRouter } from 'vue-router';
import { useTasksStore } from 'src/stores/tasks';

const router = useRouter()
const store = useTasksStore()

const data = computed(() => store.parseSettings)

const tableColumns = [
  {
    name: 'id',
    label: 'ID',
    field: 'id',
    required: true,
    sortable: true,
    style: 'width: 20px'
  },
  {
    name: 'domain',
    label: 'Домен',
    field: 'domain',
    align: 'left',
    sortable: true,
  },
  {
    name: 'url_match',
    label: 'URL задачи',
    field: 'url_match',
    align: 'left',
    sortable: true,
  },
  // {
  //   name: 'created_at',
  //   label: 'Дата создания',
  //   field: 'created_at',
  //   format(val: string){
  //     return formatDateTime(val)
  //   },
  //   sortable: true,
  //   style: 'width:100px'
  // }
] as QTableProps["columns"]

function loadData(payload: object){
  const prom = store.loadParseSettings(payload)
  return prom
}

function onRowClick(e, data: ParseTask){
  void router.push({
    name: 'admin_parse_setting', params: {id: data.id}
  })
}

function onCreateNew(){
  void router.push({
    name: 'admin_parse_setting', params: {id: 'new'}
  })
}
</script>
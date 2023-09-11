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
      title="Задачи"
      :columns="tableColumns"
      :data="data"
      :load="loadData"
      @row-click="onRowClick"
    >
      <template #body-cell-status="props">
        <q-td>
          <task-status-badge :status="props.value" />
        </q-td>
      </template>
    </fast-table>
  </q-page>
</template>

<script setup lang="ts">
import FastTable from '../../components/form/FastTable.vue'
import TaskStatusBadge from '../../components/task/TaskStatusBadge.vue'
import { computed } from 'vue';
import { useTasksStore } from 'src/stores/tasks';
import { QTableProps } from 'quasar';
import { ParseTask, ShortUser } from "src/client"
import {formatDateTime} from 'src/Modules/Utils'
import { useRouter } from 'vue-router';
import { userReadable } from 'src/Modules/StaticTranslate';

const router = useRouter()

const store = useTasksStore()

const data = computed(() => store.parseTasks)

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
    name: 'name',
    label: 'Название',
    field: 'name',
    align: 'left',
    sortable: true,
  },
  {
    name: 'status',
    label: 'Статус',
    field: 'status',
    align: 'left',
    // format(val:number) {
    //     return TaskStatus.get(val) || val
    // },
    sortable: true,
  },
  {
    name: 'author',
    label: 'Автор',
    field: 'author',
    align: 'left',
    format(val:ShortUser) {
        return userReadable(val)
    },
    sortable: true,
  },
  {
    name: 'created_at',
    label: 'Создан',
    field: 'created_at',
    format(val: string){
      return formatDateTime(val)
    },
    sortable: true,
    style: 'width:100px'
  }
] as QTableProps["columns"]

function loadData(payload: object){
  const prom = store.loadParseTasks(payload)
  return prom
}


function onRowClick(e, data: ParseTask){
  void router.push({
    name: 'user_task', params: {id: data.id}
  })
}

function onCreateNew(){
  void router.push({
    name: 'user_task', params: {id: 'new'}
  })
}
</script>
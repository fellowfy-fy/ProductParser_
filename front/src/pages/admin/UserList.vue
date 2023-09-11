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
      title="Пользователи"
      :columns="tableColumns"
      :data="data"
      :load="loadData"
      @row-click="onRowClick"
    >
      <template #body-cell-is_active="props">
        <q-td :props="props">
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
import { ParseTask, } from "src/client"
import {formatDateTime} from 'src/Modules/Utils'
import { useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';

const router = useRouter()

const store = useAuthStore()


const data = computed(() => store.users)

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
    name: 'username',
    label: 'Username',
    field: 'username',
    align: 'left',
    sortable: true,
  },
  {
    name: 'first_name',
    label: 'Имя',
    field: 'first_name',
    align: 'left',
    sortable: true,
  },
  {
    name: 'last_name',
    label: 'Фамилия',
    field: 'last_name',
    align: 'left',
    sortable: true,
  },
  {
    name: 'is_active',
    label: 'Активен',
    field: 'is_active',
    align: 'center',
    sortable: true,
    style: 'width: 20px'
  },
  {
    name: 'date_joined',
    label: 'Создан',
    field: 'date_joined',
    format(val: string){
      return formatDateTime(val)
    },
    sortable: true,
    style: 'width:100px'
  }
] as QTableProps["columns"]

function loadData(payload: object){
  const prom = store.loadUsers(payload)
  return prom
}


function onRowClick(e, data: ParseTask){
  void router.push({
    name: 'admin_user', params: {id: data.id}
  })
}

function onCreateNew(){
  void router.push({
    name: 'admin_user', params: {id: 'new'}
  })
}

</script>
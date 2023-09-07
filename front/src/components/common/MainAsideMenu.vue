<template>
  <template v-if="userRole == TUserRole.admin">
    <!-- Admin -->
  </template>

  <template v-if="userRole == TUserRole.manager">
    <!-- Manager -->
  </template>

  <template v-if="true">
    <!-- Common -->
    <q-item
      clickable
      :to="{name: 'user_products'}"
    >
      <q-item-section avatar>
        <q-icon
          name="inventory"
        />
      </q-item-section>
      <q-item-section>
        Товары
      </q-item-section>
    </q-item>
    <q-item
      clickable
      :to="{name: 'user_categories'}"
    >
      <q-item-section avatar>
        <q-icon
          name="category"
        />
      </q-item-section>
      <q-item-section>
        Разделы
      </q-item-section>
    </q-item>
    <q-item
      clickable
      :to="{name: 'user_tasks'}"
    >
      <q-item-section avatar>
        <q-icon
          name="task"
        />
      </q-item-section>
      <q-item-section>
        Задачи
      </q-item-section>
    </q-item>
  </template>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { TUserRole, useAuthStore } from 'src/stores/auth';


const store = useAuthStore()
const {userRole} = storeToRefs(store)

</script>
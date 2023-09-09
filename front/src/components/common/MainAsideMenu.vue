<template>
  <template v-if="userRole == TUserRole.admin">
    <!-- Admin -->
    <menu-item
      :to="{name: 'admin_users'}"
      icon="manage_accounts"
      label="Пользователи"
    />
    <menu-item
      :to="{name: 'admin_parse_settings'}"
      icon="memory"
      label="Парсеры"
    />
    <q-separator />
  </template>

  <template v-if="userRole == TUserRole.manager">
    <!-- Manager -->
  </template>

  <template v-if="true">
    <!-- Common -->
    <menu-item
      :to="{name: 'user_products'}"
      icon="inventory"
      label="Товары"
    />
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
import MenuItem from './MenuItem.vue'
import { storeToRefs } from 'pinia';
import { TUserRole, useAuthStore } from 'src/stores/auth';


const store = useAuthStore()
const {userRole} = storeToRefs(store)

</script>
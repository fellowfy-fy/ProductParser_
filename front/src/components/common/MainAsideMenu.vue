<template>
  <menu-item
    :to="homePage"
    icon="home"
    label="Главная"
    exact
  />

  <template v-if="1">
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
    <q-item
      clickable
      :to="{name: 'user_prices'}"
    >
      <q-item-section avatar>
        <q-icon
          name="currency_ruble"
        />
      </q-item-section>
      <q-item-section>
        Цены товаров
      </q-item-section>
    </q-item>
  </template>

  <template v-if="userRole == TUserRole.admin">
    <q-separator />
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
    <menu-item
      :to="{name: 'admin_preferences'}"
      icon="settings"
      label="Настройки"
    />
  </template>

  <template v-if="userRole == TUserRole.manager">
    <!-- Manager -->
  </template>
</template>

<script setup lang="ts">
import MenuItem from './MenuItem.vue'
import { storeToRefs } from 'pinia';
import { TUserRole, useAuthStore } from 'src/stores/auth';
import { computed } from 'vue';


const store = useAuthStore()
const {userRole} = storeToRefs(store)

const homePage = computed(() => {
  if (userRole.value == TUserRole.admin){
    return {"name": "manager_index"}
  }
  else if (userRole.value == TUserRole.manager){
    return {"name": "manager_index"}
  }
  return {"name": "user_index"}
})

</script>
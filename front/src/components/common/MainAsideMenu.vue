<template>
  <template v-if="userRole == 'admin'">
    <!--  -->
  </template>
  <template v-if="userRole == 'manager'">
    <!--  -->
  </template>
  <template>
    <!--  -->
  </template>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { useAuthStore } from 'src/stores/auth';


const store = useAuthStore()
const {userRole} = storeToRefs(store)

</script>
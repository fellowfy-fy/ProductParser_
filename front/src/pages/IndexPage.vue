<template>
  <div>
    <!--  -->
  </div>
</template>

<script lang="ts" setup>
import { useAuthStore } from "src/stores/auth"
import { nextTick, onMounted } from "vue"
import { useRouter } from "vue-router"

const store = useAuthStore()
const $router = useRouter()

onMounted(() => {
  void nextTick(() => {

    switch (store.userRole) {
      case "manager":
        void $router.push({ name: "manager_index" })

        break

      default:
        void $router.push({ name: "manager_index" })
        break
    }
  })
})
</script>

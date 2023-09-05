<template>
  <q-page class="flex flex-center"> Главная</q-page>
</template>

<script>
import { useAuthStore } from 'src/stores/auth';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'IndexPage',
  components: {},
  data() {
    const storeAuth = useAuthStore();
    return {
      storeAuth,
    };
  },
  methods: {},
  computed: {
    user() {
      return this.storeAuth.account;
    },
  },
});
</script>

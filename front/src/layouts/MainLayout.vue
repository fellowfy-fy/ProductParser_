<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-toolbar-title> </q-toolbar-title>

        <!-- <div>Quasar v{{ $q.version }}</div> -->
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      :width="220"
      :breakpoint="1200"
      show-if-above
      bordered
    >
      <q-list class="flex column full-height">
        <!-- <q-item-label header>База рецептов</q-item-label> -->

        <q-item class="cursor-pointer">
          <q-item-section avatar>
            <q-icon name="account_circle" size="lg"></q-icon>
          </q-item-section>
          <q-item-section>
            {{ userReadable }}
          </q-item-section>

          <q-menu anchor="bottom middle" self="top middle" auto-close>
            <q-list dense>
              <q-item class="justify-center text-negative" clickable @click="askLogout">
                Выйти
              </q-item>
            </q-list>
          </q-menu>
        </q-item>

        <q-separator class="q-mb-md" />

        <q-item :to="{ name: 'index' }"
          ><q-item-section avatar><q-icon name="home"></q-icon></q-item-section>
          <q-item-section>Главная</q-item-section>
        </q-item>

        <q-space />

        <q-item clickable @click="toggleDark">
          <q-item-section avatar>
            <q-icon :name="darkIcon()"></q-icon>
          </q-item-section>
          <q-item-section> Тёмная тема </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { useQuasar } from 'quasar';
import { useAuthStore } from 'src/stores/auth';
import { defineComponent, ref } from 'vue';

const darkModes = ['auto', true, false];

export default defineComponent({
  name: 'MainLayout',

  components: {},

  setup() {
    const leftDrawerOpen = ref(false);
    const store = useAuthStore();
    const $q = useQuasar();

    const preferedMode = $q.localStorage.getItem('preferedMode');

    if (preferedMode !== null) {
      $q.dark.set(preferedMode);
    }

    return {
      store,
      leftDrawerOpen,
      darkModes,

      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
      toggleDark() {
        let mode = $q.dark.mode;
        let idxCurr = darkModes.indexOf(mode);
        let idxNew = idxCurr + 1;
        if (idxNew >= darkModes.length) {
          idxNew = 0;
        }
        let newMode = darkModes[idxNew];
        // set
        $q.dark.set(newMode);
        $q.localStorage.set('preferedMode', newMode);
      },
      darkIcon() {
        let mode = $q.dark.mode;
        switch (mode) {
          case false:
            return 'light_mode';
          case true:
            return 'dark_mode';
          case 'auto':
            return 'brightness_auto';
          default:
            return 'dark_mode';
        }
      },
    };
  },

  methods: {
    askLogout() {
      this.$q
        .dialog({
          title: 'Подтверждение',
          message: 'Вы уверены что хотите выйти из аккаунта?',
          cancel: true,
          persistent: true,
        })
        .onOk(() => {
          this.logout();
        });
    },
    logout() {
      this.store.logout();
      this.$router.push({ name: 'login' }).catch(() => {});
    },
  },

  computed: {
    user() {
      return this.store.account;
    },
    userReadable() {
      if (!this.user) {
        return;
      }
      return this.user.first_name
        ? this.user.first_name + ' ' + this.user.last_name
        : '@' + this.user.username;
    },
  },
});
</script>

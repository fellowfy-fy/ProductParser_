<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title />

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
            <q-icon
              name="account_circle"
              size="lg"
            />
          </q-item-section>
          <q-item-section>
            {{ userReadable }}
            <q-item-label caption>
              {{ userRole }}
            </q-item-label>
          </q-item-section>

          <q-menu
            anchor="bottom middle"
            self="top middle"
            auto-close
          >
            <q-list dense>
              <q-item
                class="justify-center text-negative"
                clickable
                @click="askLogout"
              >
                Выйти
              </q-item>
            </q-list>
          </q-menu>
        </q-item>

        <q-separator class="q-mb-md" />

        <main-aside-menu />

        <q-space />

        <q-item
          clickable
          @click="toggleDark"
        >
          <q-item-section avatar>
            <q-icon :name="darkIcon" />
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

<script lang="ts" setup>
import { UserRoleReadable } from "src/Modules/StaticTranslate"
import MainAsideMenu from "../components/common/MainAsideMenu.vue"
import { useQuasar } from "quasar"
import { useAuthStore } from "src/stores/auth"
import { computed, ref } from "vue"
import { useRouter } from "vue-router"

const store = useAuthStore()
const $q = useQuasar()
const $router = useRouter()

type darkMode = "auto" | true | false

const darkModes:darkMode[] = ["auto", true, false]
const leftDrawerOpen = ref(false)
const preferredMode = $q.localStorage.getItem("preferredMode") as darkMode

if (preferredMode !== null) {
  $q.dark.set(preferredMode)
}

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
function toggleDark() {
  const mode = $q.dark.mode
  const idxCurr = darkModes.indexOf(mode)
  let idxNew = idxCurr + 1
  if (idxNew >= darkModes.length) {
    idxNew = 0
  }
  const newMode:darkMode = darkModes[idxNew]
  // set
  $q.dark.set(newMode)
  $q.localStorage.set("preferredMode", newMode)
}
const darkIcon = computed(() => {
  const mode = $q.dark.mode
  switch (mode) {
    case false:
      return "light_mode"
    case true:
      return "dark_mode"
    case "auto":
      return "brightness_auto"
    default:
      return "dark_mode"
  }
})

const user = computed(() => {
  return store.account
})
const userReadable = computed(() => {
  if (!user.value) {
    return
  }
  return user.value.first_name ? user.value.first_name + " " + String(user.value.last_name) : "@" + user.value.username
})

const userRole = computed(() => {
  if (!user.value){
    return
  }
  return UserRoleReadable(user.value.role)
})

function askLogout() {
  $q.dialog({
    title: "Подтверждение",
    message: "Вы уверены что хотите выйти из аккаунта?",
    cancel: true,
    persistent: true,
  }).onOk(() => {
    logout()
    void $router.go(0)
  })
}
function logout() {
  void store.logout()
}
</script>

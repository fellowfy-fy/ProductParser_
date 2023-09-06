import { defineStore } from "pinia"
import { LocalStorage } from "quasar"
import { AuthService, AuthToken, OpenAPI, CustomUser, UsersService } from "src/client"
import { UserRoleFromNum } from "src/modules/StaticTranslate"
import { storeShortcut } from "src/modules/StoreCrud"

// eslint-disable-next-line @typescript-eslint/require-await
const getToken = async () => {
  return localStorage.getItem("authToken") || ""
}

OpenAPI.TOKEN = getToken

const cachedPermissions: string[] = LocalStorage.getItem("cachedPermissions") || []

export type TUserRole = "user" | "admin" | "manager"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    authToken: localStorage.getItem("authToken"),
    user: null as CustomUser | null,
    account: null as CustomUser | null,
    notifications: null as Notification[] | null,
    pageLoading: false,
  }),

  getters: {
    isAuthenticated(state) {
      return !!state.authToken
    },
    userRole(state): TUserRole {
      const acc = state.account
      return UserRoleFromNum(acc)
    },
    isAdmin(state) {
      return state.account?.is_staff
    },
    // permissions(state): Array<string> {
    //   return state.account?.permissions || []
    // },
  },

  actions: {
    // hasPerm(perm: string): boolean {
    //   if (this.account?.is_superuser) {
    //     return true
    //   }
    //   const perms = this.permissions.length > 0 ? this.permissions : cachedPermissions
    //   return perms.includes(perm)
    // },
    setToken(token: string): void {
      localStorage.setItem("authToken", token)
      this.authToken = token
    },
    deleteToken(): void {
      localStorage.removeItem("authToken")
    },

    //
    async logout(): Promise<void> {
      return new Promise((resolve) => {
        this.authToken = null
        this.deleteToken()
        resolve()
      })
    },

    async loadUser(id: number): Promise<CustomUser> {
      return storeShortcut({
        promise: UsersService.usersRetrieve({ id }),
        setValue: (resp: CustomUser) => {
          this.user = resp
        },
      })
    },

    async updateUser(id: number, payload: CustomUser): Promise<CustomUser> {
      return storeShortcut({
        promise: UsersService.usersPartialUpdate({ id, requestBody: payload }),
        setValue: (resp: CustomUser) => {
          this.user = resp
        },
      })
    },

    async createUser(payload: CustomUser): Promise<CustomUser> {
      return storeShortcut({
        promise: UsersService.usersCreate({ requestBody: payload }),
        setValue: (resp: CustomUser) => {
          this.user = resp
        },
      })
    },

    async loadAccountInfo(): Promise<CustomUser> {
      return storeShortcut({
        promise: UsersService.usersCurrentRetrieve(),
        setValue: (user: CustomUser) => {
          this.account = user
        },
      })
    },

    async login(payload: AuthToken): Promise<AuthToken> {
      return new Promise((resolve, reject) => {
        AuthService.authTokenCreate({ formData: payload })
          .then((resp) => {
            const token = resp.token
            this.setToken(token)

            resolve(resp)
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
  },
})

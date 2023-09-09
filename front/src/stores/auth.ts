import { defineStore } from "pinia"
import { LocalStorage } from "quasar"
import { AuthService, AuthToken, OpenAPI, CustomUser, UsersService, PaginatedCustomUserList } from "src/client"
import { storeShortcut } from "src/Modules/StoreCrud"

// eslint-disable-next-line @typescript-eslint/require-await
const getToken = async () => {
  return localStorage.getItem("authToken") || ""
}

OpenAPI.TOKEN = getToken

export enum TUserRole {
  user = 1,
  manager = 2,
  admin = 3,
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    authToken: localStorage.getItem("authToken"),
    user: null as CustomUser | null,
    users: null as CustomUser[] | null,
    account: null as CustomUser | null,
    notifications: null as Notification[] | null,
    pageLoading: false,

    cachedAccount: LocalStorage.getItem("cachedAccount", null) as unknown as CustomUser | null,
  }),

  getters: {
    isAuthenticated(state) {
      return !!state.authToken
    },
    userRole(state): TUserRole {
      const acc = state.account
      const accCached = state.cachedAccount
      return (acc?.role as TUserRole | undefined) || (accCached?.role as TUserRole | undefined) || TUserRole.user
    },
    isAdmin(state) {
      return state.account?.is_staff || (state.account?.role && state.account?.role >= 3)
    },
    isManager(state) {
      return state.account?.role && state.account?.role >= 2
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

    async loadUser(id: number, noSave = false): Promise<CustomUser> {
      return storeShortcut({
        promise: UsersService.usersRetrieve({ id }),
        setValue: (resp: CustomUser) => {
          if (!noSave) {
            this.user = resp
          }
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
    async deleteUser(id: number): Promise<CustomUser> {
      return storeShortcut({
        promise: UsersService.usersDestroy({ id }),
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
          LocalStorage.set("cachedAccount", user)
        },
      })
    },
    async loadUsers(payload: object): Promise<PaginatedCustomUserList> {
      return storeShortcut({
        promise: UsersService.usersList(payload),
        setValue: (resp: PaginatedCustomUserList) => {
          this.users = resp.results as CustomUser[]
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

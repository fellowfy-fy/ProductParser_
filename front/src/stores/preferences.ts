import { defineStore } from "pinia"
import { storeShortcut } from "src/Modules/StoreCrud"
import { GlobalPreference, GlobalService, PaginatedGlobalPreferenceList } from "src/client"

export const usePreferencesStore = defineStore("preferences", {
  state: () => ({
    preference: null as GlobalPreference | null,
    preferences: null as GlobalPreference[] | null,
  }),

  getters: {},

  actions: {
    loadPreferences(payload: object): Promise<PaginatedGlobalPreferenceList> {
      return storeShortcut({
        promise: GlobalService.globalList(payload),
        setValue: (resp: PaginatedGlobalPreferenceList) => {
          this.preferences = resp.results as []
        },
      })
    },
    loadPreference(id: number): Promise<GlobalPreference> {
      return storeShortcut({
        promise: GlobalService.globalRetrieve({ id }),
        setValue: (resp: GlobalPreference) => {
          this.preference = resp
        },
      })
    },
    updatePreference(id: number, payload: GlobalPreference): Promise<GlobalPreference> {
      return storeShortcut({
        promise: GlobalService.globalUpdate({ id, requestBody: payload }),
        setValue: (resp: GlobalPreference) => {
          this.preference = resp
        },
      })
    },
  },
})

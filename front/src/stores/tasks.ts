import { defineStore } from "pinia"
import { PaginatedParseTaskList, PaginatedSiteParseSettingsList, ParseSettingsService, ParseTask, ParseTaskService, SiteParseSettings } from "src/client"
import { storeShortcut } from "src/modules/StoreCrud"

export const useTasksStore = defineStore("tasks", {
  state: () => ({
    parseTask: null as ParseTask | null,
    parseTasks: null as ParseTask[] | null,
    parseSetting: null as SiteParseSettings | null,
    parseSettings: null as SiteParseSettings[] | null,
  }),

  getters: {},

  actions: {
    loadParseTasks(payload: object): Promise<PaginatedParseTaskList> {
      return storeShortcut({
        promise: ParseTaskService.parseTaskList(payload),
        setValue: (resp: PaginatedParseTaskList) => {
          this.parseTasks = resp.results as []
        },
      })
    },
    loadParseTask(id: number): Promise<ParseTask> {
      return storeShortcut({
        promise: ParseTaskService.parseTaskRetrieve({ id }),
        setValue: (resp: ParseTask) => {
          this.parseTask = resp
        },
      })
    },
    deleteParseTask(id: number): Promise<ParseTask> {
      return storeShortcut({
        promise: ParseTaskService.parseTaskDestroy({ id }),
        setValue: () => {
          this.parseTask = null
        },
      })
    },
    createParseTask(payload: ParseTask): Promise<ParseTask> {
      return storeShortcut({
        promise: ParseTaskService.parseTaskCreate({ requestBody: payload }),
        setValue: (resp: ParseTask) => {
          this.parseTask = resp
        },
      })
    },
    updateParseTask(id: number, payload: ParseTask): Promise<ParseTask> {
      return storeShortcut({
        promise: ParseTaskService.parseTaskUpdate({ id, requestBody: payload }),
        setValue: (resp: ParseTask) => {
          this.parseTask = resp
        },
      })
    },
    // Settings
    loadParseSettings(payload: object): Promise<PaginatedSiteParseSettingsList> {
      return storeShortcut({
        promise: ParseSettingsService.parseSettingsList(payload),
        setValue: (resp: PaginatedSiteParseSettingsList) => {
          this.parseSettings = resp.results as []
        },
      })
    },
    loadParseSettingsItem(id: number): Promise<SiteParseSettings> {
      return storeShortcut({
        promise: ParseSettingsService.parseSettingsRetrieve({ id }),
        setValue: (resp: SiteParseSettings) => {
          this.parseSetting = resp
        },
      })
    },
    deleteParseSettings(id: number): Promise<SiteParseSettings> {
      return storeShortcut({
        promise: ParseSettingsService.parseSettingsDestroy({ id }),
        setValue: () => {
          this.parseSetting = null
        },
      })
    },
    createParseSettings(payload: SiteParseSettings): Promise<SiteParseSettings> {
      return storeShortcut({
        promise: ParseSettingsService.parseSettingsCreate({ requestBody: payload }),
        setValue: (resp: SiteParseSettings) => {
          this.parseSetting = resp
        },
      })
    },
    updateParseSettings(id: number, payload: SiteParseSettings): Promise<SiteParseSettings> {
      return storeShortcut({
        promise: ParseSettingsService.parseSettingsUpdate({ id, requestBody: payload }),
        setValue: (resp: SiteParseSettings) => {
          this.parseSetting = resp
        },
      })
    },
  },
})

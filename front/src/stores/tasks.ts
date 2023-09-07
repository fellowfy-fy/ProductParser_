import { defineStore } from "pinia"
import { PaginatedParseTaskList, ParseTask, ParseTaskService } from "src/client"
import { storeShortcut } from "src/modules/StoreCrud"

export const useTasksStore = defineStore("tasks", {
  state: () => ({
    parseTask: null as ParseTask | null,
    parseTasks: null as ParseTask[] | null,
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
  },
})

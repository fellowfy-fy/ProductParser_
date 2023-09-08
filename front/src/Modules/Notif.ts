import { Notify } from "quasar"

export function notifySaved() {
  Notify.create({
    type: "positive",
    message: "Успешно сохранено",
  })
}

export function notifyTaskStatusUpdated() {
  Notify.create({
    type: "positive",
    message: "Статус задачи успешно изменен",
  })
}

export function notifyDeleted() {
  Notify.create({
    type: "positive",
    icon: "delete",
    message: "Успешно удалено",
  })
}

export function promiseFunc(promise: Promise<unknown>, func: CallableFunction) {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-return
  void promise.then(() => func())
}

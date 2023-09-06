import { Notify } from "quasar"

export function notifySaved() {
  Notify.create({
    type: "positive",
    message: "Успешно сохранено",
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
  void promise.then(() => func())
}

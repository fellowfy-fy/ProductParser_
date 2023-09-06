import { date } from "quasar"

export function formatDate(dt: Date | string): string {
  return date.formatDate(dt, "YYYY.MM.DD")
}

export function formatDateTime(dt: Date | string): string {
  return date.formatDate(dt, "YYYY.MM.DD hh:mm")
}

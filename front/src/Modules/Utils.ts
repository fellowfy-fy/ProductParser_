import { date } from "quasar"

export function formatDate(dt: Date | string): string {
  return date.formatDate(dt, "YYYY.MM.DD")
}

export function formatDateTime(dt: Date | string): string {
  return date.formatDate(dt, "YYYY.MM.DD HH:mm")
}

export function formatDateTimeSeconds(dt: Date | string): string {
  return date.formatDate(dt, "DD.MM HH:mm:ss")
}

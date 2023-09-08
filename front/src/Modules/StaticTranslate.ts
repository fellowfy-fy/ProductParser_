import { CustomUser, ShortUser } from "src/client"
import { TUserRole } from "src/stores/auth"

export const TaskStatus = new Map([
  [1, "Создана"],
  [2, "В работе"],
  [3, "Отменена"],
  [4, "Пауза"],
  [5, "Остановлена"],
  [6, "Настройка"],
])

export function UserRoleFromNum(role: TUserRole) {
  switch (role) {
    case 1:
      return "user"
    case 2:
      return "manager"
    case 3:
      return "admin"

    default:
      return "admin"
  }
}

export function UserRoleReadable(role: number | undefined): string {
  switch (role) {
    case TUserRole.admin:
      return "Администратор"
    case TUserRole.manager:
      return "Руководитель"

    default:
      return "Сотрудник"
  }
}

export function userReadable(user: CustomUser | ShortUser | null): string {
  if (!user) {
    return "-"
  }
  if (user.first_name) {
    return [user.first_name, user.last_name, user.middle_name].join(" ")
  }
  return "@" + user.username
}

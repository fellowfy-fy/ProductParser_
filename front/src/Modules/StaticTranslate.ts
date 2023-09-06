import { TUserRole } from "src/stores/auth"

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

import { CustomUser } from "src/client"

export function UserRoleFromNum(acc: CustomUser | null) {
  if (!acc) {
    return "user"
  }
  switch (acc.role) {
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

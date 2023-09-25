export const ruleRequired = (val: string) => !!val || "Обязательное поле"
export const ruleValidEmail = (val: string) => {
  const emailPattern = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/
  return emailPattern.test(val) || "Введите валидный email адрес "
}

function isValidURL(urlString: string) {
  try {
    return Boolean(new URL(urlString))
  } catch (e) {
    return false
  }
}

export const ruleValidURL = (val: string) => {
  return isValidURL(val) || "Введите валидный URL "
}
export const ruleValidJSON = (val: string) => {
  return isJsonString(val) || "Введите валидный JSON"
}

function isJsonString(str: string): boolean {
  let parsed: unknown
  try {
    parsed = JSON.parse(str)
  } catch (e) {
    return false
  }
  return typeof parsed === "object"
}

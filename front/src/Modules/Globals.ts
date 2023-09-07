export const ruleRequired = (val: string) => !!val || "Обязательное поле"
export const ruleValidEmail = (val: string) => {
  const emailPattern = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/
  return emailPattern.test(val) || "Введите валидный email адрес "
}
export const ruleValidURL = (val: string) => {
  const pattern = new RegExp(
    "^(https?:\\/\\/)?" + // protocol
      "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // domain name
      "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
      "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
      "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
      "(\\#[-a-z\\d_]*)?$",
    "i"
  ) // fragment locator

  // Remove django template items
  const clearRegex = new RegExp("{[{%][^}]*[%}]}")
  const valClean = val.replace(clearRegex, "")

  return pattern.test(valClean) || "Введите валидный URL "
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

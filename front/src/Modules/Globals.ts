export const ruleRequired = (val: string) => !!val || "Обязательное поле"
export const ruleValidEmail = (val: string) => {
  const emailPattern = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/
  return emailPattern.test(val) || "Введите верный email адрес "
}
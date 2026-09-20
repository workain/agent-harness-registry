// The form's constraints live in index.html as plain HTML attributes (`required`,
// `type="email"`, `pattern`). This file reads them back through the browser's own
// Constraint Validation API and turns them into messages the page can render inline.
// That is the whole job: no form-validation library, for two fields.

const MESSAGES = {
  valueMissing: 'Заполните это поле',
  typeMismatch: 'Проверьте адрес почты',
  patternMismatch: 'Проверьте адрес почты',
}

/**
 * @param {HTMLFormElement} form
 * @returns {{ field: HTMLInputElement, message: string }[]} empty when the form may be sent
 */
export function validateForm(form) {
  const errors = []
  for (const field of form.querySelectorAll('input')) {
    if (field.checkValidity()) continue
    const reason = Object.keys(MESSAGES).find((key) => field.validity[key])
    errors.push({ field, message: MESSAGES[reason] ?? 'Проверьте это поле' })
  }
  return errors
}

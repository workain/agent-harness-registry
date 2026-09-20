import { test, expect, type Page } from '@playwright/test'

const FORM_ENDPOINT = 'https://formspree.io/f/**'

/**
 * Intercepts the external form service so no test ever posts to the real internet,
 * and returns a counter of how many times the page tried to.
 */
async function stubFormEndpoint(page: Page) {
  const attempts: string[] = []
  await page.route(FORM_ENDPOINT, async (route) => {
    attempts.push(route.request().method())
    await route.fulfill({ status: 200, contentType: 'text/html', body: 'ok' })
  })
  return attempts
}

test('the page shows a name field, an email field and a submit button', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByLabel('Имя')).toBeVisible()
  await expect(page.getByLabel('Email')).toBeVisible()
  await expect(page.getByRole('button', { name: 'Отправить заявку' })).toBeVisible()
})

test('an empty form is not submitted, and says which fields are missing', async ({ page }) => {
  const attempts = await stubFormEndpoint(page)
  await page.goto('/')

  await page.getByRole('button', { name: 'Отправить заявку' }).click()

  // The point of the whole test file: nothing left the page.
  await expect(page).toHaveURL('/')
  expect(attempts).toEqual([])

  await expect(page.locator('.error[data-error-for="name"]')).toHaveText('Заполните это поле')
  await expect(page.locator('.error[data-error-for="email"]')).toHaveText('Заполните это поле')
  await expect(page.getByLabel('Имя')).toBeFocused()
})

test('an address with no @ at all is not submitted (caught by type="email")', async ({ page }) => {
  const attempts = await stubFormEndpoint(page)
  await page.goto('/')

  await page.getByLabel('Имя').fill('Анна')
  await page.getByLabel('Email').fill('anna-at-example')
  await page.getByRole('button', { name: 'Отправить заявку' }).click()

  await expect(page).toHaveURL('/')
  expect(attempts).toEqual([])

  await expect(page.locator('.error[data-error-for="email"]')).toHaveText('Проверьте адрес почты')
})

test('an address type="email" accepts but our pattern rejects is not submitted', async ({ page }) => {
  const attempts = await stubFormEndpoint(page)
  await page.goto('/')

  // `a@b` is a perfectly valid address as far as type="email" is concerned. It is the
  // `pattern` attribute, and only that attribute, that insists on a dot in the domain --
  // so this is the one test that goes red if `pattern` is dropped from index.html.
  await page.getByLabel('Имя').fill('Анна')
  await page.getByLabel('Email').fill('a@b')
  await page.getByRole('button', { name: 'Отправить заявку' }).click()

  await expect(page).toHaveURL('/')
  expect(attempts).toEqual([])

  await expect(page.locator('.error[data-error-for="email"]')).toHaveText('Проверьте адрес почты')
})

test('a filled-in form is sent to the external form service', async ({ page }) => {
  const attempts = await stubFormEndpoint(page)
  await page.goto('/')

  await page.getByLabel('Имя').fill('Анна')
  await page.getByLabel('Email').fill('anna@example.com')
  await page.getByRole('button', { name: 'Отправить заявку' }).click()

  // Without this case, a validate.js that rejected everything would still look green.
  await expect.poll(() => attempts).toEqual(['POST'])
})

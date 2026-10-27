// Iniciar sesión, cerrar sesión y volver a entrar; el registro a medias.
import { expect, test } from '@playwright/test';
import { CLAVE, captura, correoNuevo, crearCuentaCompleta, escribirCodigo, leerCodigo } from './ayudas';

test('iniciar sesión, cerrar sesión y volver a entrar', async ({ page }) => {
  const correo = correoNuevo('sesion');
  await crearCuentaCompleta(page, correo, 'Docente');

  // recargar la página no pierde la sesión
  await page.reload();
  await expect(page.getByRole('heading', { name: 'Mis experiencias' })).toBeVisible();

  await page.getByRole('button', { name: 'Cerrar sesión' }).click();
  await expect(page.getByRole('heading', { name: 'Bienvenido de vuelta' })).toBeVisible();
  // sin sesión, el Dashboard no se puede abrir
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Bienvenido de vuelta' })).toBeVisible();

  // contraseña equivocada: el mensaje genérico
  await page.getByLabel('Correo electrónico').fill(correo);
  await page.getByLabel('Contraseña', { exact: true }).fill('Equivocada9');
  await page.getByRole('button', { name: 'Iniciar sesión' }).click();
  await expect(page.getByText('Correo o contraseña incorrectos.')).toBeVisible();
  await captura(page, '014-error-credenciales');

  await page.getByLabel('Contraseña', { exact: true }).fill(CLAVE);
  await page.getByRole('button', { name: 'Iniciar sesión' }).click();
  await expect(page.getByRole('heading', { name: 'Mis experiencias' })).toBeVisible();
  await expect(page.getByTestId('nombre-sidebar')).toHaveText('Ana María Pérez Gómez');
});

test('un registro a medias retoma donde quedó al iniciar sesión (ADR-035)', async ({ page }) => {
  const correo = correoNuevo('amedias');
  await page.goto('/crear-cuenta');
  await page.getByLabel('Correo electrónico').fill(correo);
  await page.getByLabel('Contraseña', { exact: true }).fill(CLAVE);
  await page.getByRole('button', { name: 'Crear cuenta' }).click();
  await expect(page.getByRole('heading', { name: 'Verifica tu correo' })).toBeVisible();

  // se va sin verificar; al volver a entrar, retoma en 015
  await page.getByRole('button', { name: 'Volver' }).click();
  await expect(page.getByRole('heading', { name: 'Crea tu cuenta' })).toBeVisible();
  // "Volver" devuelve el correo y la contraseña ya escritos (015 §7)
  await expect(page.getByLabel('Correo electrónico')).toHaveValue(correo);
  await expect(page.getByLabel('Contraseña', { exact: true })).toHaveValue(CLAVE);
  await page.getByText('Inicia sesión', { exact: true }).click();
  await page.getByRole('button', { name: 'Iniciar sesión' }).click();
  await expect(page.getByRole('heading', { name: 'Verifica tu correo' })).toBeVisible();

  // verifica, y se va sin elegir rol (cierra la pestaña: la sesión se borra)
  await escribirCodigo(page, await leerCodigo(correo, 1));
  await page.getByRole('button', { name: 'Verificar' }).click();
  await expect(page.getByRole('heading', { name: 'Completa tu perfil' })).toBeVisible();
  await page.evaluate(() => sessionStorage.clear());
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Bienvenido de vuelta' })).toBeVisible();
  await page.getByLabel('Correo electrónico').fill(correo);
  await page.getByLabel('Contraseña', { exact: true }).fill(CLAVE);
  await page.getByRole('button', { name: 'Iniciar sesión' }).click();
  // verificada sin rol → retoma en Completa tu perfil
  await expect(page.getByRole('heading', { name: 'Completa tu perfil' })).toBeVisible();
});

test('correo con formato inválido y Google sin configurar', async ({ page }) => {
  await page.goto('/iniciar-sesion');
  await page.getByLabel('Correo electrónico').fill('ana@');
  await page.getByLabel('Contraseña', { exact: true }).click();
  await expect(page.getByLabel('Correo electrónico')).toHaveAttribute('aria-invalid', 'true');
  await page.getByRole('button', { name: 'Iniciar sesión' }).click();
  await expect(page.getByText('Escribe un correo válido.')).toBeVisible();
  await captura(page, '014-error-correo-invalido');

  await page.getByLabel('Correo electrónico').fill('');
  await page.getByRole('button', { name: 'Continuar con Google' }).click();
  await expect(page.getByText('El acceso con Google no está configurado en este servidor.')).toBeVisible();
  await captura(page, '014-google-no-configurado');
  await page.getByRole('button', { name: 'Continuar con Microsoft' }).click();
  await expect(page.getByText('El acceso con Microsoft no está configurado en este servidor.')).toBeVisible();
});

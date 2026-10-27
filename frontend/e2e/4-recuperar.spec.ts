// Recuperar la contraseña (018 → 015 → 019 → 014) y entrar con la nueva.
import { expect, test } from '@playwright/test';
import { CLAVE, captura, correoNuevo, crearCuentaCompleta, escribirCodigo, leerCodigo } from './ayudas';

test('recuperar la contraseña y entrar con la nueva', async ({ page }) => {
  const correo = correoNuevo('recupera');
  await crearCuentaCompleta(page, correo, 'Docente');
  await page.getByRole('button', { name: 'Cerrar sesión' }).click();

  await page.getByText('¿Olvidaste tu contraseña?').click();
  await expect(page.getByRole('heading', { name: '¿Olvidaste tu contraseña?' })).toBeVisible();
  const enviar = page.getByRole('button', { name: 'Enviar código' });
  await expect(enviar).toBeDisabled();
  await page.getByLabel('Correo electrónico').fill('ana@');
  await page.getByLabel('Correo electrónico').blur();
  await expect(page.getByText('Escribe un correo válido.')).toBeVisible();
  await captura(page, '018-error-correo');
  await page.getByLabel('Correo electrónico').fill(correo);
  await expect(enviar).toBeEnabled();
  await captura(page, '018-recupera-tu-contrasena');
  await enviar.click();

  // 015, flujo de recuperación (el primer código de recuperación de este correo)
  await expect(page.getByRole('heading', { name: 'Verifica tu correo' })).toBeVisible();
  await captura(page, '015-recuperacion');
  await escribirCodigo(page, await leerCodigo(correo, 2));
  await page.getByRole('button', { name: 'Verificar' }).click();

  // 019
  await expect(page.getByRole('heading', { name: 'Crea una nueva contraseña' })).toBeVisible();
  const guardar = page.getByRole('button', { name: 'Guardar' });
  await page.getByLabel('Nueva contraseña').fill('nuevaclave');
  await expect(guardar).toBeDisabled();
  await page.getByLabel('Nueva contraseña').fill('NuevaClave9');
  await expect(guardar).toBeEnabled();
  await captura(page, '019-nueva-contrasena');
  await guardar.click();

  // 014 con la confirmación
  await expect(page.getByText('Contraseña actualizada. Inicia sesión.')).toBeVisible();
  await captura(page, '014-confirmacion-contrasena-actualizada');
  await page.getByLabel('Correo electrónico').fill(correo);
  await page.getByLabel('Contraseña', { exact: true }).fill(CLAVE);
  await page.getByRole('button', { name: 'Iniciar sesión' }).click();
  await expect(page.getByText('Correo o contraseña incorrectos.')).toBeVisible();
  await page.getByLabel('Contraseña', { exact: true }).fill('NuevaClave9');
  await page.getByRole('button', { name: 'Iniciar sesión' }).click();
  await expect(page.getByRole('heading', { name: 'Mis experiencias' })).toBeVisible();
});

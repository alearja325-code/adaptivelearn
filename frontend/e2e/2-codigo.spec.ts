// Ventana 015: un código equivocado y el reenvío con su espera de 30 s.
import { expect, test } from '@playwright/test';
import { CLAVE, captura, correoNuevo, escribirCodigo, leerCodigo } from './ayudas';

test('un código equivocado, y el reenvío después de 30 segundos', async ({ page }) => {
  const correo = correoNuevo('codigo');
  await page.goto('/crear-cuenta');
  await page.getByLabel('Correo electrónico').fill(correo);
  await page.getByLabel('Contraseña', { exact: true }).fill(CLAVE);
  await page.getByRole('button', { name: 'Crear cuenta' }).click();
  const primero = await leerCodigo(correo, 1);

  // código equivocado: el texto de la spec, las cajas en rojo y el valor intacto
  const malo = primero === '000000' ? '111111' : '000000';
  await escribirCodigo(page, malo);
  await page.getByRole('button', { name: 'Verificar' }).click();
  await expect(page.getByText('Código incorrecto. Revisa que esté bien escrito.')).toBeVisible();
  await expect(page.getByLabel('Dígito 1')).toHaveValue(malo[0]);
  await captura(page, '015-codigo-incorrecto');

  // antes de 30 s, "Reenviar" cuenta y no se puede usar
  await expect(page.getByText(/^Reenviar \(00:[0-9]{2}\)$/)).toBeVisible();
  await expect(page.getByRole('button', { name: 'Reenviar' })).toHaveCount(0);
  await page.waitForTimeout(31_000);
  await expect(page.getByRole('button', { name: 'Reenviar' })).toBeVisible();
  await captura(page, '015-reenviar-activo');
  await page.getByRole('button', { name: 'Reenviar' }).click();
  await expect(page.getByText('Reenviar (00:30)')).toBeVisible();

  // el código nuevo sirve
  const segundo = await leerCodigo(correo, 2);
  for (let i = 1; i <= 6; i++) await page.getByLabel(`Dígito ${i}`).fill('');
  await escribirCodigo(page, segundo);
  await page.getByRole('button', { name: 'Verificar' }).click();
  await expect(page.getByRole('heading', { name: 'Completa tu perfil' })).toBeVisible();
});

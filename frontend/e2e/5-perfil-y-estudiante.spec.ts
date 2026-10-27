// Editar el perfil en la ventana 026; elegir "Estudiante" y su Dashboard vacío.
import { expect, test } from '@playwright/test';
import { captura, correoNuevo, crearCuentaCompleta, fotoPng } from './ayudas';

test('editar el perfil en la ventana 026', async ({ page }) => {
  await crearCuentaCompleta(page, correoNuevo('perfil'), 'Docente');
  await page.getByRole('button', { name: 'Editar mi perfil' }).click();
  const modal = page.getByRole('dialog', { name: 'Mi perfil' });
  await expect(modal.getByLabel('Nombres')).toHaveValue('Ana María');
  const guardar = modal.getByRole('button', { name: 'Guardar cambios' });
  await expect(guardar).toBeDisabled(); // sin cambios
  await captura(page, '026-mi-perfil');

  await modal.getByLabel('Apellidos').fill('');
  await expect(guardar).toBeDisabled(); // apellidos vacíos
  await modal.getByLabel('Apellidos').fill('Pérez Ruiz');
  await modal.getByTestId('entrada-foto').setInputFiles(fotoPng());
  await expect(guardar).toBeEnabled();
  await captura(page, '026-mi-perfil-con-cambios');
  // demora la respuesta para ver el Modal: Cargando (024) "Guardando tu perfil..."
  await page.route('**/auth/profile', async (ruta) => {
    if (ruta.request().method() === 'PATCH') await new Promise((r) => setTimeout(r, 1000));
    await ruta.continue();
  });
  await guardar.click();
  await expect(page.getByText('Guardando tu perfil...')).toBeVisible();
  await captura(page, '024-cargando-guardando-perfil');

  // se cierra y el Sidebar se actualiza
  await expect(modal).toHaveCount(0);
  await expect(page.getByTestId('nombre-sidebar')).toHaveText('Ana María Pérez Ruiz');
  await expect(page.getByRole('button', { name: 'Editar mi perfil' }).locator('img')).toBeVisible();
  await captura(page, '001-dashboard-perfil-actualizado');

  // la X cierra sin guardar
  await page.getByRole('button', { name: 'Editar mi perfil' }).click();
  await modal.getByLabel('Nombres').fill('Otra');
  await modal.getByRole('button', { name: 'Cerrar' }).click();
  await expect(page.getByTestId('nombre-sidebar')).toHaveText('Ana María Pérez Ruiz');
});

test('elegir "Estudiante": su Dashboard vacío y el aviso de "Unirse con código"', async ({ page }) => {
  await crearCuentaCompleta(page, correoNuevo('estudiante'), 'Estudiante');
  await expect(page.getByText('Únete a una experiencia con el código de tu docente.')).toBeVisible();
  await expect(page.getByText('Aún no te has unido a ninguna experiencia.')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Completadas' })).toBeVisible();
  await expect(page.getByRole('button', { name: '+ Crear experiencia' })).toHaveCount(0);
  await captura(page, '001-dashboard-estudiante-vacio');
  await page.getByRole('button', { name: '→ Unirse con código' }).click();
  await expect(page.getByText('Unirse a una experiencia llega en la siguiente etapa.')).toBeVisible();
  await captura(page, '001-dashboard-estudiante-aviso-unirse');
});

test('a 1280 de ancho no se rompe: ni el Dashboard ni el modal se salen', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 800 });
  await crearCuentaCompleta(page, correoNuevo('ancho'), 'Docente');
  const sinDesborde = () => page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth);
  expect(await sinDesborde()).toBe(true);
  await page.getByRole('button', { name: '+ Crear experiencia' }).click();
  await page.getByRole('radio', { name: 'Matemáticas' }).click();
  await page.getByRole('button', { name: 'Continuar' }).click();
  await expect(page.getByTestId('lista-dba').locator('li[data-codigo]').first()).toBeVisible();
  expect(await sinDesborde()).toBe(true);
  const caja = await page.getByRole('dialog').boundingBox();
  expect(caja!.x).toBeGreaterThanOrEqual(0);
  expect(caja!.x + caja!.width).toBeLessThanOrEqual(1280);
  expect(caja!.y + caja!.height).toBeLessThanOrEqual(800);
  await captura(page, '003-paso2-a-1280');
});

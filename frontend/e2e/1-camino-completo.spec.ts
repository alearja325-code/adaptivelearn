// El camino completo del encargo 04 §1, en un navegador real, contra el
// backend real y MySQL: crear la cuenta → recibir el código → verificar →
// completar el perfil → elegir "Docente" → Dashboard → Crear experiencia →
// Paso 1 → Paso 2 (filtrar por grado, buscar, expandir CS-08-08) → Paso 3 → parar.
import { expect, test } from '@playwright/test';
import { CLAVE, captura, correoNuevo, escribirCodigo, fotoPng, leerCodigo } from './ayudas';

test('el camino completo, hasta el aviso del Paso 3', async ({ page }) => {
  const correo = correoNuevo('docente');

  // 014 — Crear cuenta
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Bienvenido de vuelta' })).toBeVisible();
  await captura(page, '014-iniciar-sesion');
  await page.getByText('Regístrate gratis').click();
  await page.getByLabel('Correo electrónico').fill(correo);
  await page.getByLabel('Contraseña', { exact: true }).fill(CLAVE);
  await captura(page, '014-crear-cuenta');
  await page.getByRole('button', { name: 'Crear cuenta' }).click();

  // 015 — el código llega a la consola del backend (sin MAIL_HOST)
  await expect(page.getByRole('heading', { name: 'Verifica tu correo' })).toBeVisible();
  await expect(page.getByTestId('correo-verificar')).toHaveText(correo);
  await expect(page.getByRole('button', { name: 'Verificar' })).toBeDisabled();
  await captura(page, '015-verifica-tu-correo');
  await escribirCodigo(page, await leerCodigo(correo));
  await page.getByRole('button', { name: 'Verificar' }).click();

  // 016 — perfil con foto
  await expect(page.getByRole('heading', { name: 'Completa tu perfil' })).toBeVisible();
  await captura(page, '016-completa-tu-perfil-vacio');
  await page.getByTestId('entrada-foto').setInputFiles({ name: 'foto.gif', mimeType: 'image/gif', buffer: Buffer.from('GIF89a') });
  await expect(page.getByText('Solo imágenes JPG o PNG, máximo 5 MB.')).toBeVisible();
  await captura(page, '016-error-foto');
  await page.getByTestId('entrada-foto').setInputFiles(fotoPng());
  await page.getByLabel('Nombres').fill('Ana María');
  await page.getByLabel('Apellidos').fill('Pérez Gómez');
  await captura(page, '016-completa-tu-perfil-lleno');
  await page.getByRole('button', { name: 'Continuar' }).click();

  // 017 — Docente
  await expect(page.getByRole('heading', { name: 'Elige tu rol' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Continuar' })).toBeDisabled();
  await page.getByRole('radio', { name: 'Soy Docente' }).click();
  await captura(page, '017-elige-tu-rol-docente');
  await page.getByRole('button', { name: 'Continuar' }).click();

  // 001 — Dashboard del docente, vacío, con su nombre y su foto
  await expect(page.getByRole('heading', { name: 'Mis experiencias' })).toBeVisible();
  await expect(page.getByText('Aún no has creado ninguna experiencia.')).toBeVisible();
  await expect(page.getByTestId('nombre-sidebar')).toHaveText('Ana María Pérez Gómez');
  await expect(page.getByRole('button', { name: 'Editar mi perfil' }).locator('img')).toBeVisible();
  await captura(page, '001-dashboard-docente-vacio');

  // 002 — Paso 1
  await page.getByRole('button', { name: '+ Crear experiencia' }).click();
  const modal = page.getByRole('dialog', { name: 'Crear experiencia' });
  await expect(modal.getByRole('radio')).toHaveCount(4);
  await expect(modal.getByRole('button', { name: 'Continuar' })).toBeDisabled();
  await captura(page, '002-paso1-sin-elegir');
  await modal.getByRole('radio', { name: 'Ciencias Sociales' }).click();
  await captura(page, '002-paso1-area-elegida');
  await modal.getByRole('button', { name: 'Continuar' }).click();

  // 003 — Paso 2: los DBA de Ciencias Sociales
  const lista = modal.getByTestId('lista-dba');
  await expect(lista.locator('li[data-codigo]')).toHaveCount(82);
  await captura(page, '003-paso2-lista');

  // filtrar por grado
  await modal.getByRole('button', { name: 'Grado' }).click();
  await captura(page, '003-paso2-select-grado-abierto');
  await modal.getByRole('option', { name: '8°' }).click();
  await expect(lista.locator('li[data-codigo]').first()).toHaveAttribute('data-codigo', /^CS-08-/);
  const deOctavo = await lista.locator('li[data-codigo]').evaluateAll((els) => els.map((e) => e.getAttribute('data-codigo')));
  expect(deOctavo.length).toBeGreaterThan(0);
  expect(deOctavo.every((c) => c?.startsWith('CS-08-'))).toBe(true);
  await captura(page, '003-paso2-filtrado-grado-8');

  // buscar por texto
  await modal.getByLabel('Buscar por enunciado').fill('asociaciones');
  await expect(lista.locator('li[data-codigo]')).toHaveCount(1);
  await expect(lista.locator('li[data-codigo="CS-08-08"]')).toBeVisible();
  await captura(page, '003-paso2-busqueda');

  // expandir CS-08-08 y ver sus evidencias (pedidas al expandir)
  const card = lista.locator('li[data-codigo="CS-08-08"]');
  await card.getByRole('button', { name: 'Ver CS-08-08' }).click();
  await expect(card.getByText('Evidencias')).toBeVisible();
  await expect(card.locator('ul li').first()).toBeVisible();
  // sin dictamen (QA-014): ninguna tachada; sin ejemplo (QA-011): sin infoblock
  await expect(card.getByText('— no aplica a formato cerrado')).toHaveCount(0);
  await expect(card.getByText('Ejemplo', { exact: true })).toHaveCount(0);
  await card.getByRole('radio', { name: 'Elegir CS-08-08' }).click();
  await captura(page, '003-paso2-dba-elegido-y-expandido');
  await modal.getByRole('button', { name: 'Continuar' }).click();

  // 004 — Paso 3: el nombre viene prellenado y "Crear experiencia" no crea nada
  await expect(modal.getByText('Qué va a pasar')).toBeVisible();
  const nombre = modal.getByRole('textbox');
  await expect(nombre).not.toHaveValue('');
  await captura(page, '004-paso3');
  const crear = modal.getByRole('button', { name: 'Crear experiencia', exact: true });
  await crear.click();
  await expect(modal.getByText('Crear la experiencia llega en la siguiente etapa.')).toBeVisible();
  await expect(page.getByText('Generando las preguntas...')).toHaveCount(0);
  await captura(page, '004-paso3-aviso-siguiente-etapa');
  await nombre.fill('');
  await expect(crear).toBeDisabled();

  // cerrar el modal: no se creó nada, el Dashboard sigue vacío
  await modal.getByRole('button', { name: 'Cerrar' }).click();
  await expect(page.getByText('Aún no has creado ninguna experiencia.')).toBeVisible();
});

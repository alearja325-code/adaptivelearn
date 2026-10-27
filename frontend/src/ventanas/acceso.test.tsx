// Pruebas de los formularios de acceso (ventanas 014, 015, 016, 017, 018,
// 019) y del paso entre ventanas según el estado de la cuenta.
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { backendFalso, montar, ruta, usuario } from '../pruebas/utilidades';

const SESION = { estado: 201, cuerpo: { user: { id: 1, email: 'ana@colegio.co', fullName: null, role: 'user' }, token: 'tok' } };

describe('Ventana 014 — Iniciar sesión / Crear cuenta', () => {
  it('marca el correo inválido al salir del campo, no mientras se escribe', async () => {
    backendFalso();
    montar('/iniciar-sesion');
    const correo = screen.getByLabelText('Correo electrónico');
    await userEvent.type(correo, 'ana@');
    expect(correo).not.toHaveAttribute('aria-invalid');
    await userEvent.tab();
    expect(correo).toHaveAttribute('aria-invalid', 'true');
  });

  it('credenciales incorrectas: el texto genérico de la spec y los campos no se limpian', async () => {
    backendFalso(ruta('POST', '/auth/login', { estado: 401, cuerpo: { message: 'Credenciales inválidas' } }));
    montar('/iniciar-sesion');
    await userEvent.type(screen.getByLabelText('Correo electrónico'), 'ana@colegio.co');
    await userEvent.type(screen.getByLabelText('Contraseña'), 'Mala12345');
    await userEvent.click(screen.getByRole('button', { name: 'Iniciar sesión' }));
    expect(await screen.findByText('Correo o contraseña incorrectos.')).toBeInTheDocument();
    expect(screen.getByLabelText('Correo electrónico')).toHaveValue('ana@colegio.co');
  });

  it('crear cuenta con una contraseña débil no llama al backend', async () => {
    const llamadas = backendFalso();
    montar('/crear-cuenta');
    expect(screen.getByText('Mínimo 8 caracteres, con una mayúscula y un número.')).toBeInTheDocument();
    await userEvent.type(screen.getByLabelText('Correo electrónico'), 'ana@colegio.co');
    await userEvent.type(screen.getByLabelText('Contraseña'), 'password123');
    await userEvent.click(screen.getByRole('button', { name: 'Crear cuenta' }));
    expect(screen.getByLabelText('Contraseña')).toHaveAttribute('aria-invalid', 'true');
    expect(llamadas).toHaveLength(0);
  });

  it('correo ya registrado: "Ya existe…" o el método que se debe usar (§2.6)', async () => {
    let respuesta = 'El email ya está registrado. Inicia sesión.';
    backendFalso(ruta('POST', '/auth/register', () => ({ estado: 409, cuerpo: { message: respuesta } })));
    montar('/crear-cuenta');
    await userEvent.type(screen.getByLabelText('Correo electrónico'), 'ana@colegio.co');
    await userEvent.type(screen.getByLabelText('Contraseña'), 'Password123');
    await userEvent.click(screen.getByRole('button', { name: 'Crear cuenta' }));
    expect(await screen.findByText('Ya existe una cuenta con este correo. Inicia sesión.')).toBeInTheDocument();

    respuesta = 'El email ya está registrado con Google. Continúa con ese botón.';
    await userEvent.click(screen.getByRole('button', { name: 'Crear cuenta' }));
    expect(await screen.findByText('Esta cuenta usa Google para entrar. Continúa con ese botón.')).toBeInTheDocument();
  });

  it('cambiar de variante conserva el correo escrito (§7)', async () => {
    backendFalso();
    montar('/iniciar-sesion');
    await userEvent.type(screen.getByLabelText('Correo electrónico'), 'ana@colegio.co');
    await userEvent.click(screen.getByText('Regístrate gratis'));
    expect(await screen.findByText('Crea tu cuenta')).toBeInTheDocument();
    expect(screen.getByLabelText('Correo electrónico')).toHaveValue('ana@colegio.co');
  });
});

describe('el paso entre ventanas según el estado de la cuenta (encargo 04 §5)', () => {
  it('registro válido → 015 con el correo de la cuenta', async () => {
    backendFalso(
      ruta('POST', '/auth/register', SESION),
      ruta('GET', '/auth/profile', { estado: 200, cuerpo: { user: usuario({ estadoVerificacion: 'procesando', perfil: null, role: 'user', idDocente: null }) } }),
    );
    montar('/crear-cuenta');
    await userEvent.type(screen.getByLabelText('Correo electrónico'), 'ana@colegio.co');
    await userEvent.type(screen.getByLabelText('Contraseña'), 'Password123');
    await userEvent.click(screen.getByRole('button', { name: 'Crear cuenta' }));
    expect(await screen.findByText('Verifica tu correo')).toBeInTheDocument();
    expect(screen.getByTestId('correo-verificar')).toHaveTextContent('ana@colegio.co');
  });

  it.each([
    ['sin verificar', usuario({ estadoVerificacion: 'procesando', perfil: null, idDocente: null }), 'Verifica tu correo'],
    ['verificada sin rol (registro a medias)', usuario({ perfil: null, idDocente: null, role: 'user' }), 'Completa tu perfil'],
    ['con rol de docente', usuario(), 'Crea una experiencia para tu grupo.'],
    ['con rol de estudiante', usuario({ idDocente: null, idEstudiante: 4, role: 'estudiante' }), 'Únete a una experiencia con el código de tu docente.'],
  ])('al recargar, una cuenta %s va a su ventana', async (_, cuenta, texto) => {
    backendFalso(ruta('GET', '/auth/profile', { estado: 200, cuerpo: { user: cuenta } }));
    montar('/', { token: 'tok' });
    expect(await screen.findByText(texto)).toBeInTheDocument();
  });

  it('sin sesión, una ruta protegida lleva a 014', async () => {
    backendFalso();
    montar('/');
    expect(await screen.findByText('Bienvenido de vuelta')).toBeInTheDocument();
  });

  it('una sesión vencida (401) lleva a 014 con el aviso', async () => {
    backendFalso(ruta('GET', '/auth/profile', { estado: 401, cuerpo: { message: 'Unauthorized' } }));
    montar('/', { token: 'vencido' });
    expect(await screen.findByText('Tu sesión terminó. Inicia sesión de nuevo.')).toBeInTheDocument();
    expect(sessionStorage.getItem('adaptivelearn.token')).toBeNull();
  });
});

describe('Ventana 015 — Verifica tu correo', () => {
  const procesando = ruta('GET', '/auth/profile', {
    estado: 200,
    cuerpo: { user: usuario({ estadoVerificacion: 'procesando', perfil: null, idDocente: null, role: 'user' }) },
  });

  it('"Verificar" se habilita con 6 dígitos, solo dígitos, y pegar llena las 6 cajas', async () => {
    backendFalso(procesando);
    montar('/verificar-correo', { token: 'tok' });
    const boton = await screen.findByRole('button', { name: 'Verificar' });
    expect(boton).toBeDisabled();
    await userEvent.type(screen.getByLabelText('Dígito 1'), 'a');
    expect(screen.getByLabelText('Dígito 1')).toHaveValue('');
    await userEvent.click(screen.getByLabelText('Dígito 1'));
    await userEvent.paste('123456');
    expect(screen.getByLabelText('Dígito 6')).toHaveValue('6');
    expect(boton).toBeEnabled();
    expect(screen.getByText('Reenviar (00:30)')).toBeInTheDocument();
  });

  it('código incorrecto: el texto de la spec, y el valor no se borra', async () => {
    backendFalso(
      procesando,
      ruta('POST', '/auth/verificar-correo', { estado: 400, cuerpo: { message: 'Código incorrecto. Revisa que esté bien escrito.' } }),
    );
    montar('/verificar-correo', { token: 'tok' });
    await userEvent.click(await screen.findByLabelText('Dígito 1'));
    await userEvent.paste('000000');
    await userEvent.click(screen.getByRole('button', { name: 'Verificar' }));
    expect(await screen.findByText('Código incorrecto. Revisa que esté bien escrito.')).toBeInTheDocument();
    expect(screen.getByLabelText('Dígito 1')).toHaveValue('0');
  });

  it('código correcto → 016', async () => {
    let verificado = false;
    backendFalso(
      ruta('GET', '/auth/profile', () => ({
        estado: 200,
        cuerpo: { user: usuario({ estadoVerificacion: verificado ? 'verificado' : 'procesando', perfil: null, idDocente: null, role: 'user' }) },
      })),
      ruta('POST', '/auth/verificar-correo', () => {
        verificado = true;
        return { estado: 200, cuerpo: { user: {} } };
      }),
    );
    montar('/verificar-correo', { token: 'tok' });
    await userEvent.click(await screen.findByLabelText('Dígito 1'));
    await userEvent.paste('123456');
    await userEvent.click(screen.getByRole('button', { name: 'Verificar' }));
    expect(await screen.findByText('Completa tu perfil')).toBeInTheDocument();
  });
});

describe('Ventanas 016 y 017 — Completa tu perfil y Elige tu rol', () => {
  const sinRol = ruta('GET', '/auth/profile', {
    estado: 200,
    cuerpo: { user: usuario({ perfil: null, idDocente: null, role: 'user', fullName: 'Ana María Pérez Gómez' }) },
  });

  it('prellena con el nombre de la cuenta y "Continuar" exige nombres y apellidos', async () => {
    backendFalso(sinRol);
    montar('/completar-perfil', { token: 'tok' });
    expect(await screen.findByLabelText('Nombres')).toHaveValue('Ana María');
    expect(screen.getByLabelText('Apellidos')).toHaveValue('Pérez Gómez');
    await userEvent.clear(screen.getByLabelText('Apellidos'));
    expect(screen.getByRole('button', { name: 'Continuar' })).toBeDisabled();
  });

  it('una foto que no es JPG ni PNG muestra el error y no cambia el avatar', async () => {
    backendFalso(sinRol);
    montar('/completar-perfil', { token: 'tok' });
    const entrada = await screen.findByTestId('entrada-foto');
    await userEvent.upload(entrada, new File(['GIF89a'], 'foto.gif', { type: 'image/gif' }), { applyAccept: false });
    expect(screen.getByText('Solo imágenes JPG o PNG, máximo 5 MB.')).toBeInTheDocument();
    expect(screen.queryByAltText('Foto de perfil')).not.toBeInTheDocument();
  });

  it('017: "Volver" devuelve el perfil escrito y "Continuar" envía rol y perfil', async () => {
    const llamadas = backendFalso(sinRol, ruta('POST', '/auth/elegir-rol', { estado: 500, cuerpo: { message: 'falló' } }));
    montar('/completar-perfil', { token: 'tok' });
    await userEvent.clear(await screen.findByLabelText('Nombres'));
    await userEvent.type(screen.getByLabelText('Nombres'), 'Ana');
    await userEvent.click(screen.getByRole('button', { name: 'Continuar' }));
    expect(await screen.findByText('Elige tu rol')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Continuar' })).toBeDisabled();
    await userEvent.click(screen.getByRole('button', { name: 'Volver' }));
    expect(await screen.findByLabelText('Nombres')).toHaveValue('Ana');

    await userEvent.click(screen.getByRole('button', { name: 'Continuar' }));
    await userEvent.click(await screen.findByRole('radio', { name: 'Soy Estudiante' }));
    await userEvent.click(screen.getByRole('button', { name: 'Continuar' }));
    const envio = await waitFor(() => {
      const l = llamadas.find((x) => x.url === '/auth/elegir-rol');
      expect(l).toBeTruthy();
      return l!;
    });
    const datos = envio.cuerpo as FormData;
    expect(datos.get('role')).toBe('estudiante');
    expect(datos.get('nombres')).toBe('Ana');
    expect(datos.get('apellidos')).toBe('Pérez Gómez');
    // un fallo del servidor nunca deja la pantalla en blanco
    expect(await screen.findByText('falló')).toBeInTheDocument();
  });
});

describe('Ventanas 018 y 019 — Recuperar la contraseña', () => {
  it('018: "Enviar código" se habilita solo con forma de correo, y siempre avanza', async () => {
    backendFalso(ruta('POST', '/auth/recuperar-contrasena', { estado: 202, cuerpo: { ok: true } }));
    montar('/recuperar');
    const boton = screen.getByRole('button', { name: 'Enviar código' });
    expect(boton).toBeDisabled();
    await userEvent.type(screen.getByLabelText('Correo electrónico'), 'nadie@x.co');
    expect(boton).toBeEnabled();
    await userEvent.click(boton);
    expect(await screen.findByText('Verifica tu correo')).toBeInTheDocument();
    expect(screen.getByTestId('correo-verificar')).toHaveTextContent('nadie@x.co');
  });

  it('el flujo completo termina en 014 con la confirmación en gris', async () => {
    backendFalso(
      ruta('POST', '/auth/recuperar-contrasena', { estado: 202, cuerpo: { ok: true } }),
      ruta('POST', '/auth/recuperar-contrasena/verificar', { estado: 200, cuerpo: { token: 'rec' } }),
      ruta('POST', '/auth/nueva-contrasena', { estado: 204 }),
    );
    montar('/recuperar');
    await userEvent.type(screen.getByLabelText('Correo electrónico'), 'ana@colegio.co');
    await userEvent.click(screen.getByRole('button', { name: 'Enviar código' }));
    await userEvent.click(await screen.findByLabelText('Dígito 1'));
    await userEvent.paste('123456');
    await userEvent.click(screen.getByRole('button', { name: 'Verificar' }));
    const guardar = await screen.findByRole('button', { name: 'Guardar' });
    await userEvent.type(screen.getByLabelText('Nueva contraseña'), 'nueva');
    expect(guardar).toBeDisabled();
    await userEvent.type(screen.getByLabelText('Nueva contraseña'), 'Clave9');
    expect(guardar).toBeEnabled();
    await userEvent.click(guardar);
    const aviso = await screen.findByText('Contraseña actualizada. Inicia sesión.');
    expect(aviso).toHaveClass('text-secondary');
    expect(screen.getByLabelText('Correo electrónico')).toHaveValue('ana@colegio.co');
  });

  it('019 sin el token de recuperación (al recargar) vuelve a 018', async () => {
    backendFalso();
    montar('/nueva-contrasena');
    expect(await screen.findByText('¿Olvidaste tu contraseña?', { selector: 'h1' })).toBeInTheDocument();
  });
});

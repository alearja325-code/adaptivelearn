import { User } from './user.entity.js';
import { PASSWORD_REGEX } from '../../auth/dto/password.constants.js';

function usuario(datos: Partial<User>): User {
  return Object.assign(new User(), {
    id: 1,
    email: 'a@example.com',
    fullName: null,
    emailVerificado: false,
    idDocente: null,
    idEstudiante: null,
    ...datos,
  });
}

describe('User', () => {
  it('nunca expone contraseña, códigos ni contadores al serializarse', () => {
    const json = JSON.stringify(
      usuario({ password: 'hash', codigoVerificacion: '123456', intentosLogin: 3 }),
    );
    expect(json).not.toMatch(/hash|123456|password|codigo|intentos/);
  });

  it('deduce el rol de la tabla en la que tiene fila (spec 20)', () => {
    expect(usuario({}).role).toBeNull();
    expect(usuario({ idDocente: 7 }).role).toBe('docente');
    expect(usuario({ idEstudiante: 7 }).role).toBe('estudiante');
  });
});

describe('Regla de contraseña (specs 17 y 22)', () => {
  it.each(['Password123', 'NuevaClave1'])('acepta %s', (p) => {
    expect(PASSWORD_REGEX.test(p)).toBe(true);
  });

  it.each(['password123', 'PASSWORDX', 'Corta1'])('rechaza %s', (p) => {
    expect(PASSWORD_REGEX.test(p)).toBe(false);
  });
});

import { Test } from '@nestjs/testing';
import type { NestExpressApplication } from '@nestjs/platform-express';
import { DataSource } from 'typeorm';
import request from 'supertest';
import { AppModule } from '../src/app.module.js';
import { configurarApp } from '../src/configurar-app.js';
import { CorreoService } from '../src/correo/correo.service.js';
import type { PropositoCodigo } from '../src/auth/entities/codigo-verificacion.entity.js';
import {
  VERIFICADORES,
  type IdentidadExterna,
  type VerificadorProveedor,
} from '../src/auth/proveedores/proveedor-identidad.js';

/** Reemplaza al correo real: guarda cada código "enviado". */
export class CorreoFalso {
  enviados: { correo: string; codigo: string; proposito: PropositoCodigo }[] = [];

  async enviarCodigo(correo: string, codigo: string, proposito: PropositoCodigo): Promise<void> {
    this.enviados.push({ correo, codigo, proposito });
  }

  ultimo(correo: string, proposito: PropositoCodigo = 'verificar_correo'): string {
    const envio = [...this.enviados].reverse().find((e) => e.correo === correo && e.proposito === proposito);
    if (!envio) throw new Error(`No se envió ningún código a ${correo} (${proposito})`);
    return envio.codigo;
  }

  cuantos(correo: string, proposito: PropositoCodigo = 'verificar_correo'): number {
    return this.enviados.filter((e) => e.correo === correo && e.proposito === proposito).length;
  }
}

/** Proveedor simulado (Google o Microsoft): acepta los tokens que se le registran. */
export class ProveedorFalso implements VerificadorProveedor {
  configurado = true;
  private readonly tokens = new Map<string, IdentidadExterna>();

  registrar(token: string, identidad: IdentidadExterna): void {
    this.tokens.set(token, identidad);
  }

  async verificar(token: string): Promise<IdentidadExterna> {
    const identidad = this.tokens.get(token);
    if (!identidad) throw new Error('token rechazado');
    return identidad;
  }
}

/** Un string con forma de JWT (tres partes base64url), como los de Google. */
export function tokenConFormaDeJwt(semilla: string): string {
  const b64 = (o: object) => Buffer.from(JSON.stringify(o)).toString('base64url');
  return `${b64({ alg: 'RS256' })}.${b64({ s: semilla })}.${Buffer.from(semilla).toString('base64url')}`;
}

export interface AppPruebas {
  app: NestExpressApplication;
  http: ReturnType<typeof request>;
  correo: CorreoFalso;
  google: ProveedorFalso;
  microsoft: ProveedorFalso;
  db: DataSource;
}

export async function crearApp(): Promise<AppPruebas> {
  const correo = new CorreoFalso();
  const google = new ProveedorFalso();
  const microsoft = new ProveedorFalso();
  const moduleRef = await Test.createTestingModule({ imports: [AppModule] })
    .overrideProvider(CorreoService)
    .useValue(correo)
    .overrideProvider(VERIFICADORES)
    .useValue({ google, microsoft })
    .compile();
  const app = moduleRef.createNestApplication<NestExpressApplication>({ logger: ['error'] });
  configurarApp(app);
  await app.init();
  return { app, http: request(app.getHttpServer()), correo, google, microsoft, db: app.get(DataSource) };
}

/** Deja las cuentas vacías (el catálogo no se toca), como sql/borrar-cuentas.sql. */
export async function borrarCuentas(db: DataSource): Promise<void> {
  await db.query('SET FOREIGN_KEY_CHECKS = 0');
  for (const t of ['codigo_verificacion', 'credencial', 'docente', 'estudiante']) {
    await db.query(`TRUNCATE TABLE ${t}`);
  }
  await db.query('SET FOREIGN_KEY_CHECKS = 1');
}

export const CLAVE = 'Password123';

/** Registra, verifica el correo y elige el rol: una cuenta completa. */
export async function crearCuenta(
  t: AppPruebas,
  email: string,
  role: 'docente' | 'estudiante' = 'docente',
): Promise<{ token: string; id: number }> {
  const reg = await t.http.post('/auth/register').send({ email, password: CLAVE }).expect(201);
  const token: string = reg.body.token;
  await t.http
    .post('/auth/verificar-correo')
    .set('Authorization', `Bearer ${token}`)
    .send({ codigo: t.correo.ultimo(email) })
    .expect(200);
  const rol = await t.http
    .post('/auth/elegir-rol')
    .set('Authorization', `Bearer ${token}`)
    .send({ role, nombres: 'Ana', apellidos: 'Pérez' })
    .expect(201);
  return { token: rol.body.token, id: rol.body.user.id };
}

/** Corre el reloj hacia atrás: el código parece creado hace `segundos`. */
export async function envejecerCodigo(db: DataSource, email: string, segundos: number): Promise<void> {
  await db.query(
    'UPDATE codigo_verificacion c JOIN credencial u ON u.id_credencial = c.id_credencial ' +
      'SET c.creado_en = DATE_SUB(c.creado_en, INTERVAL ? SECOND) WHERE u.correo = ?',
    [segundos, email],
  );
}

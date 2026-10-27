import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { createHmac, randomInt, timingSafeEqual } from 'node:crypto';
import { CodigoVerificacion, type PropositoCodigo } from './entities/codigo-verificacion.entity.js';

// RF-01-03 y ADR-039
export const MINUTOS_VIGENCIA_CODIGO = 10;
export const SEGUNDOS_ESPERA_REENVIO = 30;
export const MAX_INTENTOS_CODIGO = 5;

export type ResultadoCodigo = 'ok' | 'incorrecto' | 'vencido' | 'agotado' | 'inexistente';

/** ¿Ya venció? Se calcula desde creado_en (ADR-039): no hay columna de vencimiento. */
export function codigoVencido(creadoEn: Date, ahora: Date): boolean {
  return ahora.getTime() - creadoEn.getTime() > MINUTOS_VIGENCIA_CODIGO * 60_000;
}

/** ¿Ya se puede reenviar? También se calcula desde creado_en. */
export function puedeReenviar(creadoEn: Date, ahora: Date): boolean {
  return ahora.getTime() - creadoEn.getTime() >= SEGUNDOS_ESPERA_REENVIO * 1000;
}

/**
 * Los códigos de verificación (CU-03, CU-07). Se guardan con HMAC-SHA256,
 * con el JWT_SECRET del servidor como clave y la credencial y el propósito
 * dentro del mensaje: el mismo código de dos personas da hashes distintos.
 */
@Injectable()
export class CodigoService {
  private readonly clave: string;

  constructor(
    @InjectRepository(CodigoVerificacion)
    private readonly codigoRepository: Repository<CodigoVerificacion>,
    configService: ConfigService,
  ) {
    this.clave = configService.getOrThrow<string>('JWT_SECRET');
  }

  hash(idCredencial: number, proposito: PropositoCodigo, codigo: string): string {
    return createHmac('sha256', this.clave)
      .update(`${idCredencial}:${proposito}:${codigo}`)
      .digest('hex');
  }

  /**
   * Genera un código nuevo, que reemplaza al anterior del mismo propósito.
   * Con `respetarEspera`, si el anterior tiene menos de 30 s no genera nada
   * y devuelve null: así se cumple la espera aunque se llame la ruta directo.
   */
  async emitir(
    idCredencial: number,
    proposito: PropositoCodigo,
    { respetarEspera = false, ahora = new Date() } = {},
  ): Promise<string | null> {
    if (respetarEspera) {
      const anterior = await this.codigoRepository.findOneBy({ idCredencial, proposito });
      if (anterior && !puedeReenviar(anterior.creadoEn, ahora)) {
        return null;
      }
    }

    // crypto y no Math.random: Math.random no es impredecible
    const codigo = randomInt(0, 1_000_000).toString().padStart(6, '0');

    // INSERT ... ON DUPLICATE KEY UPDATE: reemplaza al anterior en una sola
    // sentencia, aunque lleguen dos peticiones a la vez (la PK es el par)
    await this.codigoRepository.upsert(
      {
        idCredencial,
        proposito,
        codigoHash: this.hash(idCredencial, proposito, codigo),
        creadoEn: ahora,
        intentos: 0,
      },
      ['idCredencial', 'proposito'],
    );

    return codigo;
  }

  /**
   * Comprueba un código. Si es correcto, lo borra (no se usa dos veces).
   * Si no, cuenta un intento; al quinto el código queda agotado hasta que
   * se pida otro (o hasta que la tarea nocturna lo borre, ya vencido).
   */
  async verificar(
    idCredencial: number,
    proposito: PropositoCodigo,
    codigo: string,
    ahora = new Date(),
  ): Promise<ResultadoCodigo> {
    const fila = await this.codigoRepository.findOneBy({ idCredencial, proposito });

    if (!fila) return 'inexistente';
    if (fila.intentos >= MAX_INTENTOS_CODIGO) return 'agotado';
    if (codigoVencido(fila.creadoEn, ahora)) return 'vencido';

    const esperado = Buffer.from(fila.codigoHash, 'hex');
    const recibido = Buffer.from(this.hash(idCredencial, proposito, codigo), 'hex');

    if (timingSafeEqual(esperado, recibido)) {
      await this.codigoRepository.delete({ idCredencial, proposito });
      return 'ok';
    }

    // Condicional: dos intentos simultáneos no pasan de 5 (CHECK del MR)
    await this.codigoRepository
      .createQueryBuilder()
      .update()
      .set({ intentos: () => 'intentos + 1' })
      .where('id_credencial = :idCredencial AND proposito = :proposito AND intentos < :max', {
        idCredencial,
        proposito,
        max: MAX_INTENTOS_CODIGO,
      })
      .execute();

    return fila.intentos + 1 >= MAX_INTENTOS_CODIGO ? 'agotado' : 'incorrecto';
  }
}

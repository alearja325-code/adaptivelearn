import { Injectable, Logger, OnModuleInit } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { SchedulerRegistry } from '@nestjs/schedule';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource } from 'typeorm';
import { CronJob } from 'cron';
import { MINUTOS_VIGENCIA_CODIGO } from '../auth/codigo.service.js';

export interface ResultadoLimpieza {
  codigosVencidos: number;
  credencialesSinTerminar: number;
}

/**
 * La tarea nocturna de ADR-039. Cada noche (por defecto a las 3:00 a. m.,
 * hora de Colombia) borra:
 *   - los códigos de verificación vencidos (más de 10 minutos);
 *   - las credenciales que llevan más de 7 días en `procesando` sin haber
 *     elegido rol (registros que nunca verificaron el correo). Sus códigos
 *     se van con ellas (FK en CASCADE).
 * La hora, la zona y los días son configuración (.env), no del modelo:
 * LIMPIEZA_CRON, LIMPIEZA_ZONA_HORARIA y LIMPIEZA_DIAS_SIN_TERMINAR.
 * No es un caso de uso: no la inicia ningún actor (`16` §7).
 */
@Injectable()
export class LimpiezaService implements OnModuleInit {
  private readonly logger = new Logger(LimpiezaService.name);
  private readonly diasSinTerminar: number;

  constructor(
    private readonly configService: ConfigService,
    private readonly schedulerRegistry: SchedulerRegistry,
    @InjectDataSource() private readonly dataSource: DataSource,
  ) {
    this.diasSinTerminar = Number(configService.get<string>('LIMPIEZA_DIAS_SIN_TERMINAR') || 7);
  }

  onModuleInit(): void {
    // Se programa aquí y no con @Cron('...'): el decorador se evalúa antes de
    // leer .env, y la hora tiene que poder cambiarse sin tocar el código.
    const cron = this.configService.get<string>('LIMPIEZA_CRON') || '0 3 * * *';
    const zona = this.configService.get<string>('LIMPIEZA_ZONA_HORARIA') || 'America/Bogota';
    const tarea = CronJob.from({
      cronTime: cron,
      timeZone: zona,
      onTick: () => {
        this.limpiar().catch((error: unknown) =>
          this.logger.error(`La limpieza nocturna falló: ${String(error)}`),
        );
      },
    });
    this.schedulerRegistry.addCronJob('limpieza-nocturna', tarea);
    tarea.start();
    this.logger.log(
      `Limpieza nocturna programada: "${cron}" (${zona}); credenciales sin terminar tras ` +
        `${this.diasSinTerminar} días`,
    );
  }

  /** Lo que hace la tarea. Público para poder probarlo y correrlo a mano. */
  async limpiar(ahora = new Date()): Promise<ResultadoLimpieza> {
    const limiteCodigo = new Date(ahora.getTime() - MINUTOS_VIGENCIA_CODIGO * 60_000);
    const limiteCredencial = new Date(ahora.getTime() - this.diasSinTerminar * 86_400_000);

    const codigos = await this.dataSource
      .createQueryBuilder()
      .delete()
      .from('codigo_verificacion')
      .where('creado_en < :limite', { limite: limiteCodigo })
      .execute();

    // Nunca una cuenta con rol ni la del administrador de la guía
    const credenciales = await this.dataSource
      .createQueryBuilder()
      .delete()
      .from('credencial')
      .where("estado_verificacion = 'procesando'")
      .andWhere('id_docente IS NULL AND id_estudiante IS NULL AND es_admin = 0')
      .andWhere('creado_en < :limite', { limite: limiteCredencial })
      .execute();

    const resultado: ResultadoLimpieza = {
      codigosVencidos: codigos.affected ?? 0,
      credencialesSinTerminar: credenciales.affected ?? 0,
    };
    this.logger.log(
      `Limpieza nocturna: ${resultado.codigosVencidos} códigos vencidos y ` +
        `${resultado.credencialesSinTerminar} credenciales sin terminar borrados`,
    );
    return resultado;
  }
}

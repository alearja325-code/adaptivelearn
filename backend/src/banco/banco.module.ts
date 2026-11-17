import { Module } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { BancoService } from './banco.service.js';
import { Experiencia } from './entities/experiencia.entity.js';
import { Item } from './entities/item.entity.js';
import { Opcion } from './entities/opcion.entity.js';
import { ExperienciasController } from './experiencias.controller.js';
import { ExperienciasService } from './experiencias.service.js';
import { GeneradorBanco, OPCIONES_POR_DEFECTO } from './generador-banco.js';
import { Generaciones } from './generaciones.js';
import { elegirServicioIa, tiempoLimite } from './ia/elegir-servicio.js';
import { SERVICIO_IA, type ServicioIa } from './ia/servicio-ia.js';
import { ItemsController } from './items.controller.js';

// SUB-02 Experiencias y SUB-03 Banco de preguntas: la iteración I2 (`20` §4.2-4.3)
@Module({
  imports: [TypeOrmModule.forFeature([Experiencia, Item, Opcion])],
  controllers: [ExperienciasController, ItemsController],
  providers: [
    ExperienciasService,
    BancoService,
    Generaciones,
    {
      provide: SERVICIO_IA,
      inject: [ConfigService],
      useFactory: elegirServicioIa,
    },
    {
      provide: GeneradorBanco,
      inject: [SERVICIO_IA, ConfigService],
      useFactory: (ia: ServicioIa, config: ConfigService) =>
        new GeneradorBanco(ia, {
          ...OPCIONES_POR_DEFECTO,
          tiempoLimiteMs: tiempoLimite(config),
        }),
    },
  ],
})
export class BancoModule {}

import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { DiagnosticoController } from './diagnostico.controller.js';
import { DiagnosticoService } from './diagnostico.service.js';
import { Inscripcion } from './entities/inscripcion.entity.js';
import { Presentacion } from './entities/presentacion.entity.js';
import { Respuesta } from './entities/respuesta.entity.js';
import { RespuestaOpcion } from './entities/respuesta-opcion.entity.js';
import { Resultado } from './entities/resultado.entity.js';

// I3 — Diagnóstico (encargo 07)
@Module({
  imports: [
    TypeOrmModule.forFeature([
      Inscripcion,
      Presentacion,
      Respuesta,
      RespuestaOpcion,
      Resultado,
    ]),
  ],
  controllers: [DiagnosticoController],
  providers: [DiagnosticoService],
})
export class DiagnosticoModule {}

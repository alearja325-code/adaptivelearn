import { Module } from '@nestjs/common';
import { ReporteController } from './reporte.controller.js';
import { HistorialController } from './historial.controller.js';
import { ReporteService } from './reporte.service.js';

// I4 — Reporte y seguimiento (encargo 07). Solo lee; no tiene tablas propias:
// el reporte se calcula al abrirlo (ADR-022).
@Module({
  controllers: [ReporteController, HistorialController],
  providers: [ReporteService],
})
export class ReporteModule {}

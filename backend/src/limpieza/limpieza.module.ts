import { Module } from '@nestjs/common';
import { LimpiezaService } from './limpieza.service.js';

// La tarea nocturna de ADR-039 (ScheduleModule se registra en AppModule)
@Module({
  providers: [LimpiezaService],
  exports: [LimpiezaService],
})
export class LimpiezaModule {}

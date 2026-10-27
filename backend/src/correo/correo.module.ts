import { Global, Module } from '@nestjs/common';
import { CorreoService } from './correo.service.js';

// Global: lo usan el acceso y, más adelante, otros módulos.
@Global()
@Module({
  providers: [CorreoService],
  exports: [CorreoService],
})
export class CorreoModule {}

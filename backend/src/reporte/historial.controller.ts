import {
  Controller,
  Get,
  Param,
  ParseIntPipe,
  UseGuards,
} from '@nestjs/common';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard.js';
import { RolesGuard } from '../auth/guards/roles.guard.js';
import { Roles } from '../auth/decorators/roles.decorator.js';
import { GetUser } from '../auth/decorators/get-user.decorator.js';
import type { User } from '../user/entities/user.entity.js';
import { ReporteService, type Historial } from './reporte.service.js';

// E-37 (`20` §6): solo el docente dueño de la experiencia de la inscripción;
// el estudiante nunca (ADR-028). Comparte el prefijo /inscripciones con el
// diagnóstico, pero es del Reporte (SUB-05).
@Controller('inscripciones')
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('docente')
export class HistorialController {
  constructor(private readonly reporte: ReporteService) {}

  /** GET /inscripciones/:id/historial — E-37 */
  @Get(':id/historial')
  historial(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
  ): Promise<Historial> {
    return this.reporte.historial(user, id);
  }
}

import {
  Controller,
  Get,
  Param,
  ParseIntPipe,
  Query,
  UseGuards,
} from '@nestjs/common';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard.js';
import { RolesGuard } from '../auth/guards/roles.guard.js';
import { Roles } from '../auth/decorators/roles.decorator.js';
import { GetUser } from '../auth/decorators/get-user.decorator.js';
import type { User } from '../user/entities/user.entity.js';
import {
  ReporteService,
  type EstudiantesPorEstado,
  type Reporte,
} from './reporte.service.js';
import { FiltroEstudiantesDto } from './dto/filtro-estudiantes.dto.js';

// SUB-05, Reporte y seguimiento (I4): E-35 a E-37 (`20` §6). Solo el
// docente dueño de la experiencia (403 si no); el estudiante nunca (ADR-028).
// El historial (E-37) cuelga de /inscripciones: está en historial.controller.ts.

@Controller('experiencias')
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('docente')
export class ReporteController {
  constructor(private readonly reporte: ReporteService) {}

  /** GET /experiencias/:id/reporte — E-35 */
  @Get(':id/reporte')
  ver(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
  ): Promise<Reporte> {
    return this.reporte.reporte(user, id);
  }

  /** GET /experiencias/:id/estudiantes?estado=no_muestra&q=nombre — E-36 */
  @Get(':id/estudiantes')
  estudiantes(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
    @Query() filtro: FiltroEstudiantesDto,
  ): Promise<EstudiantesPorEstado> {
    return this.reporte.estudiantesPorEstado(user, id, filtro);
  }
}

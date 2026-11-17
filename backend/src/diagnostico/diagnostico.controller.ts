import {
  Body,
  Controller,
  Delete,
  Get,
  HttpCode,
  Param,
  ParseIntPipe,
  Post,
  Query,
  Res,
  UseGuards,
} from '@nestjs/common';
import type { Response } from 'express';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard.js';
import { RolesGuard } from '../auth/guards/roles.guard.js';
import { Roles } from '../auth/decorators/roles.decorator.js';
import { GetUser } from '../auth/decorators/get-user.decorator.js';
import type { User } from '../user/entities/user.entity.js';
import {
  DiagnosticoService,
  type InscripcionDetalle,
  type InscripcionResumen,
  type PreguntaParaEstudiante,
} from './diagnostico.service.js';
import { FiltroInscripcionesDto } from './dto/filtro-inscripciones.dto.js';
import { UnirseDto } from './dto/unirse.dto.js';
import { ResponderDto } from './dto/responder.dto.js';

// SUB-04, Diagnóstico (I3): E-29 a E-34 (`20` §5). Solo para la sesión de
// un estudiante, y cada inscripción solo para su dueño (403 si no).
@Controller('inscripciones')
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('estudiante')
export class DiagnosticoController {
  constructor(private readonly diagnostico: DiagnosticoService) {}

  /** GET /inscripciones?progreso=en_curso&q=texto — E-29 */
  @Get()
  lista(
    @GetUser() user: User,
    @Query() filtro: FiltroInscripcionesDto,
  ): Promise<InscripcionResumen[]> {
    return this.diagnostico.misInscripciones(user, filtro);
  }

  /** POST /inscripciones — E-30: 201 la nueva; 200 la que ya existía (RI-1). */
  @Post()
  async unirse(
    @GetUser() user: User,
    @Body() dto: UnirseDto,
    @Res({ passthrough: true }) res: Response,
  ): Promise<InscripcionResumen> {
    const { creada, inscripcion } = await this.diagnostico.unirse(
      user,
      dto.codigo,
    );
    res.status(creada ? 201 : 200);
    return inscripcion;
  }

  /** GET /inscripciones/:id — E-31 */
  @Get(':id')
  consultar(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
  ): Promise<InscripcionDetalle> {
    return this.diagnostico.consultar(user, id);
  }

  /**
   * POST /inscripciones/:id/presentaciones — E-32: 201 una pregunta nueva;
   * 200 la misma de antes (ADR-031) o `{ pregunta: null }`, el cierre.
   */
  @Post(':id/presentaciones')
  async siguiente(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
    @Res({ passthrough: true }) res: Response,
  ): Promise<{ pregunta: PreguntaParaEstudiante | null }> {
    const { creada, pregunta } = await this.diagnostico.siguientePregunta(
      user,
      id,
    );
    res.status(creada ? 201 : 200);
    return { pregunta };
  }

  /** POST /inscripciones/:id/respuestas — E-33: 201, sin decir si acertó (RF-04-08). */
  @Post(':id/respuestas')
  async responder(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
    @Body() dto: ResponderDto,
  ): Promise<{ registrada: true }> {
    await this.diagnostico.responder(user, id, dto);
    return { registrada: true };
  }

  /** DELETE /inscripciones/:id — E-34: 204 */
  @Delete(':id')
  @HttpCode(204)
  async salir(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
  ): Promise<void> {
    await this.diagnostico.salir(user, id);
  }
}

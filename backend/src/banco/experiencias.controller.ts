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
  UseGuards,
} from '@nestjs/common';
import { GetUser } from '../auth/decorators/get-user.decorator.js';
import { Roles } from '../auth/decorators/roles.decorator.js';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard.js';
import { RolesGuard } from '../auth/guards/roles.guard.js';
import type { User } from '../user/entities/user.entity.js';
import {
  BancoService,
  type BancoVista,
  type ItemVista,
} from './banco.service.js';
import { CrearExperienciaDto } from './dto/crear-experiencia.dto.js';
import { FiltroBancoDto, FiltroExperienciasDto } from './dto/filtros.dto.js';
import { ItemDto } from './dto/item.dto.js';
import {
  ExperienciasService,
  type ExperienciaDetalle,
  type ExperienciaResumen,
  type GeneracionVista,
} from './experiencias.service.js';

// SUB-02 Experiencias (`20` §4.2) y E-24, E-28 del banco (§4.3). Solo
// docentes; cada experiencia, solo su dueño (403 si es de otro).
@Controller('experiencias')
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('docente')
export class ExperienciasController {
  constructor(
    private readonly experiencias: ExperienciasService,
    private readonly banco: BancoService,
  ) {}

  /** GET /experiencias?estado=borrador&q=texto — E-18 */
  @Get()
  listar(
    @GetUser() user: User,
    @Query() filtro: FiltroExperienciasDto,
  ): Promise<ExperienciaResumen[]> {
    return this.experiencias.listar(user.idDocente!, filtro);
  }

  /** POST /experiencias — E-19: 202 con la generación (ADR-045) */
  @Post()
  @HttpCode(202)
  crear(
    @GetUser() user: User,
    @Body() dto: CrearExperienciaDto,
  ): Promise<GeneracionVista> {
    return this.experiencias.crear(user.idDocente!, dto);
  }

  /** GET /experiencias/generaciones/:id — cómo va la generación (ADR-045) */
  @Get('generaciones/:id')
  generacion(@GetUser() user: User, @Param('id') id: string): GeneracionVista {
    return this.experiencias.generacion(user.idDocente!, id);
  }

  /** GET /experiencias/:id — E-20 */
  @Get(':id')
  consultar(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
  ): Promise<ExperienciaDetalle> {
    return this.experiencias.consultar(user.idDocente!, id);
  }

  /** POST /experiencias/:id/publicar — E-21 */
  @Post(':id/publicar')
  @HttpCode(200)
  publicar(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
  ): Promise<ExperienciaDetalle> {
    return this.experiencias.publicar(user.idDocente!, id);
  }

  /** GET /experiencias/:id/codigo — E-22 */
  @Get(':id/codigo')
  codigo(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
  ): Promise<{ codigo: string }> {
    return this.experiencias.codigo(user.idDocente!, id);
  }

  /** DELETE /experiencias/:id — E-23 */
  @Delete(':id')
  @HttpCode(204)
  eliminar(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
  ): Promise<void> {
    return this.experiencias.eliminar(user.idDocente!, id);
  }

  /** GET /experiencias/:id/banco?formato=matching&q=texto — E-24 */
  @Get(':id/banco')
  verBanco(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
    @Query() filtro: FiltroBancoDto,
  ): Promise<BancoVista> {
    return this.banco.banco(user.idDocente!, id, filtro);
  }

  /** POST /experiencias/:id/evidencias/:n/items — E-28 */
  @Post(':id/evidencias/:n/items')
  agregarItem(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
    @Param('n', ParseIntPipe) n: number,
    @Body() dto: ItemDto,
  ): Promise<ItemVista> {
    return this.banco.agregarItem(user.idDocente!, id, n, dto);
  }
}

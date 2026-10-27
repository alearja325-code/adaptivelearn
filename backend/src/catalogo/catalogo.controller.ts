import { Controller, Get, Param, Query, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard.js';
import { RolesGuard } from '../auth/guards/roles.guard.js';
import { Roles } from '../auth/decorators/roles.decorator.js';
import { CatalogoService, type DbaDetalle, type DbaResumen } from './catalogo.service.js';
import { FiltroDbasDto } from './dto/filtro-dbas.dto.js';
import { Area } from './entities/area.entity.js';
import { Grado } from './entities/grado.entity.js';

// El catálogo curricular (SUB-06): solo lectura y solo para la sesión de
// un docente (`20` §4.1). Se protege como /users en la guía: token y rol.
@Controller('catalogo')
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('docente')
export class CatalogoController {
  constructor(private readonly catalogoService: CatalogoService) {}

  /** GET /catalogo/areas — E-16 */
  @Get('areas')
  areas(): Promise<Area[]> {
    return this.catalogoService.areas();
  }

  /** GET /catalogo/grados — E-17 */
  @Get('grados')
  grados(): Promise<Grado[]> {
    return this.catalogoService.grados();
  }

  /** GET /catalogo/dbas?codigo_area=MAT&numero_grado=8&q=texto — E-14 */
  @Get('dbas')
  dbas(@Query() filtro: FiltroDbasDto): Promise<DbaResumen[]> {
    return this.catalogoService.dbas(filtro);
  }

  /** GET /catalogo/dbas/:codigo — E-15 */
  @Get('dbas/:codigo')
  dba(@Param('codigo') codigo: string): Promise<DbaDetalle> {
    return this.catalogoService.dba(codigo);
  }
}

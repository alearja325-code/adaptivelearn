import {
  Body,
  Controller,
  HttpCode,
  Param,
  ParseIntPipe,
  Patch,
  Post,
  UseGuards,
} from '@nestjs/common';
import { GetUser } from '../auth/decorators/get-user.decorator.js';
import { Roles } from '../auth/decorators/roles.decorator.js';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard.js';
import { RolesGuard } from '../auth/guards/roles.guard.js';
import type { User } from '../user/entities/user.entity.js';
import { BancoService, type ItemVista } from './banco.service.js';
import { ItemDto } from './dto/item.dto.js';

// SUB-03 Banco de preguntas: E-25 a E-27 (`20` §4.3)
@Controller('items')
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('docente')
export class ItemsController {
  constructor(private readonly banco: BancoService) {}

  /** PATCH /items/:id — E-25 */
  @Patch(':id')
  editar(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
    @Body() dto: ItemDto,
  ): Promise<ItemVista> {
    return this.banco.editarItem(user.idDocente!, id, dto);
  }

  /** POST /items/:id/descartar — E-26 */
  @Post(':id/descartar')
  @HttpCode(204)
  descartar(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
  ): Promise<void> {
    return this.banco.descartar(user.idDocente!, id);
  }

  /** POST /items/:id/reincluir — E-27 */
  @Post(':id/reincluir')
  @HttpCode(204)
  reincluir(
    @GetUser() user: User,
    @Param('id', ParseIntPipe) id: number,
  ): Promise<void> {
    return this.banco.reincluir(user.idDocente!, id);
  }
}

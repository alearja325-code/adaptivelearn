import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  ParseIntPipe,
  UseGuards,
  ForbiddenException,
} from '@nestjs/common';
import { UserService } from './user.service.js';
import { CreateUserDto } from './dto/create-user.dto.js';
import { UpdateUserDto } from './dto/update-user.dto.js';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard.js';
import { GetUser } from '../auth/decorators/get-user.decorator.js';
import { User } from './entities/user.entity.js';

// Guía: mismas rutas, sin ninguna protección. Acá todas exigen JWT — sin
// eso, cualquiera podría listar, crear o modificar cuentas sin iniciar
// sesión. Sin DELETE: ninguna spec define borrar cuentas y el modelo
// relacional usa RESTRICT sobre Docente/Estudiante.
@UseGuards(JwtAuthGuard)
@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  /**
   * POST /users
   * Crear un nuevo usuario
   */
  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    return this.userService.create(createUserDto);
  }

  /**
   * GET /users
   * Obtener todos los usuarios
   */
  @Get()
  findAll() {
    return this.userService.findAll();
  }

  /**
   * GET /users/:id
   * Obtener un usuario por ID
   */
  @Get(':id')
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.userService.findOne(id);
  }

  /**
   * PATCH /users/:id
   * Completar/actualizar el perfil (spec 19) — solo la propia cuenta
   */
  @Patch(':id')
  update(
    @Param('id', ParseIntPipe) id: number,
    @Body() updateUserDto: UpdateUserDto,
    @GetUser() user: User,
  ) {
    if (user.id !== id) {
      throw new ForbiddenException('Solo puedes modificar tu propia cuenta.');
    }
    return this.userService.update(id, updateUserDto);
  }
}

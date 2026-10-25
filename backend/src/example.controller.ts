import { Controller, Get, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from './auth/guards/jwt-auth.guard.js';
import { RolesGuard } from './auth/guards/roles.guard.js';
import { Roles } from './auth/decorators/roles.decorator.js';
import { GetUser } from './auth/decorators/get-user.decorator.js';
import { User } from './user/entities/user.entity.js';

@Controller('example')
export class ExampleController {
  // Ruta protegida solo con autenticación
  @UseGuards(JwtAuthGuard)
  @Get('protected')
  protectedRoute(@GetUser() user: User) {
    return {
      message: 'Esta ruta está protegida',
      user: user,
    };
  }

  // Ruta protegida solo para docentes. Guía: @Roles('admin'); este modelo
  // no tiene rol admin, solo docente y estudiante (spec 20).
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('docente')
  @Get('docente')
  docenteRoute(@GetUser() user: User) {
    return {
      message: 'Esta ruta es solo para docentes',
      user: user,
    };
  }
}

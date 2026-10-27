import { Controller, Get, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard.js';
import { RolesGuard } from '../auth/guards/roles.guard.js';
import { Roles } from '../auth/decorators/roles.decorator.js';
import { GetUser } from '../auth/decorators/get-user.decorator.js';
import { User } from '../user/entities/user.entity.js';

interface ExampleResponse {
  message: string;
  user: User;
}

// Sección 6 de la guía: los dos niveles de protección. No es del producto.
@Controller('example')
export class ExampleController {
  // Ruta protegida solo con autenticación
  @UseGuards(JwtAuthGuard)
  @Get('protected')
  protectedRoute(@GetUser() user: User): ExampleResponse {
    return {
      message: 'Esta ruta está protegida',
      user,
    };
  }

  // Ruta protegida solo para administradores
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @Get('admin')
  adminRoute(@GetUser() user: User): ExampleResponse {
    return {
      message: 'Esta ruta es solo para administradores',
      user,
    };
  }
}

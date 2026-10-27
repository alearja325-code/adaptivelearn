import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UserService } from './user.service.js';
import { UserController } from './user.controller.js';
import { User } from './entities/user.entity.js';
import { Docente } from './entities/docente.entity.js';
import { Estudiante } from './entities/estudiante.entity.js';

@Module({
  // Importar los repositorios: la credencial (User) y las dos tablas de rol
  imports: [TypeOrmModule.forFeature([User, Docente, Estudiante])],
  controllers: [UserController],
  providers: [UserService],
  // Exportar el servicio para usarlo en otros módulos (como Auth)
  exports: [UserService],
})
export class UserModule {}

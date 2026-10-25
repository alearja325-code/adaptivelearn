import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Estudiante } from './entities/estudiante.entity.js';
import { EstudiantesService } from './estudiantes.service.js';

@Module({
  imports: [TypeOrmModule.forFeature([Estudiante])],
  providers: [EstudiantesService],
  exports: [EstudiantesService],
})
export class EstudiantesModule {}

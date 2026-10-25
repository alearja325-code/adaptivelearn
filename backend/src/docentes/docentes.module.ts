import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Docente } from './entities/docente.entity.js';
import { DocentesService } from './docentes.service.js';

@Module({
  imports: [TypeOrmModule.forFeature([Docente])],
  providers: [DocentesService],
  exports: [DocentesService],
})
export class DocentesModule {}

import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CatalogoController } from './catalogo.controller.js';
import { CatalogoService } from './catalogo.service.js';
import { Area } from './entities/area.entity.js';
import { Grado } from './entities/grado.entity.js';
import { DocumentoOficial } from './entities/documento-oficial.entity.js';
import { Dba } from './entities/dba.entity.js';
import { Evidencia } from './entities/evidencia.entity.js';
import { EvidenciaDictamen } from './entities/evidencia-dictamen.entity.js';

@Module({
  imports: [
    TypeOrmModule.forFeature([Area, Grado, DocumentoOficial, Dba, Evidencia, EvidenciaDictamen]),
  ],
  controllers: [CatalogoController],
  providers: [CatalogoService],
})
export class CatalogoModule {}

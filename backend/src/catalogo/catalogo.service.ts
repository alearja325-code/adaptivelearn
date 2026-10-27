import { BadRequestException, Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Area } from './entities/area.entity.js';
import { Grado } from './entities/grado.entity.js';
import { Dba } from './entities/dba.entity.js';
import { FiltroDbasDto } from './dto/filtro-dbas.dto.js';

export interface DbaResumen {
  codigo: string;
  enunciado: string;
  area: { codigo: string; nombre: string };
  grado: { numero: number; nombre: string };
}

export interface DbaDetalle extends DbaResumen {
  ejemplo: string | null;
  documento: { titulo: string; version: string; anio: number; paginas: number; urlOficial: string };
  evidencias: {
    numero: number;
    enunciado: string;
    // null mientras no haya dictamen (censo QA-014 pendiente, V-6)
    admiteFormatoCerrado: boolean | null;
    formato: string | null;
  }[];
}

/**
 * El catálogo curricular (SUB-06, CU-31), de solo lectura. Sus datos los
 * carga el equipo desde data/curriculo-men/ (scripts/preparar-base.mjs).
 */
@Injectable()
export class CatalogoService {
  constructor(
    @InjectRepository(Area) private readonly areaRepository: Repository<Area>,
    @InjectRepository(Grado) private readonly gradoRepository: Repository<Grado>,
    @InjectRepository(Dba) private readonly dbaRepository: Repository<Dba>,
  ) {}

  /** E-16 — las áreas, para el Paso 1 de crear experiencia. */
  async areas(): Promise<Area[]> {
    return await this.areaRepository.find({ order: { nombre: 'ASC' } });
  }

  /** E-17 — los grados, para el filtro del Paso 2. */
  async grados(): Promise<Grado[]> {
    return await this.gradoRepository.find({ order: { numero: 'ASC' } });
  }

  /** E-14 — los DBA de un área, filtrados por grado y por texto. */
  async dbas(filtro: FiltroDbasDto): Promise<DbaResumen[]> {
    const area = await this.areaRepository.findOneBy({ codigo: filtro.codigo_area });
    if (!area) {
      throw new BadRequestException('codigo_area debe ser una de las 4 áreas: MAT, LEN, CN o CS');
    }

    const consulta = this.dbaRepository
      .createQueryBuilder('dba')
      .innerJoinAndSelect('dba.area', 'area')
      .innerJoinAndSelect('dba.grado', 'grado')
      .where('dba.codigo_area = :area', { area: area.codigo })
      .orderBy('dba.numero_grado', 'ASC')
      .addOrderBy('dba.codigo_dba', 'ASC');

    if (filtro.numero_grado !== undefined) {
      consulta.andWhere('dba.numero_grado = :grado', { grado: filtro.numero_grado });
    }
    if (filtro.q?.trim()) {
      // LIKE con los comodines del texto escapados: "50%" busca "50%"
      const texto = filtro.q.trim().replace(/[\\%_]/g, (c) => `\\${c}`);
      consulta.andWhere('dba.enunciado LIKE :q', { q: `%${texto}%` });
    }

    const filas = await consulta.getMany();
    return filas.map((dba) => resumen(dba));
  }

  /** E-15 — un DBA con su documento oficial y sus evidencias en orden. */
  async dba(codigo: string): Promise<DbaDetalle> {
    const dba = await this.dbaRepository
      .createQueryBuilder('dba')
      .innerJoinAndSelect('dba.area', 'area')
      .innerJoinAndSelect('dba.grado', 'grado')
      .innerJoinAndSelect('dba.documento', 'documento')
      .leftJoinAndSelect('dba.evidencias', 'evidencia')
      .leftJoinAndSelect('evidencia.dictamen', 'dictamen')
      .where('dba.codigo_dba = :codigo', { codigo })
      .orderBy('evidencia.numero_evidencia', 'ASC')
      .getOne();

    if (!dba) {
      throw new NotFoundException(`No existe el DBA ${codigo}`);
    }

    const { titulo, version, anio, paginas, urlOficial } = dba.documento;
    return {
      ...resumen(dba),
      ejemplo: dba.ejemplo,
      documento: { titulo, version, anio, paginas, urlOficial },
      evidencias: dba.evidencias.map((e) => ({
        numero: e.numero,
        enunciado: e.enunciado,
        admiteFormatoCerrado: e.dictamen ? e.dictamen.aplicaFormatoCerrado : null,
        formato: e.dictamen?.formato ?? null,
      })),
    };
  }
}

function resumen(dba: Dba): DbaResumen {
  return {
    codigo: dba.codigo,
    enunciado: dba.enunciado,
    area: { codigo: dba.area.codigo, nombre: dba.area.nombre },
    grado: { numero: dba.grado.numero, nombre: dba.grado.nombre },
  };
}

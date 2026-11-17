import { ForbiddenException, NotFoundException } from '@nestjs/common';
import type { EntityManager } from 'typeorm';
import type { EstadoExperiencia } from './entities/experiencia.entity.js';

export interface ExperienciaPropia {
  id: number;
  idDocente: number;
  codigoDba: string;
  estado: EstadoExperiencia;
}

/** Ítems activos que necesita cada evidencia para publicar (RI-14, ADR-026). */
export const MINIMO_ACTIVOS = 6;

/**
 * La experiencia, si existe (404) y es del docente (403, `20` §2.2: el 403
 * no esconde que existe, porque los ids no son secretos).
 */
export async function experienciaPropia(
  m: EntityManager,
  id: number,
  idDocente: number,
): Promise<ExperienciaPropia> {
  const [fila] = (await m.query(
    'SELECT id_experiencia AS id, id_docente AS idDocente, codigo_dba AS codigoDba, estado FROM experiencia WHERE id_experiencia = ?',
    [id],
  )) as ExperienciaPropia[];
  if (!fila) throw new NotFoundException('No existe esa experiencia.');
  if (fila.idDocente !== idDocente)
    throw new ForbiddenException('Esa experiencia no es tuya.');
  return fila;
}

/** LIKE con los comodines del texto escapados, como en el catálogo. */
export const patronLike = (q: string): string =>
  `%${q.trim().replace(/[\\%_]/g, (c) => `\\${c}`)}%`;

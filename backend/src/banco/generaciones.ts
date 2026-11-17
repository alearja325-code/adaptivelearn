import { randomUUID } from 'node:crypto';
import { Injectable } from '@nestjs/common';

export type EstadoGeneracion = 'generando' | 'lista' | 'fallida';

export interface Generacion {
  id: string;
  idDocente: number;
  estado: EstadoGeneracion;
  idExperiencia: number | null;
  mensaje: string | null;
}

/** El mensaje de `07-spec` (ADR-043 punto 2) cuando la generación falla. */
export const MENSAJE_FALLIDA =
  'No se pudieron generar las preguntas. Intenta de nuevo.';

/** Una generación terminada se olvida después de una hora. */
const OLVIDAR_TRAS_MS = 60 * 60 * 1000;

/**
 * El estado de cada generación, en memoria (ADR-045 punto 1): sin tabla
 * nueva, no cambia el MER. Si el servidor se reinicia, las generaciones en
 * curso se pierden; en la base no queda nada a medias (ADR-027).
 */
@Injectable()
export class Generaciones {
  private readonly todas = new Map<string, Generacion>();

  crear(idDocente: number): Generacion {
    const generacion: Generacion = {
      id: randomUUID(),
      idDocente,
      estado: 'generando',
      idExperiencia: null,
      mensaje: null,
    };
    this.todas.set(generacion.id, generacion);
    return generacion;
  }

  buscar(id: string): Generacion | undefined {
    return this.todas.get(id);
  }

  lista(id: string, idExperiencia: number): void {
    this.terminar(id, { estado: 'lista', idExperiencia });
  }

  fallida(id: string): void {
    this.terminar(id, { estado: 'fallida', mensaje: MENSAJE_FALLIDA });
  }

  private terminar(id: string, cambios: Partial<Generacion>): void {
    const generacion = this.todas.get(id);
    if (!generacion) return;
    Object.assign(generacion, cambios);
    setTimeout(() => this.todas.delete(id), OLVIDAR_TRAS_MS).unref();
  }
}

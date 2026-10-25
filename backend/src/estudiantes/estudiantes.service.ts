import { Injectable } from '@nestjs/common';
import { EntityManager } from 'typeorm';
import { Estudiante } from './entities/estudiante.entity.js';

@Injectable()
export class EstudiantesService {
  // Recibe el EntityManager de la transacción de "Elige tu rol" (spec 20),
  // para que crear esta fila y enlazarla a la credencial pasen juntas o
  // ninguna.
  crear(
    manager: EntityManager,
    datos: { nombre: string; correo: string; avatarUrl: string | null },
  ): Promise<Estudiante> {
    return manager.save(manager.create(Estudiante, datos));
  }
}

import { Injectable } from '@nestjs/common';
import { EntityManager } from 'typeorm';
import { Docente } from './entities/docente.entity.js';

@Injectable()
export class DocentesService {
  // Recibe el EntityManager de la transacción de "Elige tu rol" (spec 20),
  // para que crear esta fila y enlazarla a la credencial pasen juntas o
  // ninguna.
  crear(
    manager: EntityManager,
    datos: { nombre: string; correo: string; avatarUrl: string | null },
  ): Promise<Docente> {
    return manager.save(manager.create(Docente, datos));
  }
}

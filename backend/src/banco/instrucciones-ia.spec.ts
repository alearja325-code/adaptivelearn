import { describe, expect, it } from 'vitest';
import {
  armarInstrucciones,
  ITEMS_POR_EVIDENCIA,
  type ContextoEvidencia,
} from './instrucciones-ia.js';

const contexto = (
  cambios: Partial<ContextoEvidencia['dba']> = {},
  formato: ContextoEvidencia['formato'] = 'single_choice',
): ContextoEvidencia => ({
  area: 'Ciencias Sociales',
  grado: { numero: 8, nombre: 'Octavo' },
  dba: {
    codigo: 'CS-08-08',
    enunciado: 'Comprende la importancia de las asociaciones.',
    ejemplo: 'A partir de la conmemoración del 1 de mayo en Colombia.',
    ejemploTieneImagen: false,
    ...cambios,
  },
  evidencia: {
    numero: 2,
    enunciado: 'Explica algunas herramientas para resolver un conflicto.',
  },
  formato,
});

describe('armarInstrucciones (ADR-045 punto 4)', () => {
  it('lleva el área, el grado, el DBA, la evidencia exacta, el formato y pide 12 ítems en JSON', () => {
    const { sistema, usuario } = armarInstrucciones(contexto());
    expect(usuario).toContain('Área: Ciencias Sociales');
    expect(usuario).toContain('Grado: 8.° (Octavo)');
    expect(usuario).toContain(
      'DBA CS-08-08: Comprende la importancia de las asociaciones.',
    );
    expect(usuario).toContain(
      '"""\nExplica algunas herramientas para resolver un conflicto.\n"""',
    );
    expect(usuario).toContain(
      `Escribe ${ITEMS_POR_EVIDENCIA} preguntas de diagnóstico de selección única`,
    );
    expect(usuario).toContain('{"items": [');
    expect(sistema).toContain('solo con un objeto JSON');
  });

  it('las reglas: solo texto (ADR-044), una correcta, distractores con su hipótesis (ADR-020), nada de «todas las anteriores», sin nombres reales', () => {
    const { usuario } = armarInstrucciones(contexto());
    expect(usuario).toContain(
      'Solo texto. Ninguna pregunta puede pedir mirar una imagen, un mapa, una gráfica',
    );
    expect(usuario).toContain('una sola respuesta correcta');
    expect(usuario).toContain('"hipotesis_error"');
    expect(usuario).toContain('no se le muestra al estudiante');
    expect(usuario).toContain(
      '"todas las anteriores", "ninguna de las anteriores"',
    );
    expect(usuario).toContain('No uses nombres de personas reales');
    expect(usuario).toContain('adecuados para la edad del grado');
  });

  it('el ejemplo del DBA como escenario (ADR-011)', () => {
    const { usuario } = armarInstrucciones(contexto());
    expect(usuario).toContain('Usa como escenario el ejemplo oficial del DBA');
    expect(usuario).toContain(
      'A partir de la conmemoración del 1 de mayo en Colombia.',
    );
    expect(usuario).not.toContain('trae una figura');
  });

  it('si el ejemplo tenía una figura, le dice que no la recibe y que no se refiera a ella', () => {
    const { usuario } = armarInstrucciones(
      contexto({ ejemploTieneImagen: true }),
    );
    expect(usuario).toContain('trae una figura');
    expect(usuario).toContain('No te refieras a ella');
  });

  it('sin ejemplo, pide un escenario cercano a un estudiante colombiano de ese grado', () => {
    const { usuario } = armarInstrucciones(contexto({ ejemplo: null }));
    expect(usuario).toContain('no tiene un ejemplo oficial');
    expect(usuario).toContain('estudiante colombiano de octavo grado');
    expect(usuario).not.toContain('Usa como escenario el ejemplo oficial');
  });

  it('la forma del JSON depende del formato', () => {
    expect(armarInstrucciones(contexto({}, 'single_choice')).usuario).toContain(
      '"es_correcta": true',
    );
    const ordenar = armarInstrucciones(contexto({}, 'ordering')).usuario;
    expect(ordenar).toContain('ordenamiento');
    expect(ordenar).toContain('"orden": 1');
    expect(ordenar).not.toContain('"es_correcta"');
    const emparejar = armarInstrucciones(contexto({}, 'matching')).usuario;
    expect(emparejar).toContain('"grupo": "izquierda"');
    expect(emparejar).toContain('número de su pareja');
  });
});

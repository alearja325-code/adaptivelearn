import { describe, expect, it } from 'vitest';
import {
  normalizarOpciones,
  validarItem,
  type ItemPropuesto,
} from './validar-item.js';

// RI-4 con los mínimos de H-9, regla por regla: cada una con un ítem válido
// y el caso inválido que la rompe (encargo 06, B.6).
const seleccion = (): ItemPropuesto => ({
  enunciado: '¿Cuánto es 2 + 3?',
  opciones: [
    { texto: '5', es_correcta: true },
    { texto: '6', es_correcta: false },
    { texto: '23', es_correcta: false },
  ],
});
const ordenar = (): ItemPropuesto => ({
  enunciado: 'Ordena de menor a mayor.',
  opciones: [
    { texto: '7', orden: 2 },
    { texto: '3', orden: 1 },
    { texto: '9', orden: 3 },
  ],
});
const emparejar = (): ItemPropuesto => ({
  enunciado: 'Une cada animal con su cubierta.',
  opciones: [
    { texto: 'Perro', grupo: 'izquierda', orden: 1 },
    { texto: 'Gallina', grupo: 'izquierda', orden: 2 },
    { texto: 'Plumas', grupo: 'derecha', orden: 2 },
    { texto: 'Pelo', grupo: 'derecha', orden: 1 },
  ],
});

describe('validarItem (RI-4, H-9)', () => {
  it('acepta un ítem válido de cada formato', () => {
    expect(validarItem('single_choice', seleccion())).toEqual([]);
    expect(validarItem('ordering', ordenar())).toEqual([]);
    expect(validarItem('matching', emparejar())).toEqual([]);
  });

  it('enunciado vacío', () => {
    expect(
      validarItem('single_choice', { ...seleccion(), enunciado: '   ' }),
    ).toContain('El enunciado no puede estar vacío.');
  });

  it('una opción vacía', () => {
    const item = seleccion();
    item.opciones[2].texto = '';
    expect(validarItem('single_choice', item)).toContain(
      'Ninguna opción puede estar vacía.',
    );
  });

  it('mínimo de opciones: 2 en selección única y en ordenamiento, 4 en emparejamiento', () => {
    const una = {
      ...seleccion(),
      opciones: [{ texto: '5', es_correcta: true }],
    };
    expect(validarItem('single_choice', una)).toContain(
      'Este formato necesita al menos 2 opciones.',
    );
    const unPaso = { ...ordenar(), opciones: [{ texto: '3', orden: 1 }] };
    expect(validarItem('ordering', unPaso)).toContain(
      'Este formato necesita al menos 2 opciones.',
    );
    const tres = { ...emparejar(), opciones: emparejar().opciones.slice(0, 3) };
    expect(validarItem('matching', tres)).toContain(
      'Este formato necesita al menos 4 opciones.',
    );
  });

  it('selección única: exactamente una correcta (ni cero ni dos)', () => {
    const ninguna = seleccion();
    ninguna.opciones[0].es_correcta = false;
    expect(validarItem('single_choice', ninguna)).toContain(
      'En selección única debe haber exactamente una opción correcta.',
    );
    const dos = seleccion();
    dos.opciones[1].es_correcta = true;
    expect(validarItem('single_choice', dos)).toContain(
      'En selección única debe haber exactamente una opción correcta.',
    );
  });

  it('ordenamiento: orden de 1 al total, sin repetidos ni huecos', () => {
    const repetido = ordenar();
    repetido.opciones[2].orden = 2;
    const hueco = ordenar();
    hueco.opciones[2].orden = 4;
    const sinOrden = ordenar();
    sinOrden.opciones[0].orden = null;
    for (const item of [repetido, hueco, sinOrden]) {
      expect(validarItem('ordering', item)).toContain(
        'En ordenamiento los números de orden deben ir de 1 al total, sin repetirse.',
      );
    }
  });

  it('emparejamiento: cada opción con su lado, al menos 2 por lado', () => {
    const sinLado = emparejar();
    sinLado.opciones[0].grupo = null;
    expect(validarItem('matching', sinLado)).toContain(
      'En emparejamiento cada opción es de la izquierda o de la derecha.',
    );
    const unLado = emparejar();
    unLado.opciones.forEach((o) => (o.grupo = 'izquierda'));
    expect(validarItem('matching', unLado)).toContain(
      'En emparejamiento cada lado necesita al menos 2 opciones.',
    );
  });

  it('emparejamiento: parejas completas, una a cada lado y sin repetir', () => {
    const repetida = emparejar();
    repetida.opciones[3].orden = 2; // dos «2» a la derecha, ningún «1»
    const sinPareja = {
      ...emparejar(),
      opciones: [
        ...emparejar().opciones,
        { texto: 'Pez', grupo: 'izquierda' as const, orden: 3 },
      ],
    };
    for (const item of [repetida, sinPareja]) {
      expect(validarItem('matching', item)).toContain(
        'En emparejamiento cada pareja tiene un número, de 1 al total, uno a cada lado y sin repetirse.',
      );
    }
  });

  it('en ordenamiento y emparejamiento ninguna opción se marca correcta, y solo emparejamiento tiene lados', () => {
    const conCorrecta = ordenar();
    conCorrecta.opciones[0].es_correcta = true;
    expect(validarItem('ordering', conCorrecta).length).toBeGreaterThan(0);
    const emparejarConCorrecta = emparejar();
    emparejarConCorrecta.opciones[0].es_correcta = true;
    expect(
      validarItem('matching', emparejarConCorrecta).length,
    ).toBeGreaterThan(0);
    const seleccionConLado = seleccion();
    seleccionConLado.opciones[0].grupo = 'izquierda';
    expect(validarItem('single_choice', seleccionConLado)).toContain(
      'En selección única las opciones no tienen grupo.',
    );
  });

  it('no revienta con datos que no son un ítem', () => {
    expect(
      validarItem('single_choice', null as unknown as ItemPropuesto).length,
    ).toBeGreaterThan(0);
    expect(
      validarItem('matching', { enunciado: 'x' } as ItemPropuesto),
    ).toContain('Faltan las opciones.');
  });
});

describe('normalizarOpciones', () => {
  it('selección única: orden nulo (`18` §15) y es_correcta sí/no; la hipótesis solo en los distractores', () => {
    const item = seleccion();
    item.opciones[0].hipotesis_error = 'no debería quedar en la correcta';
    item.opciones[1].hipotesis_error = 'suma mal';
    const [a, b, c] = normalizarOpciones('single_choice', item.opciones);
    expect([a.orden, b.orden, c.orden]).toEqual([null, null, null]);
    expect([a.es_correcta, b.es_correcta, c.es_correcta]).toEqual([
      true,
      false,
      false,
    ]);
    expect([a.hipotesis_error, b.hipotesis_error]).toEqual([null, 'suma mal']);
  });

  it('ordenamiento y emparejamiento: es_correcta nulo; grupo solo en emparejamiento', () => {
    expect(
      normalizarOpciones('ordering', ordenar().opciones).every(
        (o) => o.es_correcta === null && o.grupo === null,
      ),
    ).toBe(true);
    expect(
      normalizarOpciones('matching', emparejar().opciones).every(
        (o) => o.es_correcta === null && o.grupo,
      ),
    ).toBe(true);
  });
});

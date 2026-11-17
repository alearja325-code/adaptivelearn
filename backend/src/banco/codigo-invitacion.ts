import { randomInt } from 'node:crypto';

/** Letras y números sin los ambiguos 0, O, 1, I, L (RI-3, RF-02-06). */
export const ALFABETO_CODIGO = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';

/** Un código de invitación de 6 caracteres, al azar (con crypto). */
export function nuevoCodigo(): string {
  return Array.from(
    { length: 6 },
    () => ALFABETO_CODIGO[randomInt(ALFABETO_CODIGO.length)],
  ).join('');
}

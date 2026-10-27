// Reglas que no dependen de React, para poder probarlas solas.
import type { Usuario } from '../api/tipos';

/** RF-01-01, ventana 014 §2.4: mínimo 8 caracteres, una mayúscula y un número
 *  (la misma regla del backend: backend/src/auth/dto/password.constants.ts) */
export const REGLA_CONTRASENA = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
export const TEXTO_REGLA_CONTRASENA = 'Mínimo 8 caracteres, con una mayúscula y un número.';

/** ¿Tiene forma de correo? (ventana 018 §7: formato, nunca existencia) */
export function esCorreo(texto: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(texto.trim());
}

/**
 * A qué ventana va una cuenta, según el backend (encargo 04 §5, ADR-035):
 * sin verificar → 015; verificada sin rol → 016; con rol → 001.
 */
export function destinoDe(usuario: Usuario): '/verificar-correo' | '/completar-perfil' | '/' {
  if (usuario.estadoVerificacion === 'procesando') return '/verificar-correo';
  if (!usuario.perfil) return '/completar-perfil';
  return '/';
}

/** Variante del Dashboard (ventana 001): docente o estudiante */
export function varianteDe(usuario: Usuario): 'docente' | 'estudiante' {
  return usuario.idDocente !== null ? 'docente' : 'estudiante';
}

/**
 * Propone nombres y apellidos a partir de un nombre completo (el de Google o
 * Microsoft, o el del registro). Decisión del encargo 04, declarada: la
 * spec 016 pide prellenar los dos campos, pero el backend entrega un solo
 * texto. Con 4 palabras o más: 2 nombres y el resto apellidos; con 3: 1 y 2;
 * con 2: 1 y 1; con 1: solo nombres. Siempre editable.
 */
export function partirNombre(completo: string | null): { nombres: string; apellidos: string } {
  const p = (completo ?? '').trim().split(/\s+/).filter(Boolean);
  if (p.length === 0) return { nombres: '', apellidos: '' };
  const n = p.length >= 4 ? 2 : 1;
  return { nombres: p.slice(0, n).join(' '), apellidos: p.slice(n).join(' ') };
}

/** RF-01-05: JPG o PNG, máximo 5 MB (la regla del backend: backend/src/auth/foto.ts) */
export const MAX_BYTES_FOTO = 5 * 1024 * 1024;
export function fotoValida(archivo: File): boolean {
  return ['image/jpeg', 'image/png'].includes(archivo.type) && archivo.size <= MAX_BYTES_FOTO;
}

/**
 * Nombre sugerido de la experiencia (ventana 004 §2.3): el enunciado del DBA.
 * Decisión del encargo 04, declarada: el "enunciado truncado" de la spec es
 * visual (una línea con elipsis); como texto se corta en 160 caracteres, el
 * largo máximo del nombre en el modelo (`experiencia.nombre`, VARCHAR(160)),
 * en el último espacio y con "…".
 */
export const MAX_NOMBRE_EXPERIENCIA = 160;
export function nombreSugerido(enunciado: string): string {
  const t = enunciado.trim();
  if (t.length <= MAX_NOMBRE_EXPERIENCIA) return t;
  const corte = t.slice(0, MAX_NOMBRE_EXPERIENCIA - 1);
  const espacio = corte.lastIndexOf(' ');
  return (espacio > 80 ? corte.slice(0, espacio) : corte).replace(/[\s,;:.]+$/, '') + '…';
}

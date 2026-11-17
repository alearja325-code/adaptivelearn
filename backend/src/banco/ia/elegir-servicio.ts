import type { ConfigService } from '@nestjs/config';
import { DeepSeekServicio } from './deepseek.servicio.js';
import { IaFalsa } from './ia-falsa.js';
import type { ServicioIa } from './servicio-ia.js';

/**
 * El servicio de IA según IA_SERVICIO (ADR-045 punto 5): `deepseek` (por
 * defecto) o `falsa` (las pruebas). Sin clave, DeepSeek no impide arrancar:
 * cada generación falla con un aviso en la consola, y lo demás funciona.
 */
export function elegirServicioIa(config: ConfigService): ServicioIa {
  const cual = (config.get<string>('IA_SERVICIO') || 'deepseek')
    .trim()
    .toLowerCase();
  if (cual === 'falsa') return new IaFalsa();
  if (cual === 'deepseek') {
    return new DeepSeekServicio(
      config.get<string>('DEEPSEEK_API_KEY'),
      config.get<string>('DEEPSEEK_MODEL'),
    );
  }
  throw new Error(`IA_SERVICIO debe ser deepseek o falsa (vale "${cual}")`);
}

/** IA_TIEMPO_LIMITE_MS: un entero positivo; por defecto 180000 (RNF-13 medido el 2026-11-16, ADR-045). */
export function tiempoLimite(config: ConfigService): number {
  const texto = config.get<string>('IA_TIEMPO_LIMITE_MS')?.trim();
  if (!texto) return 180_000;
  const ms = Number(texto);
  if (!Number.isInteger(ms) || ms <= 0)
    throw new Error(
      'IA_TIEMPO_LIMITE_MS debe ser un número entero de milisegundos',
    );
  return ms;
}

import { Column, Entity, PrimaryColumn } from 'typeorm';

export type PropositoCodigo = 'verificar_correo' | 'recuperar_contrasena';

// ADR-039 (nota R4 del docente): el código de 6 dígitos en su propia tabla.
// A lo sumo uno por credencial y propósito: la llave primaria es el par.
// El vencimiento (10 min) y la espera para reenviar (30 s) se calculan
// desde `creado_en`; no se guardan.
@Entity('codigo_verificacion')
export class CodigoVerificacion {
  @PrimaryColumn({ name: 'id_credencial', type: 'int', unsigned: true })
  idCredencial: number;

  @PrimaryColumn({ type: 'enum', enum: ['verificar_correo', 'recuperar_contrasena'] })
  proposito: PropositoCodigo;

  // HMAC-SHA256 del código, en hexadecimal: nunca el código legible (RNF-08)
  @Column({ name: 'codigo_hash', type: 'char', length: 64 })
  codigoHash: string;

  @Column({ name: 'creado_en', type: 'datetime' })
  creadoEn: Date;

  // Intentos fallidos con este código; al quinto deja de servir
  @Column({ type: 'tinyint', unsigned: true, default: 0 })
  intentos: number;
}

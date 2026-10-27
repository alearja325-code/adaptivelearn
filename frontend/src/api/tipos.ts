// Los datos que viajan entre el frontend y el backend. Salen del código del
// backend (backend/src/), no de memoria: los nombres de campo son los suyos.

export type Rol = 'user' | 'docente' | 'estudiante' | 'admin';

/** AuthResponse de la guía: register, login, elegir-rol, google, microsoft */
export interface RespuestaSesion {
  user: { id: number; email: string; fullName: string | null; role: Rol };
  token: string;
}

/** El usuario de GET /auth/profile (la entidad User serializada) */
export interface Usuario {
  id: number;
  email: string;
  proveedor: 'correo' | 'google' | 'microsoft';
  estadoVerificacion: 'procesando' | 'verificado';
  idDocente: number | null;
  idEstudiante: number | null;
  role: Rol;
  fullName: string | null;
  perfil: { nombres: string; apellidos: string; avatarUrl: string | null } | null;
}

export interface Area {
  codigo: string;
  nombre: string;
}

export interface Grado {
  numero: number;
  nombre: string;
  nivel: string;
}

export interface DbaResumen {
  codigo: string;
  enunciado: string;
  area: Area;
  grado: { numero: number; nombre: string };
}

export interface DbaDetalle extends DbaResumen {
  ejemplo: string | null;
  documento: { titulo: string; version: string; anio: number; paginas: number; urlOficial: string };
  evidencias: {
    numero: number;
    enunciado: string;
    admiteFormatoCerrado: boolean | null;
    formato: string | null;
  }[];
}

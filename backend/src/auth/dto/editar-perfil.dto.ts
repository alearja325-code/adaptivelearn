import { PartialType } from '@nestjs/mapped-types';
import { PerfilDto } from './perfil.dto.js';

// Editar mi perfil (CU-09, ventana 026): nombres y apellidos, cada uno
// opcional pero nunca vacío; la foto, como archivo. El correo y el rol no
// se editan: forbidNonWhitelisted responde 400 si llegan.
export class EditarPerfilDto extends PartialType(PerfilDto) {}

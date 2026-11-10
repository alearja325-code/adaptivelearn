// Ventana 004 — Crear Experiencia: Paso 3 (Confirmar)
// Spec: docs/modesec/fase-2-diseno-multimedial/07-spec-crear-experiencia-paso3.md
// Sin backend en esta etapa (encargo 04 §4.3): "Crear experiencia" se ve y se
// habilita como dice la spec, pero no llama a nada ni abre el Modal: Cargando;
// muestra, en el lugar del mensaje de error de §7 y con su mismo estilo pero en
// color Informativo, "Crear la experiencia llega en la siguiente etapa."
import { useState, type ReactNode } from 'react';
import type { DbaResumen } from '../../api/tipos';
import { BotonGhost, BotonPrimario } from '../../componentes/Botones';
import { Mensaje } from '../../componentes/Formulario';
import { nombreSugerido } from '../../sesion/reglas';
import { Subencabezado } from './Subencabezado';

export const AVISO_CREAR = 'Crear la experiencia llega en la siguiente etapa.';

interface Props {
  dba: DbaResumen;
  nombre: { texto: string; editado: boolean } | null;
  onNombre: (texto: string, editado: boolean) => void;
  onVolver: () => void;
}

export function Paso3Confirmar({ dba, nombre, onNombre, onVolver }: Props) {
  const texto = nombre?.texto ?? nombreSugerido(dba.enunciado);
  const editado = nombre?.editado ?? false;
  const [aviso, setAviso] = useState(false);

  return (
    <>
      <Subencabezado titulo="Confirmar" descripcion="Dale un nombre a la experiencia y revisa qué va a ocurrir." />

      {/* §2.3 Campo Nombre de la experiencia */}
      <label className="flex flex-col gap-8">
        <span className="text-caption font-regular text-secondary">Nombre de la experiencia</span>
        <input
          value={texto}
          maxLength={160}
          onFocus={(e) => e.target.select()}
          onChange={(e) => {
            onNombre(e.target.value, true);
            setAviso(false);
          }}
          className={`h-44 w-full rounded-12 borde-1 border-border bg-surface-0 px-16 text-boton font-medium outline-none focus:border-primary-ink ${
            editado ? 'text-primary-ink' : 'text-muted'
          }`}
        />
      </label>

      {/* §2.4 Card informativa "Qué va a pasar" */}
      <div className="flex flex-col gap-8">
        <h4 className="text-body font-bold text-primary-ink">Qué va a pasar</h4>
        <div className="flex flex-col gap-16 rounded-16 borde-1 border-border bg-surface-0 p-16">
          <Info etiqueta="¿Qué es?">
            Al crear esta experiencia, el sistema genera un banco de preguntas y ejercicios para cada evidencia del DBA que
            elegiste — usando como referencia el enunciado oficial del MEN, no contenido inventado sin anclar.
          </Info>
          <Info etiqueta="¿Para qué sirve?">
            Te da, en un solo lugar, todo el material de diagnóstico de este DBA listo para revisar, antes de decidir si es
            adecuado para tu grupo.
          </Info>
          <Info etiqueta="¿Cómo funciona?">
            Queda en estado Borrador. Puedes revisar y editar cada pregunta antes de publicarla — tus estudiantes no la ven
            hasta que tú decidas hacerlo.
          </Info>
        </div>
      </div>

      {/* §2.5 Footer; el aviso va debajo, en el lugar del mensaje de error de §7 */}
      <div className="flex flex-col gap-8">
        <div className="mt-24 grid grid-cols-2 gap-12">
          <BotonGhost onClick={onVolver}>Volver</BotonGhost>
          <BotonPrimario disabled={texto.trim() === ''} onClick={() => setAviso(true)}>
            Crear experiencia
          </BotonPrimario>
        </div>
        <Mensaje texto={aviso ? AVISO_CREAR : null} tipo="informativo" />
      </div>
    </>
  );
}

function Info({ etiqueta, children }: { etiqueta: string; children: ReactNode }) {
  return (
    <div className="flex flex-col gap-4">
      <p className="text-caption font-regular text-muted">{etiqueta}</p>
      <p className="text-body font-regular text-primary-ink">{children}</p>
    </div>
  );
}

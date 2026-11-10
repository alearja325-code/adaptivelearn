// Ventanas 002, 003 y 004 — Crear experiencia: el marco compartido y sus 3 pasos
// Specs: docs/modesec/fase-2-diseno-multimedial/05-spec-crear-experiencia-paso1.md (marco + Paso 1),
//        06-spec-crear-experiencia-paso2.md (Paso 2) y 07-spec-crear-experiencia-paso3.md (Paso 3)
// Marco (002 §2.1): ancho fijo 912, alto Hug hasta "alto de pantalla menos 48",
// Radio 24, Fill #FFFFFF, Stroke 1 #E7E7E7, Padding 32, Gap 24; encabezado de 3
// zonas y stepper de 3 círculos.
import { useState } from "react";
import type { Area, DbaResumen } from "../api/tipos";
import { BotonCerrar } from "../componentes/Botones";
import { EncabezadoModal, Modal } from "../componentes/Modal";
import { Paso1Area } from "./crear/Paso1Area";
import { Paso2Dba } from "./crear/Paso2Dba";
import { Paso3Confirmar } from "./crear/Paso3Confirmar";
import { Stepper } from "./crear/Stepper";

export function V002CrearExperiencia({ onCerrar }: { onCerrar: () => void }) {
  const [paso, setPasoActual] = useState<1 | 2 | 3>(1);
  // M7: el paso nuevo entra desde la derecha al avanzar y desde la izquierda al volver
  const [sentido, setSentido] = useState<"adelante" | "atras" | null>(null);
  const setPaso = (nuevo: 1 | 2 | 3) => {
    setSentido(nuevo > paso ? "adelante" : "atras");
    setPasoActual(nuevo);
  };
  const entrada =
    sentido === null
      ? ""
      : sentido === "adelante"
        ? "animate-paso-adelante"
        : "animate-paso-atras";
  const [area, setArea] = useState<Area | null>(null);
  const [dba, setDba] = useState<DbaResumen | null>(null);
  // El nombre se conserva al volver del Paso 3 al 2 y regresar con el mismo DBA
  const [nombre, setNombre] = useState<{
    dba: string;
    texto: string;
    editado: boolean;
  } | null>(null);

  return (
    <Modal etiqueta="Crear experiencia" onCerrar={onCerrar}>
      <div className="flex max-h-alto-modal w-912 flex-col gap-24 rounded-24 borde-1 border-border bg-surface-0 p-32">
        <EncabezadoModal
          titulo="Crear experiencia"
          cerrar={<BotonCerrar onClick={onCerrar} />}
        />
        <Stepper paso={paso} />
        <div
          key={paso}
          className={`flex min-h-0 flex-1 flex-col gap-24 ${entrada}`}
        >
          {paso === 1 && (
            <Paso1Area
              elegida={area}
              onElegir={(a) => {
                // otra área: el DBA elegido ya no es de ella
                if (a.codigo !== area?.codigo) setDba(null);
                setArea(a);
              }}
              onContinuar={() => setPaso(2)}
            />
          )}
          {paso === 2 && area && (
            <Paso2Dba
              area={area}
              elegido={dba}
              onElegir={setDba}
              onVolver={() => setPaso(1)}
              onContinuar={() => setPaso(3)}
            />
          )}
          {paso === 3 && dba && (
            <Paso3Confirmar
              dba={dba}
              nombre={nombre?.dba === dba.codigo ? nombre : null}
              onNombre={(texto, editado) =>
                setNombre({ dba: dba.codigo, texto, editado })
              }
              onVolver={() => setPaso(2)}
            />
          )}
        </div>
      </div>
    </Modal>
  );
}

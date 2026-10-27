// Página de retorno de Google y Microsoft (ventana 014 §7): la abre el
// proveedor en la ventana emergente con el ID token en la dirección
// (#id_token=…), se lo pasa a la ventana que la abrió y se cierra.
// No es una ventana de la Fase II: no muestra nada propio.
import { useEffect } from 'react';
import { leerRetorno } from '../sesion/proveedores';

export function RetornoOAuth() {
  useEffect(() => {
    const { idToken, state } = leerRetorno(window.location.hash);
    window.opener?.postMessage({ tipo: 'oauth-retorno', idToken, state }, window.location.origin);
    window.close();
  }, []);
  return null;
}

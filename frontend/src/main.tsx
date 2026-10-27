import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router';
import { App } from './App';
import { FlujoProveedor } from './sesion/FlujoContexto';
import { SesionProveedor } from './sesion/SesionContexto';
import './estilos/index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <SesionProveedor>
        <FlujoProveedor>
          <App />
        </FlujoProveedor>
      </SesionProveedor>
    </BrowserRouter>
  </StrictMode>,
);

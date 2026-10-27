# Marcas de terceros

`google.svg` y `microsoft.svg` son los logos oficiales de Google y Microsoft,
con sus colores de marca, para los botones de la ventana 014 (§2.8). La spec
lo dice: *"no son íconos de este sistema, son marcas de terceros con su
propia guía de marca"* — por eso sus colores no están en `tokens.json`, y
`scripts/verificar-estilos.mjs` no revisa esta carpeta. No se recolorean ni
se deforman (`30-indice-recursos.md`).

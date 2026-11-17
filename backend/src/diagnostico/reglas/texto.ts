/** Para buscar sin distinguir mayúsculas ni tildes ("José" = "jose"). */
export function normalizar(texto: string): string {
  return texto.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
}

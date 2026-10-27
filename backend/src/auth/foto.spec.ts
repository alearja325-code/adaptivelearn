import { describe, expect, it } from 'vitest';
import { extensionFoto } from './foto.js';

// RF-01-05: JPG o PNG, decidido por los primeros bytes del archivo
describe('extensionFoto', () => {
  it('reconoce JPG y PNG por su firma', () => {
    expect(extensionFoto(Buffer.from([0xff, 0xd8, 0xff, 0xe0, 0x00]))).toBe('jpg');
    expect(extensionFoto(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00]))).toBe('png');
  });
  it('rechaza lo demás, aunque se llame .png', () => {
    expect(extensionFoto(Buffer.from('GIF89a'))).toBeNull();
    expect(extensionFoto(Buffer.from('<svg></svg>'))).toBeNull();
    expect(extensionFoto(Buffer.alloc(0))).toBeNull();
  });
});

// Build favicon.ico (16, 32, 48 px, PNG-encoded entries) and favicon.png from the mark.
// Usage (from the repo root): node favicon.js
const fs = require('fs');
const sharp = require(require.resolve('sharp', { paths: [process.cwd()] }));

const mark = 'apps/frontend/public/brand/geoscribe-social-icon.svg';
const out = 'apps/frontend/public';

const png = (size) =>
  sharp(fs.readFileSync(mark), { density: 72 * (size / 96) * 4 })
    .resize(size, size)
    .png()
    .toBuffer();

(async () => {
  const sizes = [16, 32, 48];
  const images = await Promise.all(sizes.map(png));

  const header = Buffer.alloc(6);
  header.writeUInt16LE(0, 0); // reserved
  header.writeUInt16LE(1, 2); // type: icon
  header.writeUInt16LE(sizes.length, 4);

  let offset = 6 + 16 * sizes.length;
  const entries = images.map((image, index) => {
    const entry = Buffer.alloc(16);
    entry.writeUInt8(sizes[index], 0); // width
    entry.writeUInt8(sizes[index], 1); // height
    entry.writeUInt8(0, 2); // palette
    entry.writeUInt8(0, 3); // reserved
    entry.writeUInt16LE(1, 4); // colour planes
    entry.writeUInt16LE(32, 6); // bits per pixel
    entry.writeUInt32LE(image.length, 8);
    entry.writeUInt32LE(offset, 12);
    offset += image.length;
    return entry;
  });

  fs.writeFileSync(`${out}/favicon.ico`, Buffer.concat([header, ...entries, ...images]));
  fs.writeFileSync(`${out}/favicon.png`, await png(64));
  console.log('favicon.ico', fs.statSync(`${out}/favicon.ico`).size, 'bytes');
})();

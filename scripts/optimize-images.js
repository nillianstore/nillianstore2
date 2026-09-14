const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const IMG_DIR = path.join(__dirname, '..', 'img');

// Configuration
const MAX_COVER = 800;     // Max dimension for cover images (largest cover display ~500px on product pages)
const MAX_GALLERY = 800;   // Max dimension for gallery images
const MAX_LOGO = 80;       // Logo size (2x for retina at 40px display)
const MAX_TEMPLATE = 1200;  // Max dimension for template/misc images
const WEBP_QUALITY = 80;

// Check if filename is a gallery image (has -1, -2, -3, etc. suffix)
function isGalleryImage(name) {
  return /-[0-9]+\.(webp|png|jpg)$/i.test(name);
}

// Check if filename is a product cover (B0*.webp or b0*.webp without suffix)
function isProductCover(name) {
  return /^(B0|b0)[A-Z0-9]+\.(webp|png)$/i.test(name);
}

// Check if filename is the logo
function isLogo(name) {
  return name.toLowerCase() === 'eleventy.png';
}

async function optimizeImage(filename) {
  const fullPath = path.join(IMG_DIR, filename);
  const stat = fs.statSync(fullPath);
  const originalSizeKB = Math.round(stat.size / 1024);

  let maxSize;
  let isWebp = filename.toLowerCase().endsWith('.webp');

  if (isLogo(filename)) {
    maxSize = MAX_LOGO;
  } else if (isGalleryImage(filename)) {
    maxSize = MAX_GALLERY;
  } else if (isProductCover(filename)) {
    maxSize = MAX_COVER;
  } else {
    maxSize = MAX_TEMPLATE;
  }

  try {
    // Read once into a buffer: avoids repeated file handles that race with
    // Windows antivirus/lockers during sequential processing.
    const input = fs.readFileSync(fullPath);
    const meta = await sharp(input).metadata();
    const width = meta.width, height = meta.height;

    // Skip if already small enough
    if (width <= maxSize && height <= maxSize && originalSizeKB < 50) {
      console.log(`  SKIP  ${filename} (${width}x${height}, ${originalSizeKB}KB) - already optimized`);
      return { filename, skipped: true, originalSizeKB };
    }

    const out = isWebp ? sharp(input).webp({ quality: WEBP_QUALITY }) : sharp(input);
    const buffer = await out
      .resize(maxSize, maxSize, { fit: 'inside', withoutEnlargement: true })
      .toBuffer();
    fs.writeFileSync(fullPath, buffer);

    const newSize = fs.statSync(fullPath).size;
    const newSizeKB = Math.round(newSize / 1024);
    const savings = Math.round((1 - newSize / stat.size) * 100);

    console.log(`  DONE  ${filename}: ${width}x${height} ${originalSizeKB}KB -> ${newSizeKB}KB (${savings}% saved)`);
    return { filename, skipped: false, originalSizeKB, newSizeKB, savings };

  } catch (err) {
    console.error(`  ERROR ${filename}: ${err.message}`);
    return { filename, error: err.message };
  }
}

async function main() {
  console.log('\n=== Image Optimization ===\n');
  
  if (!fs.existsSync(IMG_DIR)) {
    console.error('Image directory not found:', IMG_DIR);
    process.exit(1);
  }

  const files = fs.readdirSync(IMG_DIR).filter(f => 
    /\.(webp|png|jpg|jpeg)$/i.test(f) && !f.includes('.tmp')
  );

  console.log(`Found ${files.length} images to process\n`);

  let totalOriginal = 0;
  let totalNew = 0;
  let optimized = 0;
  let skipped = 0;

  for (const file of files) {
    const result = await optimizeImage(file);
    if (result.skipped) {
      skipped++;
      totalOriginal += result.originalSizeKB;
      totalNew += result.originalSizeKB;
    } else if (!result.error) {
      optimized++;
      totalOriginal += result.originalSizeKB;
      totalNew += result.newSizeKB;
    }
  }

  console.log('\n=== Summary ===');
  console.log(`Total images: ${files.length}`);
  console.log(`Optimized: ${optimized}`);
  console.log(`Skipped (already small): ${skipped}`);
  console.log(`Total size: ${totalOriginal}KB -> ${totalNew}KB (${Math.round((1 - totalNew / totalOriginal) * 100)}% saved)`);
  console.log('');
}

main().catch(console.error);

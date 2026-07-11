#!/usr/bin/env node
const fs = require('fs').promises;
const path = require('path');

const ROOT = path.resolve(process.cwd(), '_site');
const BAD_RE = /[?#]/;

async function walk(dir) {
  let results = [];
  const entries = await fs.readdir(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      results = results.concat(await walk(full));
    } else if (e.isFile()) {
      results.push(full);
    }
  }
  return results;
}

(async function main(){
  try {
    // Ensure _site exists
    await fs.access(ROOT);
  } catch (err) {
    console.error('Error: _site directory not found. Run the build first (npm run build).');
    process.exit(2);
  }

  try {
    const files = await walk(ROOT);
    const bad = files.filter(f => BAD_RE.test(path.relative(ROOT, f)));
    if (bad.length > 0) {
      console.error('Filenames containing forbidden characters [?#] were found:');
      bad.forEach(f => console.error(' - ' + path.relative(ROOT, f)));
      process.exit(1);
    }
    console.log('OK: No filenames with # or ? found in _site');
    process.exit(0);
  } catch (err) {
    console.error('Error while scanning _site:', err);
    process.exit(2);
  }
})();
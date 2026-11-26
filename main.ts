// Copies the pre-rendered front page (entry.png, built by draw.py) to the output directory.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const src = join(here, "entry.png");
const dest = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);

// Verify the copy: a truncated or partial write must never pass silently.
const srcSize = statSync(src).size;
const destSize = statSync(dest).size;
if (destSize !== srcSize) {
  throw new Error(`copy verification failed: ${dest} is ${destSize} bytes, source is ${srcSize} bytes`);
}
console.log(`wrote ${dest} (${destSize} bytes, size verified)`);

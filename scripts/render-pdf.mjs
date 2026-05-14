import { mkdir } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

import { chromium } from "playwright";

const inputPath = path.resolve(process.argv[2] ?? "index.html");
const outputPath = path.resolve(
  process.argv[3] ?? "production-ai-engineering.pdf",
);

await mkdir(path.dirname(outputPath), { recursive: true });

let browser;

try {
  browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto(pathToFileURL(inputPath).href, { waitUntil: "networkidle" });
  await page.emulateMedia({ media: "print" });
  await page.pdf({
    path: outputPath,
    format: "A4",
    printBackground: true,
    margin: {
      top: "16mm",
      right: "14mm",
      bottom: "16mm",
      left: "14mm",
    },
  });

  console.log(`Wrote ${path.relative(process.cwd(), outputPath)}`);
} finally {
  await browser?.close();
}

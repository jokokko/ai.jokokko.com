import path from "node:path";

import { chromium } from "playwright";

const outputPath = path.resolve(process.argv[2] ?? "og-image.png");

const html = String.raw`<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    width: 1200px;
    height: 630px;
    display: grid;
    place-items: center;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #111827;
    background:
      linear-gradient(90deg, #003580 0 18px, transparent 18px),
      linear-gradient(180deg, #f8fafc 0%, #ffffff 58%, #eef2f7 100%);
  }
  main {
    width: 1040px;
    display: grid;
    gap: 34px;
  }
  h1 {
    margin: 0;
    max-width: 900px;
    font-size: 82px;
    line-height: 0.98;
    font-weight: 780;
    letter-spacing: 0;
  }
  p {
    margin: 0;
    max-width: 900px;
    font-size: 31px;
    line-height: 1.24;
    color: #374151;
  }
  footer {
    margin-top: 32px;
    display: flex;
    align-items: center;
    gap: 18px;
    font-size: 25px;
    color: #003580;
    font-weight: 650;
  }
  .rule {
    width: 84px;
    height: 4px;
    background: #ffb000;
  }
</style>
</head>
<body>
<main>
  <h1>Production AI Engineering</h1>
  <p>A practical guide to shipping LLM-backed systems that survive contact with production.</p>
  <footer><span class="rule"></span><span>Joona-Pekka Kokko · ai.jokokko.com</span></footer>
</main>
</body>
</html>`;

let browser;

try {
  browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await page.setContent(html, { waitUntil: "networkidle" });
  await page.screenshot({ path: outputPath, type: "png" });
  console.log(`Wrote ${path.relative(process.cwd(), outputPath)}`);
} finally {
  await browser?.close();
}

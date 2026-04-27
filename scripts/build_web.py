#!/usr/bin/env python3
"""
Build index.html from production-ai-engineering.md using web.css.

Renders the markdown article to a self-contained HTML page suitable for
deployment as a static site (Cloudflare Pages, GitHub Pages, etc.).

The print stylesheet (style.css) and the PDF build are unchanged — this
script targets screen reading only.

Usage:
    python scripts/build_web.py
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parent.parent
SRC_MD = ROOT / "production-ai-engineering.md"
SRC_CSS = ROOT / "web.css"
OUT_HTML = ROOT / "index.html"

TITLE = "Production AI Engineering"
DESCRIPTION = (
    "What you actually need to know to ship LLM-backed systems that don't "
    "fall over. Foundations, RAG, agents, evaluation, production."
)
CANONICAL_URL = "https://ai.jokokko.com/"
PDF_URL = "production-ai-engineering.pdf"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


def render_body(md_text: str) -> str:
    # Strip the h1 + byline div from the source — we render those ourselves
    # so the page has a structured header section.
    lines = md_text.splitlines()
    out_lines: list[str] = []
    skipped_h1 = False
    in_byline = False
    for line in lines:
        if not skipped_h1 and line.startswith("# "):
            skipped_h1 = True
            continue
        if line.strip().startswith('<div class="byline">'):
            in_byline = True
            if line.strip().endswith("</div>"):
                in_byline = False
            continue
        if in_byline:
            if "</div>" in line:
                in_byline = False
            continue
        out_lines.append(line)

    stripped = "\n".join(out_lines).lstrip("\n")

    md = markdown.Markdown(
        extensions=[
            "extra",  # tables, fenced code, attr_list, etc.
            "toc",
            "sane_lists",
        ],
        extension_configs={
            "toc": {
                "permalink": "¶",
                "permalink_class": "anchor",
                "permalink_title": "Permalink to this section",
                "slugify": lambda value, sep: slugify(value).replace(" ", sep),
            },
        },
    )
    html = md.convert(stripped)

    # Wrap tables for horizontal scroll on mobile.
    html = re.sub(
        r"(<table>[\s\S]*?</table>)",
        r'<div class="table-wrap">\1</div>',
        html,
    )
    return html


def build() -> None:
    if not SRC_MD.exists():
        sys.exit(f"missing source: {SRC_MD}")
    if not SRC_CSS.exists():
        sys.exit(f"missing stylesheet: {SRC_CSS}")

    md_text = SRC_MD.read_text(encoding="utf-8")
    css_text = SRC_CSS.read_text(encoding="utf-8")
    body = render_body(md_text)

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESCRIPTION}">
<meta name="author" content="Joona-Pekka Kokko">
<link rel="canonical" href="{CANONICAL_URL}">

<meta property="og:type" content="article">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:url" content="{CANONICAL_URL}">
<meta property="og:site_name" content="ai.jokokko.com">

<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESCRIPTION}">

<style>
{css_text}
</style>
</head>
<body>
<main>
<h1>{TITLE}</h1>
<div class="byline">Joona-Pekka Kokko · <a href="https://jokokko.com">jokokko.com</a> · <a href="https://github.com/jokokko">github.com/jokokko</a></div>
<div class="meta">
  <a href="{PDF_URL}">Download PDF</a>
</div>
{body}
</main>
<footer>
<p>Joona-Pekka Kokko · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a></p>
</footer>
</body>
</html>
"""

    OUT_HTML.write_text(html, encoding="utf-8")
    size_kb = OUT_HTML.stat().st_size / 1024
    print(f"wrote {OUT_HTML.relative_to(ROOT)} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    build()

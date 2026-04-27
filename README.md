# Production AI Engineering

What you actually need to know to ship LLM-backed systems that don't fall over. Written for engineers, not procurement.

**[🌐 Read on the web](https://ai.jokokko.com) · [📄 Read on GitHub](./production-ai-engineering.md) · [⬇ Download PDF](./production-ai-engineering.pdf)**

---

## TL;DR — top 5 if you read nothing else

1. **Build an eval set before anything else.** No eval set, no way to tell if a change is an improvement.
2. **Use prompt caching.** ~10× cheaper input tokens for stable prefixes.
3. **Hybrid retrieval (vector + BM25 via RRF), then rerank.** Pure vector search misses identifiers, error codes, version numbers.
4. **Structured outputs via native APIs**, not "please return JSON". Validate and repair on failure.
5. **For agents: budget caps, sandboxed code, HITL in trusted UI.** Loop budgets stop runaway spend; destructive actions need confirmation outside the model loop.

Full rationale and detail in the [article](./production-ai-engineering.md).

---

## What's covered

| Section | Topics |
|---|---|
| **1. Foundations** | Classical vs. LLM systems · request cycle · model selection · transformer mechanics · controlling randomness |
| **2. Context engineering and RAG** | Prompt-engineering principles · ingestion · retrieval · reranking · long-context vs. RAG · retrieval evaluation · semantic caching |
| **3. Agents** | Agent loop · MCP · workflow patterns · structured outputs · tool design · resilience · side effects |
| **4. Evaluation** | The eval loop · error analysis · LLM-as-judge · human evaluation · synthetic and adversarial testing |
| **5. Production** | Quantization · fine-tuning · guardrails · observability · pre-launch checklist |

## Why this exists

Most LLM "best-practice" writing is one of two things: shallow takeaways with no implementation detail, or vendor marketing with framework acronyms. This is neither. It is the distilled set of decisions that determine whether an LLM-backed system survives contact with production.

The document is opinionated where opinions are warranted by evidence and neutral where they aren't. It does not claim novelty — it claims usefulness as a single reference for an engineer who needs to make these decisions this quarter.

## Builds

Two render targets share `production-ai-engineering.md` as the single source of truth:

| Target | Output | Stylesheet | Build script |
|---|---|---|---|
| Print / archival | `production-ai-engineering.pdf` | `style.css` (JetBrains Mono, A4) | `scripts/build.sh` / `scripts/build.ps1` |
| Web (`ai.jokokko.com`) | `index.html` | `web.css` (system fonts, responsive) | `scripts/build_web.py` |

### Web build

```bash
pip install -r requirements.txt
python scripts/build_web.py
```

Produces `index.html` with the stylesheet inlined into a `<style>` block, so the page is a single self-contained file. CI rebuilds and fails the run if the committed `index.html` is out of date — keep it in sync when editing the markdown.

### PDF build

The PDF is regenerated on every change to the article source. To rebuild locally:

**Linux / macOS:** `./scripts/build.sh` — requires `pandoc`, `wkhtmltopdf`, `npm`, and `python3`.
**Windows (PowerShell):** `./scripts/build.ps1` — requires `pandoc`, `wkhtmltopdf`, `npm`, and `python`.

The PDF build:
1. Fetches JetBrains Mono via `@fontsource/jetbrains-mono` from npm.
2. Generates `dist/style.css` by base64-embedding the four needed font weights into `@font-face` blocks prepended to `style.css`.
3. Runs `pandoc` to convert `production-ai-engineering.md` → `dist/production-ai-engineering.html` with embedded CSS.
4. Runs `wkhtmltopdf` to convert HTML → `production-ai-engineering.pdf`.

The build is reproducible — the committed PDF is what the build script produces.

## Hosting

The web version is served by Cloudflare Pages from the repository root: `index.html`, `web.css`, the PDF, and `_headers` are all the deploy needs. No build step runs in Cloudflare — the committed `index.html` is served directly.

## Contributing

Issues and pull requests welcome. This is a living document; corrections, additions, and updates as the field evolves are encouraged. See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

Content is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](./LICENSE). Build scripts and CSS are in the public domain (CC0) — use however you want.

## Author

**Joona-Pekka Kokko** — [jokokko.com](https://jokokko.com) · [github.com/jokokko](https://github.com/jokokko)

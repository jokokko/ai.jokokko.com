# Production AI Engineering

A practical guide to shipping LLM-backed systems that survive contact with production.

This repository is primarily the publication source for the article. The important artifact is the writing itself, not the tooling around it.

Read it here:

- Web: [ai.jokokko.com](https://ai.jokokko.com)
- Markdown: [production-ai-engineering.md](./production-ai-engineering.md)
- PDF: [production-ai-engineering.pdf](./production-ai-engineering.pdf)
- LLM-friendly index: [llms.txt](./llms.txt)
- LLM-friendly full text: [llms-full.txt](./llms-full.txt)

## What It Covers

The article is written for engineers building or operating LLM-backed systems. It focuses on decisions that affect reliability, cost, latency, security, and maintainability.

Core topics:

- Foundations of LLM-backed services
- Context engineering and retrieval-augmented generation
- Agents, tools, MCP, and workflow design
- Evaluation, error analysis, and LLM-as-judge
- Production concerns: observability, guardrails, fine-tuning, quantization, and launch readiness

## Central Claims

If you only read the short version:

1. Build an eval set before anything else.
2. Use prompt caching where the provider and model support it.
3. Use hybrid retrieval, not pure vector search.
4. Use native structured-output APIs instead of asking for JSON in prose.
5. Put budget caps, sandboxing, and human approval around agentic systems.

The article expands these into implementation-level guidance and tradeoffs.

## Files

- [production-ai-engineering.md](./production-ai-engineering.md) is the canonical article text.
- [index.html](./index.html) is the web version served at the site root.
- [production-ai-engineering.pdf](./production-ai-engineering.pdf) is generated from the web version.
- [og-image.png](./og-image.png) is the social preview image referenced by the HTML metadata.
- [llms.txt](./llms.txt) and [llms-full.txt](./llms-full.txt) are entry points for language models and AI tooling.
- [sitemap.xml](./sitemap.xml) and [robots.txt](./robots.txt) describe the public crawl surface.
- [LICENSE](./LICENSE) contains the content license.

The Markdown and HTML versions are currently maintained together. They are not byte-identical because one is source text and the other is a rendered web page, but the article body is intended to stay the same.

## Maintenance

The site is served as static files from the repository root. The PDF can be regenerated from `index.html`:

```sh
npm install
npm run pdf:install
npm run artifacts
```

This writes `production-ai-engineering.pdf` and `og-image.png` in the repository root.

## License

Content licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](./LICENSE).

## Author

Joona-Pekka Kokko  
[jokokko.com](https://jokokko.com) · [github.com/jokokko](https://github.com/jokokko)

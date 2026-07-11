A flat collection of independent CLI entry points (no shared package) each driven by a `main()` guarded by `if __name__ == "__main__"`:
- `blog_bot.py` — picks an unpicked product from `./shop/*.md`, calls the Groq OpenAI-compatible chat endpoint (`llama-3.3-70b-versatile`) with a structured prompt, then writes an Eleventy post under `./posts/` with YAML frontmatter and embedded Amazon buy-button HTML; tracks already-posted products in `./blog_log.json`.
- `social_bot.py` — same product-selection loop but posts to Meta Graph API v18 (Instagram single/carousel + Facebook page photos), retries up to 3 times, persists a capped `./social_log.json`, and optionally pushes it back to GitHub via `subprocess` using a `GITHUB_TOKEN`.
- `verify_links.py` — cross-checks every file in `./posts/` against the source `./shop/` mapping to flag mismatched Amazon links.
- `test_frontmatter.py` — ad-hoc sanity loader for two known shop SKUs.
- `scripts/check-filenames.js` — Node script that walks `_site/` after build and fails if any filename contains `?` or `#`.
- `scripts/test_blog_bot_run.py` — unit-style smoke test importing `create_blog_file` directly.

Dependency direction is one-way: scripts read `./shop/*.md` and write into `./posts/`; they never import each other. All secrets are consumed exclusively through `os.getenv` (GROQ_API_KEY, META_ACCESS_TOKEN, FB_PAGE_ID, IG_USER_ID, GITHUB_TOKEN).
---
kind: build_system
name: Eleventy Static Site Build and Netlify CI/CD Pipeline
category: build_system
scope:
    - '**'
source_files:
    - .eleventy.js
    - package.json
    - netlify.toml
    - .github/workflows/build-check.yml
    - .github/workflows/validate-site.yml
    - .github/workflows/blog_bot.yml
    - .github/workflows/social_bot.yml
---

This repository uses Eleventy (v2 canary) as its static site generator, with a Node.js-based build pipeline orchestrated through npm scripts and GitHub Actions, targeting Netlify for hosting.

Build system and toolchain
- Core SSG: @11ty/eleventy v2 canary, configured in .eleventy.js. Template engine is Nunjucks (njk) for both HTML and Markdown; Liquid and plain HTML are also supported.
- Output directory: _site, declared in the Eleventy config dir.output.
- Asset passthrough: img, css, feed, videos, and robots.txt are copied verbatim into _site.
- Markdown pipeline: custom markdown-it instance with html, breaks, linkify, plus markdown-it-anchor for heading permalinks.
- Plugins: @11ty/eleventy-plugin-rss, @11ty/eleventy-plugin-syntaxhighlight, @11ty/eleventy-navigation.
- Global data: site.url = https://www.nillianstore.com; deep merge enabled via setDataDeepMerge(true).
- Layout aliases: post -> layouts/post.njk, shop -> layouts/shop.njk.
- Custom filters: readableDate, htmlDateString, isoDateTime (Asia/Dubai), head, min, safeSlug (sanitizes tags to hyphenated ASCII slugs), filterTagList, sanitize, xmlEncode.
- Development server: Eleventy's built-in BrowserSync with a middleware that serves _site/404.html on unmatched routes locally.

npm scripts
- build: runs eleventy
- watch: eleventy --watch
- serve / start: eleventy --serve
- debug: DEBUG=* eleventy
- check:filenames: runs scripts/check-filenames.js to validate generated filenames against filesystem constraints.

CI/CD (GitHub Actions)
Four workflows cover the full lifecycle:

1. build-check.yml - On push/PR to main: checkout, setup Node 18, npm install, run npx @11ty/eleventy.
2. validate-site.yml - On push/PR to main: npm ci + npm run build + node scripts/check-filenames.js to catch invalid filenames early.
3. blog_bot.yml - Scheduled weekly (cron 0 0 * * 0) or dispatch: runs Python blog_bot.py (uses Groq API key secret) to generate new blog posts under posts/*.md, then builds the site with Node 18 and validates filenames before committing/pushing changes back to the repo.
4. social_bot.yml - Runs every 8 hours: first job builds the site and waits ~30s for Netlify deployment; second job (depends on the first) runs social_bot.py using secrets GROQ_API_KEY, META_ACCESS_TOKEN, FB_PAGE_ID, IG_USER_ID, GITHUB_TOKEN to post content to Facebook/Instagram.

Hosting configuration
- netlify.toml declares publish = "_site" and command = "DEBUG=* eleventy", so Netlify runs the same Eleventy build and deploys the _site folder.

Conventions developers should follow
- Use npm run build / npm run serve for local development; do not rely on Makefiles or Docker — the project has none.
- Keep template files under _includes and pages/markdown at the repo root or in posts/ / shop/; Eleventy treats these as collections based on front matter tags.
- Tag names must be slug-compatible because safeSlug normalizes them to [a-z0-9-]; avoid apostrophes, ampersands, or non-ASCII characters in tags.
- All images live under img/ and are passthrough-copied; reference them relative to the output path.
- When adding new Markdown content, ensure filenames are valid on Netlify's filesystem (the check-filenames.js script enforces this).
- Secrets required by automation (GROQ_API_KEY, META_ACCESS_TOKEN, FB_PAGE_ID, IG_USER_ID, GITHUB_TOKEN) must be set in GitHub repository settings for the bot workflows to succeed.
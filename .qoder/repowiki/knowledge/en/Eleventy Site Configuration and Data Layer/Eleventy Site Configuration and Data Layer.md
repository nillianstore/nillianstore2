---
kind: configuration_system
name: Eleventy Site Configuration and Data Layer
category: configuration_system
scope:
    - '**'
source_files:
    - .eleventy.js
    - package.json
    - netlify.toml
    - _data/metadata.json
    - _data/home.json
    - _data/premier.json
    - _data/premium.json
    - _data/template.json
    - _data/widget.json
---

This Eleventy site uses a flat, file-driven configuration model with no external config loader or environment-variable system. All runtime configuration is centralized in two places: the Eleventy JavaScript config and JSON data files under `_data/`.

**Build & framework configuration**
- `.eleventy.js` — the single source of truth for Eleventy behavior: plugin registration (`@11ty/eleventy-plugin-rss`, `syntaxhighlight`, `navigation`), global data (`site.url`), layout aliases (`post`, `shop`), custom Nunjucks filters (`readableDate`, `htmlDateString`, `isoDateTime`, `safeSlug`, `filterTagList`, `sanitize`, `xmlEncode`), passthrough copy rules, Markdown-it setup (with anchor permalinks), Browsersync middleware, and directory layout (`input: .`, `includes: _includes`, `data: _data`, `output: _site`). Deep merge of data is enabled via `setDataDeepMerge(true)`.
- `package.json` — npm scripts (`build`, `watch`, `serve`, `debug`) wrap the `eleventy` CLI; dev dependencies pin Eleventy v2 canary and supporting plugins.
- `netlify.toml` — deployment config declaring `_site` as publish dir and `DEBUG=* eleventy` as the build command.

**Site content configuration (JSON data layer)**
- `_data/metadata.json` — global site metadata (title, description, canonical URL, language/locale, feed paths, author). This is the primary place to change the site identity and feed URLs.
- `_data/home.json` — homepage hero/banner text and image references consumed by home layouts.
- `_data/premier.json` / `_data/premium.json` — arrays of template showcase entries (cover, title, description, url, link) rendered by theme pages.
- `_data/template.json` — catalog of other Eleventy templates offered by the project.
- `_data/widget.json` — reusable footer/help widget strings.

All `_data/*.json` files are automatically merged into the Eleventy data cascade and available globally in Nunjucks templates via `metadata.*`, `home.*`, `premier`, `premium`, `template`, `widget`.

**Environment variables and secrets**
There is no `.env` file, no `dotenv` usage, and no `process.env` reads anywhere in the codebase. The only "secret" present is an email address inside `_data/metadata.json`. Build-time overrides are not supported; the site URL is hard-coded both in `metadata.json` and in `.eleventy.js` (`site.url`).

**Conventions developers should follow**
- Change site-wide identity (title, description, canonical URL, feeds, author) exclusively in `_data/metadata.json`; do not duplicate it in templates.
- Keep per-page or per-section text that varies across builds in `_data/*.json` rather than scattering it across templates.
- New Eleventy features (filters, collections, passthrough copies, layout aliases) belong in `.eleventy.js`, not in individual templates.
- Do not introduce environment variables without adding corresponding loading logic to `.eleventy.js` and documenting them in this card.
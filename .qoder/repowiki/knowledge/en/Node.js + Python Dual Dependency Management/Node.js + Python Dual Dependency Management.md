---
kind: dependency_management
name: Node.js + Python Dual Dependency Management
category: dependency_management
scope:
    - '**'
source_files:
    - package.json
    - .nvmrc
    - .github/workflows/blog_bot.yml
    - .github/workflows/social_bot.yml
    - .github/workflows/build-check.yml
---

This Eleventy static site uses a dual-language dependency strategy managed through two separate ecosystems, with no lockfiles committed to the repository.

**Node.js dependencies (Eleventy build toolchain)**
- Declared exclusively in `package.json` under `devDependencies`: `@11ty/eleventy`, `@11ty/eleventy-navigation`, `@11ty/eleventy-plugin-rss`, `@11ty/eleventy-plugin-syntaxhighlight`, plus runtime helpers `luxon`, `markdown-it`, and `markdown-it-anchor`. No production (`dependencies`) are declared — everything is treated as a dev/build-time concern.
- Node version is pinned via `.nvmrc` to major version `16`, but GitHub Actions workflows install Node `18` for CI builds. There is no `package-lock.json` or `pnpm-lock.yaml`; `.gitignore` explicitly excludes both `node_modules/` and `package-lock.json`, so installs are non-deterministic across environments.
- Build scripts expose `build`, `watch`, `serve`, `start`, `debug`, and `check:filenames` (a custom filename validator). The project has no vendoring of Node packages.

**Python dependencies (automation bots)**
- Two automation scripts — `blog_bot.py` (Groq-powered blog post generator) and `social_bot.py` (Instagram/Facebook publisher) — declare their requirements inline via `pip install python-frontmatter requests` inside the GitHub Actions jobs (`blog_bot.yml`, `social_bot.yml`). There is no `requirements.txt`, `pyproject.toml`, or `Pipfile` at the repo root; Python dependencies are not pinned anywhere outside the workflow YAML.
- Workflows run on Python `3.11` via `actions/setup-python@v5`.

**CI-driven installation patterns**
- `build-check.yml` runs `npm install` then `npx @11ty/eleventy` to validate the build.
- `blog_bot.yml` installs Python deps with `pip install python-frontmatter requests`, runs the bot, then sets up Node 18, runs `npm ci` (note: this expects a lockfile that is not tracked), builds, and validates filenames before committing new posts.
- `social_bot.yml` mirrors the same pattern: install Node deps, build the site, wait for Netlify deployment, then install Python deps and run the social bot.

**Conventions & gaps**
- No private registries, proxy config, or scoped package configuration exists.
- Lockfiles are intentionally ignored, which means reproducible installs rely on caret ranges (`^x.y.z`) in `package.json` and unpinned pip installs in CI — a potential source of drift between local and CI environments.
- The Node version mismatch between `.nvmrc` (16) and CI (`18`) should be reconciled.
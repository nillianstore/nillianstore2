---
kind: error_handling
name: Ad-hoc print-based error handling in automation scripts
category: error_handling
scope:
    - '**'
source_files:
    - blog_bot.py
    - social_bot.py
    - scripts/check-filenames.js
    - _includes/layouts/base.njk
---

This Eleventy static site has no centralized error-handling framework. Error management is limited to the two Python automation scripts and one Node helper, each using a simple print-and-exit pattern with broad `except Exception` catches.

**Python automation scripts**
- `blog_bot.py`: Catches all exceptions around the blog-generation pipeline (`frontmatter.load`, Groq API call, file write) and prints `Error: {e}` before exiting. Missing config (`GROQ_API_KEY`) is detected early and printed as a message; the process returns without an explicit exit code.
- `social_bot.py`: Uses per-call try/except blocks for Git operations (`subprocess.CalledProcessError`), HTTP calls (`requests.exceptions.RequestException`), and a final catch-all `Exception`. Network errors are logged with status codes and response bodies, including special-case detection of Meta token expiry (error code 190). The script exits with `sys.exit(1)` when required secrets are missing or after three failed posting attempts. A retry loop over `main()` isolates failures by product id.
- Both scripts persist partial state to JSON log files (`blog_log.json`, `social_log.json`) and fall back gracefully when those logs are malformed or missing.

**Node helper**
- `scripts/check-filenames.js`: Uses async I/O with try/catch, prints via `console.error`, and uses distinct `process.exit` codes (0 success, 1 forbidden filenames found, 2 build not run) to signal different failure modes.

**Nunjucks templates**
- No server-side error handling exists; the only client-side error path is a `.catch(err => console.error(...))` on a fetch of `/products.json` in `_includes/layouts/base.njk`.

There are no custom exception classes, sentinel errors, middleware, panic/recover equivalents, or structured logging — just inline `print`/`console.error` statements and `sys.exit` / `process.exit` codes.
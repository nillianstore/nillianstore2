---
kind: logging_system
name: Ad-hoc print + JSON-file logging for automation bots
category: logging_system
scope:
    - '**'
source_files:
    - blog_bot.py
    - social_bot.py
    - blog_log.json
    - social_log.json
---

This repository does not implement a centralized logging system. There is no shared logger module, no log-level configuration, and no structured logging framework in use across the codebase.

What exists instead is an ad-hoc pattern used by two Python automation scripts:
- `blog_bot.py` writes a running list of processed product IDs to `blog_log.json` via simple `json.dump` calls and prints status messages with bare `print()`.
- `social_bot.py` maintains `social_log.json` (capped at 50 entries) and similarly uses `print()` for human-readable progress, error details, and API diagnostics; it also commits `social_log.json` back to GitHub so the history persists in version control.

Key characteristics:
- No Python `logging` module import or usage anywhere in the repo.
- No log rotation, level filtering, or sink abstraction — each script owns its own JSON file.
- Human-readable output goes only to stdout via `print()`, making it suitable for CI console logs but not parseable as structured events.
- The JSON files (`blog_log.json`, `social_log.json`) act as both persistence and de-duplication history rather than true audit logs — they contain only product IDs, not timestamps, severity, or contextual fields.
- Error paths still rely on `print()` and occasional `traceback.print_exc()` inside `social_bot.py`; there is no exception-to-log pipeline.

Because this is primarily an Eleventy static-site project, the Node/Nunjucks build layer has no logging concerns either — all runtime output comes from the two Python bots invoked by CI workflows.
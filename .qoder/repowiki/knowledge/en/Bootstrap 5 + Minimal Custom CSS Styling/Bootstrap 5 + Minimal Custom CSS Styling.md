---
kind: frontend_style
name: Bootstrap 5 + Minimal Custom CSS Styling
category: frontend_style
scope:
    - '**'
source_files:
    - css/bs.css
    - css/index.css
    - _includes/widget/head.njk
    - .eleventy.js
---

The site uses a straightforward, utility-first styling approach built on top of Bootstrap 5.2.2 with minimal custom overrides.

**System and packages**
- **Bootstrap 5.2.2** is vendored as `css/bs.css` (full compiled distribution) and loaded via `<link rel="preload">` in `_includes/widget/head.njk`, with a noscript fallback.
- **Custom styles** live in `css/index.css` — a small file (~50 lines) that adds only what Bootstrap doesn't cover: link defaults, tag sizing, image constraints for blog posts, and CTA video responsive rules.
- **Font Awesome 6.5.0** icons are pulled from the Cloudflare CDN and preloaded similarly to the local CSS files.
- **Swiper 11** carousel CSS/JS is loaded lazily from jsDelivr; CSS is preloaded and JS is appended after DOMContentLoaded when a `.swiper` element exists.
- No SCSS/Sass, Tailwind, CSS-in-JS, or build-time CSS pipeline is used — all CSS ships as static files copied verbatim by Eleventy (`addPassthroughCopy('css')`).

**Architecture and conventions**
- Layouts compose through Nunjucks includes: `base.njk` → `widget/head.njk` → `widget/navbar.njk` / `widget/content.njk` / `widget/footer.njk`. All global stylesheet links are centralized in `head.njk`.
- The design system is essentially Bootstrap's default token set (colors, spacing, breakpoints, grid, utilities like `d-none`, `text-muted`, `p-2`, etc.) plus two custom class families:
  - Semantic page classes such as `.tag`, `.black`, `.cta-video-wrapper`, `.cta-video`.
  - Inline `<style>` blocks inside `head.njk` for hero-image layout (positioned container with 16:9 aspect ratio).
- Responsive strategy follows Bootstrap's mobile-first breakpoints (`col-md-*`, `@media (min-width: 768px)`, etc.). There is no custom breakpoint system or CSS variables beyond Bootstrap's own `--bs-*` tokens.
- Theme variants (`free.njk`, `pro.njk`, `premier.njk`) under `_includes/desain/themes/` reuse the same CSS stack; they differ in content/layout, not in separate style sheets.

**Rules developers should follow**
- Add new global styles to `css/index.css`; avoid inline `<style>` except for one-off page-specific tweaks already present in `head.njk`.
- Prefer Bootstrap utility classes (`d-flex`, `text-center`, `mb-3`, `img-fluid`, `container`, `row`/`col-*`) over writing custom CSS.
- Do not edit `css/bs.css` directly — it is the unmodified Bootstrap distribution; override via `index.css` or component-level classes.
- Keep third-party assets (Font Awesome, Swiper) referenced from their CDNs as in `head.njk`; do not vendor them locally unless required.
- When adding new CSS, mirror the preload/noscript pattern used for existing stylesheets so non-JS clients still receive the styles.
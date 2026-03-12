---
name: "Frontend"
description: "Conventions for the vanilla JS/CSS/HTML weather dashboard"
applyTo: "src/weather_app/static/**"
---

# Frontend Conventions

## Stack

- **Vanilla JavaScript** — no frameworks, no build step, no bundler.
- **Chart.js 4.x** loaded via CDN for forecast visualization.
- **CSS custom properties** for theming; no preprocessors (no Sass/Less).
- All frontend files live in `src/weather_app/static/` and are served by
  FastAPI's `StaticFiles` mount.

## JavaScript (`app.js`)

### Structure

The file is organized in clearly separated sections using comment banners:

```javascript
// ---------------------------------------------------------------------------
// Section Name
// ---------------------------------------------------------------------------
```

Maintain this structure when adding code.  Sections: State, DOM references,
API helpers, rendering functions, event handlers, initialization.

### API Communication

- Use the `fetch` API via the existing `apiGet`, `apiPost`, `apiDelete`
  helpers.  Never use `XMLHttpRequest` or add `axios`.
- All API calls go to `/api/...` endpoints served by the FastAPI backend.
- Handle errors by catching and displaying them in `#search-error`.

### Style Rules

- Use `const` by default, `let` only when reassignment is needed.  Never `var`.
- Use `async`/`await` for asynchronous code — no `.then()` chains.
- Template literals for string interpolation.
- JSDoc comments (`/** ... */`) on all top-level functions.
- DOM lookups are cached at module level — don't re-query the DOM in loops.
- Use descriptive `id` and `class` names matching the HTML structure.

### No External Dependencies

Do not add npm packages, bundlers, or frameworks.  The only external script
is Chart.js via CDN.  If new visualization is needed, extend Chart.js usage
or use vanilla DOM manipulation.

## CSS (`style.css`)

### Custom Properties

All colors, sizing, and shadows are defined as CSS custom properties on `:root`:

```css
:root {
    --color-bg: #f4f6f9;
    --color-primary: #3b82f6;
    --radius: 8px;
    --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

When adding new styles, **always** use existing custom properties or define new
ones on `:root`.  Never hard-code color or shadow values in individual rules.

### Conventions

- Use the existing section-comment banner style (`/* ==== Section ==== */`).
- Mobile-first responsive approach — base styles for small screens, media
  queries for larger breakpoints.
- `box-sizing: border-box` is set globally — do not override.
- System font stack on `body` — do not import web fonts.
- Use semantic class names matching component purpose (`.weather-card`,
  `.search-bar`, `.sidebar`).

## HTML (`index.html`)

- Semantic elements: `<header>`, `<main>`, `<section>`, `<footer>`.
- All interactive elements have an `id` used by `app.js` for DOM lookups.
- External scripts load from CDN with full version pins.
- No inline styles or inline `<script>` blocks — keep JS in `app.js` and
  CSS in `style.css`.
- `lang="en"` on `<html>`, `charset="UTF-8"`, viewport meta tag present.

## Accessibility

- All `<input>` and `<select>` elements have `placeholder` or associated
  `<label>` elements.
- Buttons have descriptive `title` attributes where icons replace text.
- Use sufficient color contrast — the existing palette meets WCAG AA.

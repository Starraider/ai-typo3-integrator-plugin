# TYPO3 Container (b13/container) — Design Rules, API, And Troubleshooting

Background and decision guidance for the snippets in
[container-patterns.md](container-patterns.md). Identifiers (`tx_acme_*`,
`acme_container_*`, `site_package`) are examples. Confirm every API against the
installed `b13/container` and TYPO3 versions.

## 1. Design Rules

- Place container registrations in the **site package or theme extension**,
  never in `typo3conf/`.
- Every container is its own **CType** with a stable vendor-prefixed
  snake_case identifier such as `acme_container_two_columns`.
- Child columns use **project-specific `colPos` integers** that do not collide
  with core values (`0`–`3`). Start at `200` and increment per column.
- Keep **one place per container**: one registration entry, one TypoScript
  block, one Fluid template, one icon.
- Expose styling options as **TCA fields, not FlexForms** — this matches how
  `b13/container` is designed and keeps values queryable.
- Ship styling **options**, not cosmetic hard-coding. Editors choose values;
  CSS utility classes render them. Actual spacing sizes live in CSS, not TCA,
  so theming can evolve without schema changes.
- Keep `space_before` / `space_after` item sets identical so editors see one
  vertical-spacing vocabulary.
- Use `onChange => 'reload'` only when a value changes `showitem` visibility —
  not for purely cosmetic options.
- Keep the **mobile stacking breakpoint global** (see section 3).

## 2. CSS Framework Detection

Detect the framework before writing Fluid, then emit only that framework's
built-in utilities. Do not introduce custom `container--*` BEM classes and do
not mix frameworks in one template. Record the decision (e.g. "Framework
detected: Bootstrap 5.3"). First positive match wins:

1. `package.json` dependencies: `bootstrap` (or `bootstrap-icons`,
   `@popperjs/core`) → Bootstrap; `tailwindcss` (or `@tailwindcss/*`) →
   Tailwind.
2. SCSS/CSS entry points: `@import "bootstrap/..."` / `@use "bootstrap"` →
   Bootstrap; `@import "tailwindcss"` (v4) or `@tailwind base;` (v3) →
   Tailwind.
3. Built CSS: `.col-6`, `.d-flex`, `.bg-primary` → Bootstrap; utility atoms
   like `.max-w-screen-lg`, `.grid-cols-3` → Tailwind.
4. `tailwind.config.*`, `postcss.config.*`, or `vite.config.*` configuring
   Tailwind → Tailwind.
5. Nothing matches → ask the user. Do not invent classes.

```bash
grep -E '"(bootstrap|tailwindcss)"' package.json
grep -RE '@tailwind |@import ["\x27](tailwindcss|bootstrap)' packages/*/Resources/Private/ 2>/dev/null
ls tailwind.config.* postcss.config.* 2>/dev/null
```

The TCA fields stay identical across frameworks; only the value → class maps
in `Partials/Container/Utilities.html` change. If the project defines theme
tokens (e.g. `bg-primary` in a Tailwind `@theme` or config), swap the default
palette classes for those tokens; never use names the project does not define.

### Making Tailwind see runtime classes

Tailwind only generates classes it finds in scanned sources. The maps contain
literal class strings, but `{bp}:grid` and `col-{bp}-6`-style strings are
assembled at runtime and are invisible to the scanner. Either replace `{bp}`
with the literal resolved token in the maps, or safelist every emitted
breakpoint variant:

```css
/* Tailwind v4.1+: in the CSS entry point */
@source inline("md:grid md:grid-cols-2 md:grid-cols-3 flex-col flex-col-reverse");
```

```js
// Tailwind v3: tailwind.config.js
module.exports = { safelist: ['md:grid', 'md:grid-cols-2', 'md:grid-cols-3', 'flex-col', 'flex-col-reverse'] };
```

Also make sure the Fluid templates and partials are covered by `@source` (v4)
or `content` (v3). Bootstrap needs no safelist, but its compiled bundle must
actually ship the utilities used (`container-xl`, `bg-body-secondary`, …).

## 3. Stacking Semantics

The breakpoint is **not** configurable per container: one project-wide value
(preferably the existing navigation/hamburger breakpoint, see
[container-patterns.md](container-patterns.md) section 5) is bound once in
`Partials/Container/Utilities.html` as `{bp}`. Container templates never
hardcode `md`/`lg` and never rebind `{bp}`. If the existing key holds a pixel
value (e.g. `992px`) instead of a token, map it to a token or fall back to
`container.stackBreakpoint` and document the mismatch. Without site settings,
use a single `<f:variable name="bp" value="md" />` in the partial.

`tx_acme_stack_order` offers two values, shared by all container CTypes:

| Container | `default` | `reverse` |
|-----------|-----------|-----------|
| Two col   | 1, 2      | 2, 1      |
| Three col | 1, 2, 3   | 3, 2, 1   |

- **Bootstrap 5:** keep `.row`, add `flex-column` / `flex-column-reverse` plus
  `flex-{bp}-row`; `col-{bp}-6` / `col-{bp}-4` decide the desktop layout.
- **Tailwind:** `flex flex-col` / `flex flex-col-reverse` below the
  breakpoint, `{bp}:grid {bp}:grid-cols-2` (or `-3`) at and above it.

DOM order stays unchanged; CSS alone decides the visual order. A container that
truly needs a different breakpoint is a separate CType, not a TCA option.

`{mapName.{data.field}}` is Fluid dynamic object access: `{bgMap.{data.tx_acme_bgcolor}}`
resolves to `{bgMap.light}`. Missing keys resolve to empty, hence the explicit
`none: ''` / `default` entries. `{data.*}` comes from the `tt_content` row that
`lib.contentElement` already exposes.

## 4. ContainerConfiguration API

Common methods (verify against the installed version):

- `setIcon(string)` — SVG path (`EXT:…`) or registered icon identifier.
- `setBackendTemplate(string)` — Page-module preview template.
- `setGridTemplate(string)` — inner backend grid template (rarely needed).
- `setGridPartialPaths(array)` / `addGridPartialPath(string)`,
  `setGridLayoutPaths(array)` — backend grid template roots.
- `setSaveAndCloseInNewContentElementWizard(bool)` — default `true`; set
  `false` so editors land in the edit form and pick styling options first.
- `setRegisterInNewContentElementWizard(bool)` — `false` hides the wizard
  entry.
- `setGroup(string)` — wizard tab and CType optgroup; keep `container` unless
  the project has its own group.
- `setRelativeToField(string)` / `setRelativePosition('before'|'after'|'replace')`
  — position relative to an existing field.
- `setDefaultValues(array)` — defaults applied to new records.

`Registry::configureContainer()` adds the CType select item, registers the
icon, writes the wizard Page TSconfig, sets a default `showitem` containing
`header`, and stores the grid in
`$GLOBALS['TCA']['tt_content']['containerConfiguration'][<CType>]`. Add style
fields via a palette and `addToAllTCAtypes()`; do not overwrite that
`showitem`.

## 5. ContainerProcessor Options

- `contentId` — container uid; defaults to the current record. Override only
  for a foreign container.
- `colPos` — restrict to one column. Without it, every column is exposed as
  `children_<colPos>`.
- `as` — variable name; honoured only together with `colPos`.
- `skipRenderingChildContent` — skip child rendering (`renderedContent` stays
  empty); only for lists that render their own child representation.

The shortest form is a bare `10 = B13\Container\DataProcessing\ContainerProcessor`.

## 6. Backend Preview And PSR-14 Events

The default preview is usually enough. Override with `setBackendTemplate()`
only to show styling context that matters to editors (e.g. selected background
as a coloured border); never re-render frontend content in the backend.

- `BeforeContainerConfigurationIsAppliedEvent` — adjust configuration of
  third-party containers or apply a shared `gridTemplate`; column properties
  can change, CType and grid structure cannot.
- `BeforeContainerPreviewIsRendered` — change the preview view, add variables,
  or swap template paths.

Use events only for changes across multiple containers or containers owned by
another extension; configure project-local containers directly.

## 7. Restricting Child Content Types Per Column

Check the installed versions first. TYPO3 v14.1+ supports per-column
`allowedContentTypes` / `disallowedContentTypes` (comma-separated CTypes) in
Page TSconfig backend layouts, and recent `b13/container` versions pass these
keys through from the grid configuration:

```php
['name' => 'Left',  'colPos' => 200, 'allowedContentTypes'    => 'text,textmedia,header,acme_cta'],
['name' => 'Right', 'colPos' => 201, 'disallowedContentTypes' => 'header'],
```

- The legacy `content_defender` form `'allowed' => ['CType' => '…']` /
  `'disallowed' => ['CType' => '…']` is still accepted and mapped; if both
  forms are present, `allowedContentTypes` wins.
- Restrictions apply in the wizard, CType/colPos selects, and move/copy.
- `maxitems` still requires EXT:content_defender; both can coexist. Without a
  `maxitems` need, `content_defender` can be dropped when moving to v14.
- Database-record backend layouts (`backend_layout` table) may not support
  the keys yet; Registry-based containers use the Page TSconfig path.
- `ManipulateBackendLayoutColPosConfigurationForPageEvent` is `@internal` in
  v14 — acceptable for tested site-local listeners only.

On older TYPO3 versions use `content_defender` and its `allowed`/`disallowed`
syntax.

## 8. Troubleshooting

- **Container missing in the New Content Element wizard** — confirm the CType
  registration, flush caches (`cache:flush -g system,pages`), check backend
  group permissions for the CType, and look for Page TSconfig that resets
  `mod.wizards.newContentElement.wizardItems.container`.
- **Child column shows as "Normal"/"Unused"** — grid `colPos` and
  `ContainerProcessor` `colPos` differ. Align the integers.
- **Backend grid or new fields empty** — flush the system cache and run the
  database analyzer (`extension:setup` or Install Tool → Analyze Database
  Structure).
- **Styling options not applied** — check `ext_tables.sql`, the `showitem`
  palette for that CType, that Fluid reads `{data.tx_acme_*}`, Tailwind
  source/safelist coverage (section 2), or that Bootstrap's build ships the
  utility.
- **Children do not render** — TypoScript block missing or `templateName`
  does not match the case-sensitive filename.
- **Translations disappear** — mixed translation mode is unsupported; use
  connected or free mode consistently.
- **Stacking order does not switch** — find which settings path `{bp}` is bound
  to in `Utilities.html`, confirm it is set in the active site settings, and
  that the value is a valid token (Bootstrap `sm…xxl`, Tailwind `sm…2xl`). An
  empty `{bp}` emits invalid classes such as `flex--row` or `:grid`. Column
  width classes must use the same `{bp}`.
- **One container flips at the wrong breakpoint** — do not add a
  per-container breakpoint; change the global value or create a separate CType.

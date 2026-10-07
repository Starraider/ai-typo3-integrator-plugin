# News Extension Workflow Details

Detailed guidance for each workflow step in `SKILL.md`. Paths such as
`packages/my-site-package/` and constant names such as
`{$mysitepackage.pages.newsStorage}` are examples; use the target project's
own site package and constants. Commands assume DDEV; translate them to the
repository's command wrapper when it differs.

## Baseline Inspection

Before making assumptions about templates, partials, plugin names, or
controller actions, inspect:

- `composer.json` for the installed `georgringer/news` constraint
- `vendor/georgringer/news/` for the actual package structure
- the site package set's `config.yaml` — it should declare a dependency on
  `georgringer/news`
- the site package's `TypoScript/plugin.typoscript` (or equivalent)
- existing overrides in `Resources/Private/Templates/News/` and
  `Resources/Private/Partials/News/`

If the official docs and vendor files differ, follow the vendor package for
implementation details and keep the output conceptually aligned with the docs.

## Installation And Maintenance

Install with Composer (only with authorization):

```bash
composer require georgringer/news
```

Then ensure the site set or template includes the News configuration. Use
`ddev typo3` for TYPO3 CLI commands, never the legacy `ddev typo3cms`. When
structural changes are involved, the usual maintenance sequence is:

```bash
ddev typo3 cache:flush
ddev typo3 database:updateschema
ddev typo3 referenceindex:update
ddev typo3 cache:warmup
```

## Configuration Placement

The site package is the override boundary. News configuration belongs in:

- `Configuration/Sets/<Set>/TypoScript/plugin.typoscript`
- `Configuration/Sets/<Set>/settings.definitions.yaml` for page-ID and option
  settings
- `Resources/Private/Templates/News/`
- `Resources/Private/Partials/News/`
- `Resources/Private/Layouts/` only when a News layout override is truly
  needed

Do not place News Fluid overrides inside `vendor/`, and do not create a custom
extension just to skin News.

## Core Settings

The base `plugin.tx_news` block in
[plugin-reference.md](plugin-reference.md) sets view paths and defaults. Use
the settings intentionally:

- `startingpoint` — storage PID for news records
- `detailPid` — target page for detail links
- `listPid` — target page for list pages when a plugin needs it
- `searchResultPid` — target page for search results
- `limit` — default number of records per page

Prefer Site Set constants for page IDs and editor-managed assets, for example
`{$mysitepackage.pages.newsStorage}`, `{$mysitepackage.pages.newsDetail}`,
`{$mysitepackage.pages.searchResultPid}`, `{$mysitepackage.news.feed.*}` for
RSS, and `{$mysitepackage.news.heroBackgroundImage}`.

## Plugin Variants

Clone the base plugin settings with TypoScript inheritance (see
[plugin-reference.md](plugin-reference.md)) for cases such as:

- sticky sidebar list
- lead-story offset list
- hero search form
- featured or curated list
- RSS-specific format switches

Do not create custom News controllers just to alter demand settings, do not
introduce custom News domain models, and stay on the native `{newsItem}` object
provided by `NewsController`.

## Related And Trending Content

Use `{newsItem.relatedSorted}` for related news (pattern in
[template-patterns.md](template-patterns.md)). For trending or editorial
sidebars, prefer a second native News plugin instance or a TypoScript-cloned
plugin variant, pass only the minimum settings needed, and keep the detail
template free of custom persistence logic. Never query the database from Fluid
or bypass Extbase with ad-hoc SQL for standard News rendering.

## Media

Keep News media in FAL and render it with `f:image` / `f:uri.image` so
processing, cropping, responsive output, and WebP generation keep working. Do
not hardcode processed file URLs or raw `/fileadmin/...` paths.

## Search Routing

- Set `searchResultPid` centrally in TypoScript.
- Customize SearchForm visuals through a template override plus cloned plugin
  settings.
- Keep a custom search form compatible with the plugin's expected request
  argument names and target page.

## Styling, Build, And Cache

When News templates gain or change utility classes (for example with a
Tailwind v4 pipeline):

```bash
ddev exec "cd packages/my-site-package && npm run build"
ddev typo3 cache:flush
```

- Utility classes in Fluid are not visible until the CSS build runs.
- TYPO3 may serve stale markup or assets until caches are flushed.
- The CSS entry point's `@source` coverage must include the News templates and
  partials.
- Do not verify visual changes before rebuilding CSS and flushing caches.

Preserve semantic `<h1>`/`<h2>` elements; if global typography conflicts with a
News design, override on the semantic element (Tailwind `!` modifier) instead of
downgrading it to a `<div>`.

## Visual Regression Testing

When the project has a Playwright workflow, cover visual changes to News List,
Detail, SearchForm, SelectedList, or shared partials with a VRT check (for
example tagged `@stitch-vrt`). Run Playwright inside DDEV, after building CSS
and flushing caches:

```bash
ddev exec "cd packages/my-site-package && npx playwright test Tests/e2e/news.spec.ts --grep @stitch-vrt"
```

Plugin page URLs are editor-managed, so read them from environment variables
such as `NEWS_LIST_TEST_URL`, `NEWS_DETAIL_TEST_URL`, and
`NEWS_SEARCH_TEST_URL`. Do not hardcode guessed URLs; ask the user for the
actual pages. If the project keeps authoritative design references (for
example under `docs/designs/`), compare changed templates against them before
calling the work done.

## Common Mistakes

- Overriding News templates in `vendor/`
- Creating custom News domain models or bypassing `NewsController` for simple
  rendering changes
- Removing `<n:excludeDisplayedNews>`, `<n:titleTag>`, or the OpenGraph partial
  from `Detail.html`
- Rendering News media with raw file paths
- Forgetting the CSS build and TYPO3 cache flush after template class changes
- Running Playwright on the host instead of inside DDEV
- Inventing News plugin page URLs instead of asking or using environment
  variables

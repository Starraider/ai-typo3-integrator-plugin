---
name: typo3-news-extension
description: Install, configure, review, or customize the TYPO3 News Extension (georgringer/news). Use for News site-set or TypoScript setup, choosing native News plugins, site-package template and partial overrides, detail-page SEO ViewHelpers, FAL media rendering, search routing, or frontend verification; do not use it for unrelated custom Extbase domains.
license: CC-BY-4.0
compatibility: Requires a TYPO3 project with georgringer/news; Composer, DDEV, CSS-build, and browser-test commands must follow the target repository.
---

# TYPO3 News Extension

Use the installed `georgringer/news` package as the implementation source of
truth and its official documentation as the conceptual reference. Keep project
configuration, templates, and assets in the owning site package.

## Workflow

1. **Establish the installed baseline.** Read repository instructions; inspect
   `composer.json`, the installed News package, existing site sets/TypoScript,
   templates, routes, and the project build/test commands. Determine whether
   the request is installation, configuration, a native-plugin choice, template
   rendering, or a bug review.
   **Complete when:** version-specific names and the owning override boundary
   are confirmed from the local project.
2. **Plan changes at the right layer.** Use Composer and site-set changes only
   with authorization. Put shared `plugin.tx_news` defaults and view paths in
   the site package. Choose a native News plugin or TypoScript variant before
   creating custom PHP; do not add a custom domain model or query data from
   Fluid for ordinary presentation changes.
   **Complete when:** every requested behavior maps to the smallest supported
   extension point.
3. **Implement site-package overrides.** Extract repeated presentation into
   News partials, use TYPO3 FAL image ViewHelpers, and preserve the installed
   News detail template's SEO and header ViewHelpers. Keep native search form
   and result routing compatible with the extension’s expected parameters.
   **Complete when:** templates retain required extension behavior while their
   visual structure is owned only by the site package.
4. **Build and verify.** Use the repository's asset pipeline if classes or
   templates change, clear relevant TYPO3 caches, and verify list, detail,
   search, and any changed plugin page at known URLs. Add or run browser tests
   when a project workflow exists; request test URLs rather than guessing them.
   **Complete when:** rendered content, images, title/meta behavior, routing,
   and responsive presentation pass the applicable checks.

## Safety

Do not edit `vendor/`, change production News records, install packages, run
database updates, or execute external browser tests without user authorization.
Treat page IDs, routes, image references, and rendered template names as
project-specific evidence, not universal defaults.

## References

- [references/plugin-reference.md](references/plugin-reference.md) — native
  plugins, TypoScript defaults, and variant patterns.
- [references/template-patterns.md](references/template-patterns.md) —
  site-package overrides, SEO ViewHelpers, FAL images, and partial patterns.

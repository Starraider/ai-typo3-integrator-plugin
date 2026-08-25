---
name: typo3-playwright-workflow
description: Verify TYPO3 frontend changes with Playwright inside DDEV. Use after changing Fluid templates, CSS, JavaScript, or UI components to run targeted smoke and visual-regression tests, capture diagnostics, or investigate visual diffs on known mounted URLs. Use typo3-playwright-ddev when the Playwright environment itself is missing or broken.
license: CC-BY-4.0
compatibility: Requires a working Playwright setup in a TYPO3 DDEV project, the site-package command path, and the real mounted URL for editor-managed content or plugins.
---

# TYPO3 Playwright Verification in DDEV

Use this repeatable execution loop after frontend implementation. It verifies the rendered TYPO3 result; it does not install or repair Playwright infrastructure.

## 1. Establish the verification target

Inspect the changed frontend files, the relevant existing tests, the site-package directory, and the configured Playwright projects. Identify the expected page URL and the smallest test that covers the changed area.

- For editor-mounted content elements or plugins, require the real mounted URL. Do not guess route paths, `cHash` values, or plugin URLs.
- If the setup, browser runtime, or configuration is absent or failing before tests start, switch to `typo3-playwright-ddev`.
- Extend an existing test that already owns the page area instead of creating duplicate coverage.

Completion: the target URL, affected locator or behavior, and test command are known.

## 2. Run the focused verification loop

With authorization to run DDEV commands, build the site package, flush TYPO3 caches when the change needs it, then run the focused Playwright test inside DDEV. Substitute the discovered package directory and spec path:

```bash
ddev exec --dir packages/<theme-name> npm run build
ddev typo3 cache:flush
ddev exec --dir packages/<theme-name> npx playwright test Tests/e2e/<file>.spec.ts --grep @stitch-vrt
```

Building may write compiled assets; cache flushing changes disposable runtime cache; Playwright writes reports and test artifacts. Do not change source tests or snapshot baselines unless the user has authorized those file changes.

For new or materially changed UI, cover the smallest useful set:

- a smoke assertion that the expected content renders on the intended URL;
- a locator-based visual assertion for the affected section or element;
- an alternate viewport or mobile check when the layout changes across breakpoints.

Use stable IDs or other durable locators, assert visibility before a screenshot, and use the committed approved baseline. See [VRT patterns and diagnostics](references/vrt-patterns.md).

Completion: the selected test ran against the intended URL and its result is recorded.

## 3. Diagnose failures from artifacts

Review evidence in this order:

1. Expected, actual, and diff screenshots.
2. The Playwright HTML report.
3. The trace file.
4. Captured response HTML or an in-container request that preserves the public host context.

First rule out an incorrect mounted URL, 404/fallback page, stale build, or TYPO3 host resolution mismatch. Do not rely on internal container hostnames such as `https://web/...` when they select a different TYPO3 site.

Completion: the failure is categorized with an artifact or command result, not inferred from a test name alone.

## 4. Handle baselines deliberately

Use `--update-snapshots` only for an intentional, reviewed visual change and only after the user authorizes snapshot writes. Inspect every changed image, record why it is expected, and rerun the non-update test before reporting success. Never use a snapshot update as a generic failure fix.

Completion: either the approved baseline still passes, or every accepted baseline change is explained and revalidated.

## Agent-environment constraint

When a host-side agent cannot open a DDEV hostname, run Playwright inside DDEV and inspect generated workspace artifacts rather than treating lack of host browser access as a rendering failure.

## Maintainer evaluation

Scenario coverage for this skill is recorded in [evals/evals.json](evals/evals.json). Run the validation commands in the README after editing this skill.

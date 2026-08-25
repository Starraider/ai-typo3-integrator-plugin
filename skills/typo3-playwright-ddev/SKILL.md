---
name: typo3-playwright-ddev
description: Set up, repair, or upgrade Playwright testing infrastructure for a TYPO3 site package running in DDEV. Use when Playwright dependencies, container browsers, configuration, test scripts, artifacts, or initial visual baselines are missing or broken. Use typo3-playwright-workflow instead for routine verification in an already working setup.
license: CC-BY-4.0
compatibility: Requires a TYPO3 project with DDEV, a site package with Node.js/npm available in the DDEV web container, and permission for dependency, DDEV configuration, and test-file changes when setup is needed.
---

# TYPO3 Playwright Setup in DDEV

Create a working, reproducible Playwright environment inside the project's DDEV container. Do not use this skill for normal frontend checks once the setup works; use `typo3-playwright-workflow` then.

## 1. Discover the project before changing it

Establish the DDEV project root, site-package directory, public DDEV URL, package manager and lockfile, existing Playwright configuration, and existing test conventions. Use read-only checks first, such as `ddev status`, `ddev describe`, repository searches, and inspection of `package.json` and test directories.

- Reuse an existing configuration, test directory, package manager, and scripts where they work.
- If the site package or public URL cannot be determined, ask for it; do not invent a package path or test URL.
- If Playwright already runs, diagnose the reported gap instead of reinstalling or overwriting working infrastructure.

Completion: the target package, command path, and specific setup defect or missing capability are known.

## 2. Plan mutations and obtain permission

Explain the smallest required change set before making it. Installation can modify `package.json`, a lockfile, `.ddev/`, Playwright configuration, test sources, generated reports, and snapshot images.

Ask for permission immediately before any of these mutations:

- installing dependencies or the `Lullabot/ddev-playwright` add-on;
- creating or changing configuration, scripts, tests, or helper files;
- generating or updating committed visual baselines.

Running tests writes disposable Playwright artifacts. Never stage, commit, publish, or replace an existing snapshot baseline unless the user explicitly asks.

Completion: the user has authorized the proposed writes, or the task remains read-only with the limitation clearly reported.

## 3. Implement the smallest compatible setup

Work from the site-package directory inside DDEV. Prefer the project's package manager; if none exists, initialize it only with permission. Install `@playwright/test` and `@axe-core/playwright` as development dependencies when absent.

For persistent container browser support, install and restart the DDEV Playwright add-on:

```bash
ddev get Lullabot/ddev-playwright
ddev restart
```

Use the project’s existing wrapper if it works. Otherwise run Playwright inside DDEV, for example:

```bash
ddev exec --dir packages/<theme-name> npx playwright test
```

Create or amend configuration rather than replacing it. The configuration must use the public DDEV URL, tolerate the local HTTPS certificate when required, retain useful failure artifacts, and declare only browser projects the container supports. Start from [the DDEV configuration asset](assets/playwright.config.ts) and load [configuration guidance](references/playwright-config.md) when adapting an existing setup.

Create a test layout only when the project has none. Keep it consistent with `testDir`; use [test patterns](references/test-patterns.md) for a smoke test, locator-based visual test, accessibility test, and browser coverage.

Completion: dependencies, browser runtime, configuration, and command path agree with the actual package layout.

## 4. Verify and establish baselines safely

Run a focused smoke test first, then list or run the suite inside DDEV. Confirm that failures produce inspectable artifacts in the workspace (screenshots, trace, and HTML report where configured). If the environment fails, use [troubleshooting guidance](references/troubleshooting.md) and report the evidence rather than applying broad reinstallations.

Generate initial snapshots only after the tested URLs and viewports are known and the user has authorized baseline writes. Review each captured page before accepting it as the legacy or approved baseline. Do not use `--update-snapshots` merely to make a failing test pass.

Completion: at least one test executes against the intended TYPO3 page, artifacts are available for failures, and any accepted baseline has been reviewed.

## Agent-environment constraint

Do not assume a host-side agent can reach `https://<project>.ddev.site`; it may resolve only inside the local environment. Run tests in DDEV and inspect files written to the workspace. Use the public DDEV hostname—not an internal `https://web/...` hostname—when TYPO3 site resolution or routing must match browser traffic.

## Maintainer evaluation

Scenario coverage for this skill is recorded in [evals/evals.json](evals/evals.json). Run the validation commands in the README after editing this skill.

# TYPO3 Playwright Setup in DDEV

## What this skill solves

It establishes, repairs, or upgrades Playwright infrastructure for a TYPO3 site package that runs in DDEV. It resolves container browser availability, package dependencies, configuration, reusable test structure, diagnostics, and reviewed initial visual baselines without treating routine frontend verification as setup work.

## Use when

- Playwright, its browser runtime, configuration, scripts, or artifacts are missing or broken.
- A TYPO3 DDEV project needs its first smoke, visual-regression, or accessibility test structure.
- An approved legacy baseline must be created after reviewing the real mounted pages.

Use [TYPO3 Playwright Workflow](../typo3-playwright-workflow/README.md) when the test environment already works and a frontend change only needs verification.

## Expected outputs

- A documented site-package command path that runs Playwright inside DDEV.
- A minimally changed configuration using the public DDEV URL and useful failure artifacts.
- At least one successfully executed test plus inspectable reports, traces, or screenshots on failure.
- Reviewed baseline images only when their creation was explicitly authorized.

## Context requirements

- A TYPO3 project with a running DDEV environment.
- The target site-package directory and public DDEV URL, or enough repository context to discover them.
- Node.js/npm (or the project’s chosen package manager) available inside DDEV.
- Permission before dependency installation, DDEV add-on/configuration changes, test-file creation, or baseline writes.

## Installation

This directory is a portable Agent Skill. Install the complete plugin through a compatible Agent Plugin client, or copy/symlink this directory into that client’s Agent Skills discovery path. Codex can use the bundled `agents/openai.yaml` for display metadata; the portable behavior remains in `SKILL.md`.

Keep `SKILL.md`, `README.md`, `assets/`, `references/`, `evals/`, and `agents/` together when installing from source.

## Example prompts

- “Set up Playwright in this TYPO3 DDEV site package and show me the exact files and dependencies you need to change before writing them.”
- “Playwright works on my Mac but not in DDEV; diagnose the container browser setup without overwriting the existing tests.”
- “Create the first reviewed visual-regression baseline for our homepage and content-element showcase in DDEV.”

## Included resources

- [DDEV Playwright configuration asset](assets/playwright.config.ts)
- [Accessibility helper asset](assets/axe-helper.ts)
- [Configuration guidance](references/playwright-config.md)
- [Test patterns](references/test-patterns.md)
- [Troubleshooting guidance](references/troubleshooting.md)

## Validation

From the plugin root, validate the portable structure with the `new-skill` validator and the reference validator when available:

```bash
/path/to/new-skill/scripts/validate-skill.sh skills/typo3-playwright-ddev --strict-portable
skills-ref validate skills/typo3-playwright-ddev
```

Then review the representative, edge-case, and near-miss scenarios in [evals/evals.json](evals/evals.json). A live setup is complete only when a focused test executes inside DDEV and failure artifacts are present.

## Related skills

- [TYPO3 Playwright Workflow](../typo3-playwright-workflow/README.md) for normal post-change verification.
- Use this skill's visual-regression workflow when a CSS change needs baseline-controlled browser verification.

## License

This skill is licensed under [CC BY 4.0](../../LICENSE). Copyright (c) 2026 Sven Kalbhenn.

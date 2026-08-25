# TYPO3 Playwright Workflow

## What this skill solves

It provides the day-to-day verification loop for TYPO3 frontend work in DDEV: selecting the real mounted page, building and testing the smallest relevant scope, reviewing visual evidence, and accepting snapshot changes only when intentional.

## Use when

- Fluid templates, CSS, JavaScript, or a frontend component changed.
- A known TYPO3 page needs a smoke test, visual-regression check, screenshot capture, or visual-diff diagnosis.
- A content element or plugin must be verified at its editor-mounted URL.

Use [TYPO3 Playwright Setup in DDEV](../typo3-playwright-ddev/README.md) if the Playwright environment, browser runtime, or configuration is missing or fails before the test runs.

## Expected outputs

- A targeted test result for the intended page URL and changed UI area.
- Evidence-based diagnosis using screenshots, an HTML report, traces, or captured responses.
- Source or snapshot changes only when the user has authorized them.
- A concise statement of whether the approved baseline passed or which intentional change was accepted.

## Context requirements

- A working Playwright setup inside a TYPO3 DDEV project.
- The site-package directory and the relevant spec or enough context to discover it.
- The actual public URL for editor-managed content or plugins.
- Authorization to run DDEV build, cache, and test commands; separate authorization for source or baseline updates.

## Installation

This directory is a portable Agent Skill. Install the complete plugin through a compatible Agent Plugin client, or copy/symlink this directory into that client’s Agent Skills discovery path. Codex can use the bundled `agents/openai.yaml` for presentation metadata.

Install the full directory, including `references/` and `evals/`, rather than `SKILL.md` alone.

## Example prompts

- “Verify the changed TYPO3 quick-menu section in DDEV against its existing Playwright baseline.”
- “The homepage visual test fails after my Fluid change. Diagnose it from the generated artifacts without updating snapshots.”
- “Run the mobile smoke and VRT checks for this mounted plugin page: https://example.ddev.site/news/search.”

## Included resources

- [VRT patterns and diagnostics](references/vrt-patterns.md)

## Validation

From the plugin root, validate the portable structure with the `new-skill` validator and the reference validator when available:

```bash
/path/to/new-skill/scripts/validate-skill.sh skills/typo3-playwright-workflow --strict-portable
skills-ref validate skills/typo3-playwright-workflow
```

Then review the representative, edge-case, and near-miss scenarios in [evals/evals.json](evals/evals.json). A workflow run is successful only when it reports the focused test result and preserves the baseline-update boundary.

## Related skills

- [TYPO3 Playwright Setup in DDEV](../typo3-playwright-ddev/README.md) for infrastructure setup and repair.
- Use this workflow for baseline-controlled verification of CSS migrations and other visual frontend changes.

## License

This skill is licensed under [CC BY 4.0](../../LICENSE). Copyright (c) 2026 Sven Kalbhenn.

# typo3-project-template

Create a reproducible TYPO3 v14 starter site from scratch or from a proven existing project.

## What this skill solves

It guides an agent through turning a working TYPO3 project into either a repository template, a Composer/Extension Manager distribution, or a sitepackage with demo content. The result follows TYPO3's Introduction Package pattern while keeping frontend implementation in the sitepackage and editor-facing content importable through `Initialisation/`.

## Use when

- You need a TYPO3 v14 quick-start project with Composer, a sitepackage, pages, content, media, and a basic site configuration.
- You want to extract a reusable template from an existing TYPO3 site without carrying secrets, production data, or instance-specific configuration.
- You need an installable distribution-style package similar to `typo3/cms-introduction`.

It is not a general TYPO3 extension-development skill and it does not replace a migration or deployment plan.

## Expected outputs

- A delivery decision: repository template, distribution extension, sitepackage, or a documented combination.
- A Composer-valid package layout and a declared clean-install command.
- An optional `Initialisation/` payload containing `data.xml`, referenced FAL assets, editor files, and `Site/<identifier>/config.yaml`.
- A fresh-install verification record.

## Context requirements

- The target TYPO3 v14 version and desired installation channel.
- For an existing-project base: its root directory, Composer files, local packages, and a source instance suitable for a redacted export.
- Authorization for any content that will be copied or distributed.

## Installation

Install the complete directory in a skill location recognized by the target client—for example, a Codex project's `.agents/skills/typo3-project-template/` directory. It uses only portable Agent Skills frontmatter, so it can also be installed in the equivalent skill location of another compatible client.

## Example prompts

- "Create a TYPO3 v14 project template based on this existing site, with a reusable sitepackage and safe demo content."
- "Add an Introduction Package-style sample page tree and site config to our TYPO3 v14 sitepackage."
- "Turn the `packages/acme_sitepackage` project into a Composer distribution and verify it against a blank TYPO3 instance."

## Validation

Validate the skill structure with:

```bash
validate-skill.sh path/to/typo3-project-template --strict-portable
skills-ref validate path/to/typo3-project-template
```

Validate a generated template with `composer validate`, followed by a new TYPO3 v14 installation and `vendor/bin/typo3 extension:setup`. Inspect the site configuration, page tree, frontend rendering, and FAL references in that clean environment.

## Related skills

- [`typo3-sitepackage`](../typo3-sitepackage/README.md) — builds the reusable theme and configuration extension that a starter template can package with demo data.
- [`typo3-site-sets`](../typo3-site-sets/README.md) — separates reusable Site Set defaults from the concrete site configuration imported by a template.
- [`typo3-ddev-worktree`](../typo3-ddev-worktree/README.md) — prepares a DDEV repository for isolated template-development worktrees and fresh runtime checks.
- [`typo3-deployer-deployment`](../typo3-deployer-deployment/README.md) — configures deployment once a repository template intentionally includes a deployment workflow.

## License

CC-BY-4.0. The skill links to official TYPO3 documentation; those sources retain their own licenses and terms.

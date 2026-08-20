# TYPO3 Content Blocks

## What this skill solves

Creates, changes, and diagnoses `friendsoftypo3/content-blocks` definitions without bypassing the project's existing Content Block conventions.

## Use when

Use for Content Element, Page Type, Record Type, File Type, field, label, template, preview, discovery, or `content-blocks:lint` work. It does not design unrelated TYPO3 extensions or replace a project's content model.

## Expected outputs

A minimal, correctly placed Content Block change; explicit schema and naming assumptions; and the project's cache, setup, and lint checks.

## Context requirements

Provide the owning site package or extension, block type/name, required fields and rendering, and any existing block to follow. The project must include `friendsoftypo3/content-blocks`.

## Installation

Install the enclosing plugin as described in the [plugin README](../../README.md), or copy this directory to a supported client Skill location such as `.agents/skills/typo3-content-blocks/`. Codex presentation metadata is in `agents/openai.yaml`; the runtime instructions remain portable.

## Example prompts

- “Create a `teaser-card` Content Block in our site package with header, image, text, a frontend template, and a backend preview.”
- “Fix this `content-blocks:lint` error at `/fields/3/fields/0` without changing unrelated fields.”
- “Why does our existing Content Block show label keys in the backend and no wizard icon?”

## Validation

Run the project's normal `content-blocks:lint`, extension setup, and cache-flush commands. Maintainers can validate the Skill with `new-skill/scripts/validate-skill.sh skills/typo3-content-blocks --strict-portable`.

## Related skills

None in this plugin; use project-specific site-package guidance for broader TCA or extension architecture.

## License

Licensed under [CC BY 4.0](../../LICENSE).

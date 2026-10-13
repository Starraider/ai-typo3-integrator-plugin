---
name: typo3-iconpack
description: Install, configure, use, and troubleshoot quellenform/t3x-iconpack and provider packs such as Font Awesome in TYPO3 Composer projects. Use for Iconpack provider registration and YAML overrides, rendering TypoScript, custom extension and site-package icons, Fluid ViewHelpers, backend iconIdentifier/TCA integration, CSS and SVG assets, CKEditor icon insertion and persistence, or pack upgrades. Excludes unrelated TYPO3 backend icons without Iconpack, generic RTE configuration, and npm-only icon libraries.
license: CC-BY-4.0
compatibility: Requires filesystem access to a TYPO3 Composer project and its owning extension or site package. Dependency changes need Composer, PHP, and network access; editor verification needs TYPO3 backend access. Examples are source-checked against Iconpack 1.5.5 and Font Awesome provider 1.3.1.
---

# TYPO3 Iconpack

Deliver a versioned integration of `quellenform/t3x-iconpack` and at least one provider, with icons verified in the requested backend, frontend, and editor contexts. Author configuration in the owning site package or extension; keep vendor files untouched.

## 1. Inspect the project and select a compatible release

Read applicable repository instructions. Identify TYPO3/PHP versions from `composer.lock`, Composer wrapper (for example DDEV), document root, owning extension key, current static includes or site sets, target fields/modules/templates, and existing RTE preset. Inspect installed providers and their `ext_localconf.php`, `ext_conf_template.txt`, and YAML before choosing keys or asset paths.

Read [installation and configuration](references/installation-configuration.md) for commands, version constraints, settings, inclusion order, and provider YAML. Read [verified sources](references/sources.md) when a target release differs from the documented baseline; recheck its actual source rather than assuming main documentation matches it.

Completion: record the selected TYPO3/Iconpack/provider versions, Composer package names, TYPO3 extension keys, pack key, styles, asset files, and configuration owner. The package version and the bundled icon-library version are separate values.

## 2. Install the extension and an additional provider

Use the project's Composer wrapper. Preview resolution, then install compatible constrained releases of `quellenform/t3x-iconpack` and, by default, `quellenform/t3x-iconpack-fontawesome`. Preserve existing lockfile and dependency conventions. Run TYPO3's version-appropriate extension setup and cache flush.

The Font Awesome provider self-registers. Do not register the same pack again or invent a TypoScript `iconPacks` list. PHP `IconpackRegistry::registerIconpack()` loads provider YAML; TypoScript only changes frontend rendering. Pack YAML does not become active just because it exists on disk.

Completion: Composer shows both packages, TYPO3 boots without registration errors, and the expected provider appears in the icon selector.

## 3. Configure extension settings and frontend rendering

Keep `autoConfigRte` and `autoAddAssets` enabled unless the project explicitly owns their replacement. Configure the provider's `version`, `stylesEnabled`, and optional `configFile` through extension configuration. Load Iconpack's static TypoScript or the `quellenform/iconpack` site set, then apply site-package rendering overrides after competing RTE parse-function definitions.

For provider overrides, use an extension-owned YAML file through the provider's supported `configFile` setting. The registry merges only top-level `iconpack` keys: overriding `renderTypes` replaces that whole branch. Preserve stable `key` values used in stored content; use `hidden: false` when a pack should be selectable.

Completion: inspect resolved settings and `lib.parseFunc_RTE.nonTypoTagUserFunc`; confirm the requested native/RTE render types and provider styles are available.

## 4. Integrate custom extensions, site packages, and assets

Read [extension, Fluid, and asset examples](references/extension-fluid-assets.md) before implementing this branch. Register custom packs in `ext_localconf.php`. Use `IconpackWizard` for selectable icon fields, and the Iconpack Fluid ViewHelper with `iconfig` values for content icons.

Keep TYPO3's Core `IconRegistry` separate: backend module `iconIdentifier`, wizard `iconIdentifier`, TCA `typeicon_classes`, and `<core:icon>` require Core identifiers. Bridge an installed provider's SVG file through `Configuration/Icons.php`. A string such as `fa7:solid,house` is an Iconpack iconfig, not a Core identifier. Do not invent `t3skin-icon` mappings; explain legacy requests and use the documented migration path.

Use `EXT:` paths and TYPO3 asset APIs. Do not hard-code `_assets/<hash>` URLs or edit `vendor/`. Backend modules and frontend plugins need their own asset inclusion when automatic loading is unavailable or the chosen render type differs from the globally configured one.

Completion: a representative icon renders in every requested extension/module/template, references a real asset, and has appropriate text or an accessible label when it conveys meaning.

## 5. Integrate and round-trip RTE icons

Read [RTE integration and persistence](references/rte.md). For TYPO3 12+, use the supplied CKEditor 5 `Iconpack` plugin and toolbar item. Page TSconfig assigns the RTE preset; plugin imports and toolbar items belong in YAML. Use automatic configuration or manual preset imports consistently, avoiding duplicate plugin/toolbar registration.

Keep editor schema, PHP persistence transformation, frontend parse function, and HTML sanitizer aligned. Iconpack stores `data-iconfig` placeholders and reconstructs selected markup; do not treat raw pasted SVG or a CSS-only span as equivalent. Preserve existing sanitizer integrations and content filtering.

Completion: the intended editor role can insert and edit an icon; save/reopen retains it; stored content contains the iconfig; frontend output renders the correct icon after cache flush. Check both webfont and SVG when requested.

## 6. Verify, troubleshoot, and maintain

Read [verification, troubleshooting, and maintenance](references/operations.md) for commands, filesystem/log locations, fixes, backups, and upgrades. Test asset URLs in browser Network and inspect console/CSP failures. Fix ownership and symlink publication at the narrowest path supported by the deployment model.

For upgrades, preserve a restorable database and files backup, manifest/lockfile, presets, pack keys, and representative stored content. Update only the requested packages and necessary dependencies; rerun backend/frontend/RTE checks before rollout.

Completion: report changed files, package versions, validation evidence, and any untested runtime contexts. Never equate Composer success with working RTE persistence.

## Authorization and scope

Creating this skill does not install packages into a TYPO3 site. On invocation, an explicit request to install/configure authorizes the necessary local dependency/configuration changes; do not ask again for routine reversible work. Follow the user's scope for production changes, publication, content migrations, or database restoration. Explain a needed boundary before crossing it. Do not delete whole cache trees, disable the sanitizer, use `chmod -R 777`, or uninstall existing packs as a repair shortcut.

## Maintainer validation

Use [evals/evals.json](evals/evals.json) for representative, edge-case, regression, and near-miss scenarios. Run:

```bash
bash /path/to/new-skill/scripts/validate-skill.sh skills/typo3-iconpack --strict-portable
skills-ref validate skills/typo3-iconpack
python3 /path/to/new-plugin/scripts/validate_agent_plugin.py . --strict
```

Structural checks are distinct from exercising a TYPO3 installation. Record the distinction in the result.

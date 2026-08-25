---
name: typo3-sitepackage
description: "Create or extend a TYPO3 v13/v14 site package extension. Use when scaffolding a new site package from scratch, deciding where files belong inside a site package, overriding templates of other extensions (EXT:fluid_styled_content, EXT:form, etc.) through the site package, or wiring a site set inside the site package. Covers composer.json, ext_emconf.php, Configuration/Sets/, Resources/Private/ directory layout, TypoScript page rendering via PAGEVIEW, template override paths, and installation steps. Do not use for Extbase controller wiring, route enhancers, or CSP headers — hand off to the matching skill."
license: CC-BY-4.0
compatibility: TYPO3 v13 and v14 (Composer mode). Requires site sets (introduced in TYPO3 v13).
---

# TYPO3 Site Package

Guide for creating and maintaining a TYPO3 v13/v14 site package using Site Sets. A site package is a regular TYPO3 extension that acts as the main theme and configuration layer for a site.

> **Start fast:** Generate a boilerplate at https://get.typo3.org/sitepackage. Place the result in `packages/my_site_package/` and install with Composer.

## Workflow

### 0. Choose a base content rendering package

Before scaffolding, ask which base package the project uses — the choice affects `composer.json`, the Site Set dependency, and the template override approach:

| | **EXT:fluid_styled_content** | **Bootstrap Package** |
|---|---|---|
| Composer package | `typo3/cms-fluid-styled-content` | `bk2k/bootstrap-package` |
| Site Set name | `typo3/fluid-styled-content` | `bk2k/bootstrap-package` (Full Package) |
| Template overrides | Via `lib.contentElement` path keys | Via Bootstrap Package's own path keys |
| Can coexist? | — | **No — conflicts with `fluid_styled_content`** |
| CSS included? | Optional (`typo3/fluid-styled-content-css`) | Yes, Bootstrap 5 CSS included |
| Site Package Builder type | "Fluid Styled Content" or "Site Package Tutorial" | "Bootstrap Package" |

**Ask the user:** *"Does this project use `EXT:fluid_styled_content` or the Bootstrap Package (`bk2k/bootstrap-package`)?"*

If the answer is Bootstrap Package: do **not** require `typo3/cms-fluid-styled-content` and do **not** install it — the two extensions conflict.

Completion: the base content rendering choice is confirmed before any files are written.

---

### 1. Scaffold the extension skeleton

Create the following minimum file set. See [templates/skeleton.md](templates/skeleton.md) for ready-to-copy file contents.

```text
packages/my_site_package/
├── composer.json
├── Configuration/
│   └── Sets/
│       └── SitePackage/
│           ├── config.yaml                    ← Site Set definition
│           ├── settings.definitions.yaml      ← Typed site settings
│           ├── settings.yaml                  ← Shipped defaults
│           ├── setup.typoscript               ← @import entry point
│           └── TypoScript/
│               ├── page.typoscript            ← PAGE / PAGEVIEW + template paths
│               └── content.typoscript         ← lib.dynamicContent
├── Resources/
│   ├── Private/
│   │   ├── Language/
│   │   ├── Layouts/Pages/ and Layouts/Content/
│   │   ├── Partials/Pages/ and Partials/Content/
│   │   └── Templates/Pages/ and Templates/Content/
│   └── Public/
│       ├── Css/
│       ├── JavaScript/
│       └── Icons/
└── Initialisation/
    └── Site/main/config.yaml
```

Completion: all mandatory directories and files exist; `composer validate` passes.

---

### 2. Write `composer.json`

```json
{
    "name": "my-vendor/my-site-package",
    "type": "typo3-cms-extension",
    "description": "Site package for my project",
    "license": ["GPL-2.0-or-later"],
    "require": {
        "typo3/cms-core": "^13.4 || ^14.0",
        "typo3/cms-fluid-styled-content": "^13.4 || ^14.0"
    },
    "autoload": {
        "psr-4": {
            "MyVendor\\MySitePackage\\": "Classes/"
        }
    },
    "extra": {
        "typo3/cms": {
            "extension-key": "my_site_package"
        }
    }
}
```

For **EXT:fluid_styled_content** projects, the `require` block is:

```json
"require": {
    "typo3/cms-core": "^13.4 || ^14.0",
    "typo3/cms-fluid-styled-content": "^13.4 || ^14.0"
}
```

For **Bootstrap Package** projects, replace it with:

```json
"require": {
    "typo3/cms-core": "^13.4 || ^14.0",
    "bk2k/bootstrap-package": "^16.0"
}
```

> **Important:** Do not include both. Bootstrap Package marks `fluid_styled_content` as a conflicting extension — requiring both will cause installation errors.

Rules:
- `"type"` must be `"typo3-cms-extension"`.
- Composer package name uses **dashes** (`my-vendor/my-site-package`).
- TYPO3 extension key uses **underscores** (`my_site_package`) in `extra.typo3/cms.extension-key` and all `EXT:` references.

Completion: `ddev composer require my-vendor/my-site-package:@dev` installs without error.

---

### 3. Define the Site Set

**`Configuration/Sets/SitePackage/config.yaml`**

For **EXT:fluid_styled_content** projects:

```yaml
name: my-vendor/site-package
label: 'My Site Package'
dependencies:
  - typo3/fluid-styled-content
  - typo3/fluid-styled-content-css  # remove if shipping own CSS
```

For **Bootstrap Package** projects:

```yaml
name: my-vendor/site-package
label: 'My Site Package'
dependencies:
  - bk2k/bootstrap-package
```

The Bootstrap Package's "Full Package" set (`bk2k/bootstrap-package`) includes all Bootstrap 5 assets, content element rendering, and TypoScript — do not add `typo3/fluid-styled-content` or `typo3/fluid-styled-content-css` as additional dependencies.

- `name` must be globally unique in `vendor/package` form.
- List all required upstream sets in `dependencies`; do not use TypoScript `@import` for cross-extension ordering.

**`Configuration/Sets/SitePackage/settings.definitions.yaml`** (example)

```yaml
settings:
  SitePackage:
    template_path:
      type: string
      default: 'EXT:my_site_package/Resources/Private/Templates/'
      label: 'Template path override'
    favicon:
      type: string
      default: 'EXT:my_site_package/Resources/Public/Icons/favicon.ico'
      label: 'Favicon path'
```

Completion: the set appears in **Sites › Setup** in the TYPO3 backend.

> **Cross-reference:** For detailed Site Set rules, `settings.definitions.yaml` patterns, and per-site override placement see `typo3-site-sets`.

---

### 4. Wire the site config

In `config/sites/<site-id>/config.yaml` (outside the package):

```yaml
base: '/'
rootPageId: 1
dependencies:
  - my-vendor/site-package
languages:
  - title: English
    enabled: true
    languageId: 0
    base: /
    locale: en_US.UTF-8
```

Never place `base`, `rootPageId`, or language config inside the site package.

Completion: TYPO3 frontend loads without "No TypoScript template found" errors.

---

### 5. Configure page rendering (PAGEVIEW)

**`Configuration/Sets/SitePackage/TypoScript/page.typoscript`**

```typoscript
page = PAGE
page {
    10 = PAGEVIEW
    10 {
        paths {
            0 = EXT:my_site_package/Resources/Private/Templates/
            10 = {$SitePackage.template_path}
        }
    }
    shortcutIcon = {$SitePackage.favicon}
}
```

`PAGEVIEW` (available since TYPO3 v13) resolves page templates from the configured paths automatically based on the backend layout identifier. Higher numeric path keys take precedence.

**`Configuration/Sets/SitePackage/setup.typoscript`**

```typoscript
@import 'EXT:my_site_package/Configuration/Sets/SitePackage/TypoScript/page.typoscript'
@import 'EXT:my_site_package/Configuration/Sets/SitePackage/TypoScript/content.typoscript'
```

Completion: the default page template renders on the frontend without Fluid exceptions.

> **Cross-reference:** For `lib.dynamicContent`, colPos propagation, Fluid template hierarchy, responsive images, and icon patterns see `typo3-fluid-patterns`.

---

### 6. Override templates of other extensions

> **Note:** Template override mechanics differ between base packages.
> - **EXT:fluid_styled_content:** override via `lib.contentElement` path keys (below).
> - **Bootstrap Package:** override via Bootstrap Package's own path keys — use the same numeric key pattern but target `plugin.tx_bootstrappackage` or the Bootstrap Package's Fluid paths. Consult the [Bootstrap Package docs](https://docs.typo3.org/p/bk2k/bootstrap-package/16.0/en-us/) for available override keys.

Add higher-priority paths (higher numeric key = higher priority) in your TypoScript.

#### Override EXT:fluid_styled_content content elements (fluid-styled-content mode only)

```typoscript
lib.contentElement {
    templateRootPaths {
        10 = EXT:my_site_package/Resources/Private/Templates/Content/
    }
    partialRootPaths {
        10 = EXT:my_site_package/Resources/Private/Partials/Content/
    }
    layoutRootPaths {
        10 = EXT:my_site_package/Resources/Private/Layouts/Content/
    }
}
```

Copy only the template file(s) you intend to change; unchanged ones are inherited from path `0`.

Example — override the Text content element:
- Source (do not edit): `vendor/typo3/cms-fluid-styled-content/Resources/Private/Templates/Text.html`
- Override: `EXT:my_site_package/Resources/Private/Templates/Content/Text.html`

#### Override EXT:form templates

```typoscript
plugin.tx_form {
    settings {
        framework {
            layoutRootPaths {
                20 = EXT:my_site_package/Resources/Private/Layouts/Form/
            }
            templateRootPaths {
                20 = EXT:my_site_package/Resources/Private/Templates/Form/
            }
            partialRootPaths {
                20 = EXT:my_site_package/Resources/Private/Partials/Form/
            }
        }
    }
}
```

Rules:
- Never edit files inside `vendor/` or `public/typo3/`.
- Use a numeric key strictly higher than the original extension's highest key.
- Add the TypoScript inside `setup.typoscript` or a dedicated import.

Completion: the overriding template renders; the original extension file is unmodified.

> **Cross-reference:** For advanced Fluid patterns inside overriding templates see `typo3-fluid-patterns`.

---

### 7. Install and verify

```bash
# 1. Ensure packages/ is a Composer path repository in root composer.json:
#    "repositories": [{"type": "path", "url": "packages/*"}]

ddev composer require my-vendor/my-site-package:@dev

# 2. TYPO3 backend:
#    Sites › Setup — add your set to the site
#    Admin Tools › Maintenance — Flush all caches

# 3. Preview a frontend page
```

Completion: the frontend page renders with your templates; no Fluid or TypoScript errors appear in the TYPO3 log.

---

## File Placement Quick Reference

| File / folder | Purpose |
|---|---|
| `Configuration/Sets/SitePackage/config.yaml` | Site Set definition |
| `Configuration/Sets/SitePackage/settings.definitions.yaml` | Typed setting definitions |
| `Configuration/Sets/SitePackage/settings.yaml` | Shipped setting defaults |
| `Configuration/Sets/SitePackage/setup.typoscript` | TypoScript entry point |
| `Configuration/Sets/SitePackage/TypoScript/` | Page & content TypoScript |
| `Resources/Private/Layouts/Pages/` | Outer HTML shell |
| `Resources/Private/Layouts/Content/` | Content element layouts |
| `Resources/Private/Templates/Pages/` | Page templates |
| `Resources/Private/Templates/Content/` | Content element templates |
| `Resources/Private/Partials/Pages/` | Header, footer partials |
| `Resources/Private/Partials/Content/` | Content-specific partials |
| `Resources/Private/Language/` | XLIFF files |
| `Resources/Public/Css/` | Compiled CSS |
| `Resources/Public/JavaScript/` | Client-side JS |
| `Resources/Public/Icons/` | SVG icons, favicon |
| `config/sites/<site>/config.yaml` | Site instance config (outside package) |
| `config/sites/<site>/settings.yaml` | Per-site setting overrides (outside package) |

## Handoff To Other TYPO3 Skills

- Fluid template hierarchy, `lib.dynamicContent`, responsive images, icons: `typo3-fluid-patterns`
- Site Set placement, `settings.definitions.yaml`, typed overrides: `typo3-site-sets`
- TypoScript conditions and `[site(...)]` context: `typo3-typoscript-conditions`
- Route enhancers in `config/sites/<site>/config.yaml`: `typo3-route-enhancers`
- XML sitemap configuration: `typo3-xml-sitemap`
- Custom content elements via Content Blocks: `typo3-content-blocks`
- DDEV + Playwright browser testing: `typo3-playwright-ddev`

## Completion And Boundaries

Never put `base`, `rootPageId`, or language configuration inside the site package. Never register TypoScript globally in PHP when Site Sets can carry it. Never use cross-extension TypoScript `@import` as the primary dependency mechanism. Complete only after the frontend renders all target page templates and no Fluid or TypoScript errors remain in the log.

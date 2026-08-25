# Site Package Skeleton — Copy Reference

Use these ready-to-copy file contents when scaffolding a new TYPO3 v13/v14 site package.
Replace `my_site_package` (extension key) and `my-vendor/my-site-package` (Composer name) throughout.

> **Before copying:** confirm whether the project uses `EXT:fluid_styled_content` or the Bootstrap Package (`bk2k/bootstrap-package`). The two conflict and cannot be installed together. Choose the matching variant below for `composer.json` and `config.yaml`.

---

## `composer.json` — Variant A: EXT:fluid_styled_content

```json
{
    "name": "my-vendor/my-site-package",
    "type": "typo3-cms-extension",
    "description": "Site package for my project",
    "license": ["GPL-2.0-or-later"],
    "keywords": ["TYPO3 CMS"],
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
            "extension-key": "my_site_package",
            "version": "1.0.0"
        }
    }
}
```

## `composer.json` — Variant B: Bootstrap Package

> **Do not** add `typo3/cms-fluid-styled-content` here — Bootstrap Package conflicts with it.

```json
{
    "name": "my-vendor/my-site-package",
    "type": "typo3-cms-extension",
    "description": "Site package for my project",
    "license": ["GPL-2.0-or-later"],
    "keywords": ["TYPO3 CMS"],
    "require": {
        "typo3/cms-core": "^13.4 || ^14.0",
        "bk2k/bootstrap-package": "^16.0"
    },
    "autoload": {
        "psr-4": {
            "MyVendor\\MySitePackage\\": "Classes/"
        }
    },
    "extra": {
        "typo3/cms": {
            "extension-key": "my_site_package",
            "version": "1.0.0"
        }
    }
}
```

---

## `Configuration/Sets/SitePackage/config.yaml` — Variant A: EXT:fluid_styled_content

```yaml
name: my-vendor/site-package
label: 'My Site Package'
dependencies:
  - typo3/fluid-styled-content
  - typo3/fluid-styled-content-css
```

## `Configuration/Sets/SitePackage/config.yaml` — Variant B: Bootstrap Package

The Bootstrap Package's site set provides all content rendering, Bootstrap 5 CSS, and TypoScript.
Do **not** add `typo3/fluid-styled-content` or `typo3/fluid-styled-content-css` as additional dependencies.

```yaml
name: my-vendor/site-package
label: 'My Site Package'
dependencies:
  - bk2k/bootstrap-package
```

---

## `Configuration/Sets/SitePackage/settings.definitions.yaml`

```yaml
settings:
  SitePackage:
    template_path:
      type: string
      default: 'EXT:my_site_package/Resources/Private/Templates/'
      label: 'Additional template path'
    favicon:
      type: string
      default: 'EXT:my_site_package/Resources/Public/Icons/favicon.ico'
      label: 'Favicon path'
```

---

## `Configuration/Sets/SitePackage/setup.typoscript`

```typoscript
@import 'EXT:my_site_package/Configuration/Sets/SitePackage/TypoScript/page.typoscript'
@import 'EXT:my_site_package/Configuration/Sets/SitePackage/TypoScript/content.typoscript'
```

---

## `Configuration/Sets/SitePackage/TypoScript/page.typoscript`

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

---

## `Configuration/Sets/SitePackage/TypoScript/content.typoscript`

```typoscript
# Override template paths for fluid_styled_content elements
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

# lib.dynamicContent — render content from a colPos
lib.dynamicContent = COA
lib.dynamicContent {
    10 = LOAD_REGISTER
    10 {
        colPos.cObject = TEXT
        colPos.cObject {
            field = colPos
            ifEmpty.data = register:colPos
            ifEmpty.ifEmpty = 0
        }
    }
    20 = CONTENT
    20 {
        table = tt_content
        select {
            orderBy = sorting
            where = {#colPos}={register:colPos}
            languageField = sys_language_uid
        }
    }
    90 = RESTORE_REGISTER
}
```

---

## `Resources/Private/Templates/Pages/Default.html`

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">
<f:layout name="Pages/Default"/>
<f:section name="Main">
    <f:cObject typoscriptObjectPath="lib.dynamicContent" data="{colPos: 0}"/>
</f:section>
</html>
```

---

## `Resources/Private/Layouts/Pages/Default.html`

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">
<!DOCTYPE html>
<html lang="{site.language.twoLetterIsoCode}">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title><f:if condition="{page.title}"><f:then>{page.title} — </f:then></f:if>{site.websiteTitle}</title>
    <f:asset.css identifier="site-css" href="EXT:my_site_package/Resources/Public/Css/main.css"/>
</head>
<body>
    <a href="#main-content" class="skip-link">
        <f:translate domain="my_site_package.messages" key="skip.to.content" default="Skip to main content"/>
    </a>
    <header>
        <f:render partial="Pages/Header" arguments="{_all}"/>
    </header>
    <main id="main-content">
        <f:render section="Main" />
    </main>
    <footer>
        <f:render partial="Pages/Footer" arguments="{_all}"/>
    </footer>
    <f:asset.script identifier="site-js" href="EXT:my_site_package/Resources/Public/JavaScript/main.js" type="module"/>
</body>
</html>
</html>
```

---

## `Initialisation/Site/main/config.yaml`

This file is imported once on first install to pre-populate the site configuration.

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
    navigationTitle: English
    flag: us
websiteTitle: 'My Site'
```

---

## Root `composer.json` path repository (add to project root)

```json
{
    "repositories": [
        {
            "type": "path",
            "url": "packages/*"
        }
    ]
}
```

Then install with:

```bash
ddev composer require my-vendor/my-site-package:@dev
```

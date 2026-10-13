# Installation and configuration

Examples use project root commands, document root `public/`, and a local extension at `packages/sitepackage/` with TYPO3 extension key `sitepackage`. Replace these only with values discovered in the target project. `EXT:sitepackage/...` is a TYPO3 resource reference, not a shell path.

## Packages and versions

| Composer package | TYPO3 extension key | Pack identifier |
| --- | --- | --- |
| `quellenform/t3x-iconpack` | `iconpack` | Registry/rendering extension; no Font Awesome assets by itself |
| `quellenform/t3x-iconpack-fontawesome` | `iconpack_fontawesome` | `fa7`, `fa6`, or `fa5`, selected by provider configuration |

The source-checked releases are Iconpack 1.5.5 and provider 1.3.1. In these releases the provider defaults to Font Awesome 7.1.0, key `fa7`; provider setting `version = 6` selects bundled 6.7.2/key `fa6`, and `5` selects 5.15.4/key `fa5`. Never infer the key from the Composer version. [Provider configuration source](https://github.com/quellenform/t3x-iconpack-fontawesome/blob/1.3.1/ext_conf_template.txt).

Iconpack 1.5.5 declares TYPO3 `>=10.4.11 <12 || >=12.4.7 <15 || 15.*.*@dev`; provider 1.3.1 requires Iconpack `^1.3.3`. Prefer the installed supported TYPO3 line. A development constraint is not a recommendation to enable `minimum-stability: dev`. [Iconpack manifest](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/composer.json), [provider manifest](https://github.com/quellenform/t3x-iconpack-fontawesome/blob/1.3.1/composer.json).

## Inspect and install

```bash
composer show typo3/cms-core
composer show quellenform/t3x-iconpack --all
composer show quellenform/t3x-iconpack-fontawesome --all
composer require 'quellenform/t3x-iconpack:~1.5.5' --dry-run
composer require 'quellenform/t3x-iconpack:~1.5.5'
composer require 'quellenform/t3x-iconpack-fontawesome:~1.3.1' --dry-run
composer require 'quellenform/t3x-iconpack-fontawesome:~1.3.1'
composer show quellenform/t3x-iconpack
composer show quellenform/t3x-iconpack-fontawesome
vendor/bin/typo3 list
vendor/bin/typo3 extension:setup --help
vendor/bin/typo3 extension:setup --extension=iconpack
vendor/bin/typo3 extension:setup --extension=iconpack_fontawesome
vendor/bin/typo3 cache:flush
```

The plain package installation commands are `composer require quellenform/t3x-iconpack` and `composer require quellenform/t3x-iconpack-fontawesome`; the constrained variants above keep updates in the verified minor lines. Alternatively install both constrained packages in one `composer require` transaction. On an existing incompatible lockfile, inspect Composer's error and `composer prohibits quellenform/t3x-iconpack 1.5.5` before changing constraints. Use `--with-all-dependencies` only when necessary and review all affected packages.

For DDEV, use `ddev composer ...` and `ddev exec vendor/bin/typo3 ...`. Older TYPO3 lines may lack the shown setup command; use the project's existing version-appropriate setup tooling or Install Tool database analysis. Setup may add database fields; inspect the proposed changes and follow project backup conventions. Composer-mode packages are discovered automatically; an Extension Manager activation step is generally unnecessary. [TYPO3 Composer extension installation](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Administration/ExtensionManagement/Composer/Index.html).

## Extension configuration

Use **Admin Tools / Settings → Extension Configuration** (menu wording differs by TYPO3 version) or TYPO3's effective PHP system configuration. In modern Composer installations values are normally persisted under `config/system/settings.php`; site-local overrides can live in `config/system/additional.php`. Older projects may use `public/typo3conf/LocalConfiguration.php` and `AdditionalConfiguration.php`. Inspect existing files instead of creating a second configuration root.

Baseline Iconpack settings from [ext_conf_template.txt](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/ext_conf_template.txt):

| Exact key under `EXTENSIONS.iconpack` | Default | Effect |
| --- | --- | --- |
| `autoConfigRte` | `1` | Add Iconpack editor plugin, button and configuration automatically |
| `rteSvg` | `1` | Add SVG choices to backend RTE defaults; explicit provider preferences can override them |
| `autoAddAssets` | `1` | Add provider CSS to frontend output automatically |
| `defaultConfig` | `EXT:iconpack/Configuration/Iconpack/Default.yaml` | Default options/transforms for packs; not a pack registration list |
| `formElementStyle` | `iconButton` | `iconButton`, `iconInputButton`, `iconInput`, or `icon` for icon picker fields |

The Font Awesome provider has `version` (default `7`), `configFile` (default empty), and `stylesEnabled` (default empty, meaning use pack YAML). Example addition to an existing `config/system/additional.php`:

```php
<?php

$GLOBALS['TYPO3_CONF_VARS']['EXTENSIONS']['iconpack'] = array_replace(
    $GLOBALS['TYPO3_CONF_VARS']['EXTENSIONS']['iconpack'] ?? [],
    [
        'autoConfigRte' => '1',
        'rteSvg' => '1',
        'autoAddAssets' => '1',
        'defaultConfig' => 'EXT:iconpack/Configuration/Iconpack/Default.yaml',
        'formElementStyle' => 'iconInputButton',
    ]
);
$GLOBALS['TYPO3_CONF_VARS']['EXTENSIONS']['iconpack_fontawesome'] = array_replace(
    $GLOBALS['TYPO3_CONF_VARS']['EXTENSIONS']['iconpack_fontawesome'] ?? [],
    [
        'version' => '7',
        'stylesEnabled' => 'solid,regular,brands',
        'configFile' => 'EXT:sitepackage/Configuration/Iconpack/FontAwesomeOverrides.yaml',
    ]
);
```

Create the override file before enabling its path. An empty `configFile` uses the provider defaults. This configuration must be available before the provider's `ext_localconf.php` runs; putting it in an arbitrary later extension can depend on load order. Preserve other entries and avoid multiple opening `<?php` tags when editing an existing file.

## Register and enable the additional pack

Installing the Font Awesome provider is the registration step: its own `ext_localconf.php` calls `IconpackRegistry::registerIconpack()` with the selected `FontAwesome7.yaml`/`6`/`5` file, the optional merge file, and its preprocessor. Do not repeat that call in the site package. [Actual registration](https://github.com/quellenform/t3x-iconpack-fontawesome/blob/1.3.1/ext_localconf.php).

`packages/sitepackage/Configuration/Iconpack/FontAwesomeOverrides.yaml`:

```yaml
iconpack:
  hidden: false
  preferredRenderTypes:
    backend:
      native: 'svgInline,svgSprite,webfont,svg'
      rte: 'webfont,svg'
    frontend:
      native: 'svgInline,svgSprite,webfont,svg'
      rte: 'svgSprite,webfont,svg'
```

This selects backend webfont RTE icons and frontend SVG sprites for the same stored iconfig. Use `rteSvg: 1` in extension configuration if SVG is desired in the editor too; then change `backend.rte` to `svgInline,svgSprite,webfont,svg`. This is provider YAML, not RTE YAML or a site `config.yaml` property.

The registry merges using PHP `array_merge` at the first `iconpack` level. Each supplied key replaces the complete value under that key. Thus the example intentionally supplies both contexts under `preferredRenderTypes`. A partial `renderTypes` override removes the omitted renderers/styles/default CSS. Start from the installed provider's complete branch when modifying asset locations. Do not change `key: fa7` in an override: stored content depends on it. Provider extension setting `stylesEnabled` overrides YAML when nonempty. [Registry merge implementation](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Classes/IconpackRegistry.php), [Font Awesome preprocessor](https://github.com/quellenform/t3x-iconpack-fontawesome/blob/1.3.1/Classes/Configuration/IconpackConfiguration.php).

## Load the frontend TypoScript

Choose the project's existing inclusion mechanism; do not import the same extension twice.

**Static templates / TYPO3 12:** Include Iconpack's provided static TypoScript after `fluid_styled_content` or any framework that writes `lib.parseFunc_RTE`. Or explicitly import it in the owning site package:

`packages/sitepackage/Configuration/TypoScript/constants.typoscript`:

```typoscript
@import 'EXT:iconpack/Configuration/TypoScript/constants.typoscript'
```

`packages/sitepackage/Configuration/TypoScript/setup.typoscript`:

```typoscript
@import 'EXT:iconpack/Configuration/TypoScript/setup.typoscript'

plugin.tx_iconpack.settings {
  cssClass = iconpack
  renderTypes {
    _default {
      native = svgInline,svgSprite,webfont,svg
      rte = svgSprite,webfont,svg
    }
    fa7 {
      native = svgInline
      rte = svgSprite,webfont
    }
  }
}
```

Make sure the site's root template includes the owning site package. Constants supply the base CSS reference; importing setup alone leaves unresolved constant placeholders. TypoScript changes frontend preference only and does not install, register, or hide packs. A scalar shorthand such as `plugin.tx_iconpack.settings.renderTypes.fa7 = webfont` applies to both native and RTE contexts. [Shipped setup](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Configuration/TypoScript/setup.typoscript).

**Site sets / TYPO3 13+:** Add to the existing set definition, for example `packages/sitepackage/Configuration/Sets/Site/config.yaml`:

```yaml
name: vendor/sitepackage
label: Site Package
dependencies:
  - typo3/fluid-styled-content
  - quellenform/iconpack
```

Activate the owning set in `config/sites/<site-identifier>/config.yaml` through the Sites module or its existing versioned configuration:

```yaml
dependencies:
  - vendor/sitepackage
```

Put site-specific `plugin.tx_iconpack.settings` overrides in that set's `setup.typoscript`. Iconpack's set exists in the baseline release; older releases may require static includes. Site set dependencies load shared configuration, not pack providers. [Shipped set name](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Configuration/Sets/Iconpack/config.yaml).

The provided setup installs this frontend transformation:

```typoscript
lib.parseFunc_RTE.nonTypoTagUserFunc = Quellenform\Iconpack\UserFunc\ParseFuncRte->replaceIcons
lib.parseFunc.nonTypoTagUserFunc < lib.parseFunc_RTE.nonTypoTagUserFunc
```

Inspect the final resolved setup if a framework overwrites it. If a different extension already owns `nonTypoTagUserFunc`, review and compose the two transformations rather than silently replacing one. Bootstrap Package integrations are a separate optional provider integration; do not install them unless needed.

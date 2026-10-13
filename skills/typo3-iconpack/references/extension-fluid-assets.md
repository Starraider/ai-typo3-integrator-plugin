# Custom extensions, Fluid, and assets

Examples use an installed site package at `packages/sitepackage/` and Font Awesome provider 1.3.1 configured for version 7. Resolve actual assets from the installed provider YAML when using another release or style.

## Register a custom pack in ext_localconf.php

For a project-owned SVG set, create `packages/sitepackage/Configuration/Iconpack/SiteIcons.yaml`:

```yaml
iconpack:
  title: 'Site Icons'
  key: 'siteicons'
  version: '1.0.0'
  hidden: false
  preferredRenderTypes:
    backend:
      native: 'svgInline,svgSprite'
      rte: 'svgInline,svgSprite'
    frontend:
      native: 'svgInline,svgSprite'
      rte: 'svgSprite,svgInline'
  renderTypes:
    svgInline:
      source: 'EXT:sitepackage/Resources/Public/Icons/Site/'
      css: 'EXT:sitepackage/Resources/Public/Css/site-icons.css'
      attributes:
        class: 'site-icon'
        fill: 'currentColor'
    svgSprite:
      source: 'EXT:sitepackage/Resources/Public/Icons/site-icons.svg'
      css: 'EXT:sitepackage/Resources/Public/Css/site-icons.css'
      attributes:
        class: 'site-icon'
        fill: 'currentColor'
  icons:
    - cloud
  categories:
    site:
      label: 'Site'
      icons:
        - cloud
```

Add to `packages/sitepackage/ext_localconf.php`:

```php
<?php

use Quellenform\Iconpack\IconpackRegistry;
use TYPO3\CMS\Core\Utility\ExtensionManagementUtility;
use TYPO3\CMS\Core\Utility\GeneralUtility;

defined('TYPO3') || die();

if (ExtensionManagementUtility::isLoaded('iconpack')) {
    GeneralUtility::makeInstance(IconpackRegistry::class)->registerIconpack(
        'EXT:sitepackage/Configuration/Iconpack/SiteIcons.yaml'
    );
}
```

Declare the required Iconpack dependency in the owning package's `composer.json` as well. The condition only avoids boot failure if an optional dependency is absent; it does not install anything. Registered pack keys must be unique and stable. For this pack an iconfig is `siteicons:cloud`; styled Font Awesome uses `fa7:solid,house`.

Create the actual assets; merely listing `cloud` does not generate them:

`packages/sitepackage/Resources/Public/Icons/Site/cloud.svg`:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path fill="currentColor" d="M6 19a5 5 0 0 1-1-9.9A7 7 0 0 1 18.6 8a5.5 5.5 0 0 1-.1 11H6Z"/>
</svg>
```

`packages/sitepackage/Resources/Public/Icons/site-icons.svg`:

```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <symbol id="cloud" viewBox="0 0 24 24">
    <path fill="currentColor" d="M6 19a5 5 0 0 1-1-9.9A7 7 0 0 1 18.6 8a5.5 5.5 0 0 1-.1 11H6Z"/>
  </symbol>
</svg>
```

`packages/sitepackage/Resources/Public/Css/site-icons.css`:

```css
.site-icon { width: 1em; height: 1em; vertical-align: -0.125em; }
```

No webfont renderer is declared here, so do not select webfont as the only preference for this pack. Backend selection needs icons/categories, not just asset files. [Provider YAML and registration API](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Documentation/Tutorials/CustomIconpack.rst).

## Bridge an installed pack to Core backend identifiers

TYPO3's Core icon identifiers and Iconpack iconfig strings are separate namespaces. For a module, TCA record icon, or wizard item, register a stable Core identifier pointing to an actual installed SVG. On TYPO3 11.4+ use `packages/sitepackage/Configuration/Icons.php`:

```php
<?php

use TYPO3\CMS\Core\Imaging\IconProvider\SvgIconProvider;
use TYPO3\CMS\Core\Imaging\IconProvider\SvgSpriteIconProvider;

return [
    'sitepackage-house' => [
        'provider' => SvgIconProvider::class,
        'source' => 'EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/svgs/solid/house.svg',
    ],
    'sitepackage-cloud' => [
        'provider' => SvgIconProvider::class,
        'source' => 'EXT:sitepackage/Resources/Public/Icons/Site/cloud.svg',
    ],
    'sitepackage-house-sprite' => [
        'provider' => SvgSpriteIconProvider::class,
        'sprite' => 'EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/sprites/solid.svg#house',
    ],
];
```

The Core sprite provider uses **`sprite` including `#symbol-id`**; Iconpack YAML uses **`renderTypes.svgSprite.source` without the fragment**. Verify `house` exists in the installed asset before registering it. The bridge references the provider's asset directly and therefore needs the provider installed even if that pack is hidden in the picker. For an extension reused outside this project, declare its provider dependency or distribute an appropriately licensed owned asset.

Legacy Core registration before TYPO3 11.4 belongs in `ext_localconf.php` instead of `Configuration/Icons.php`:

```php
<?php

use TYPO3\CMS\Core\Imaging\IconProvider\SvgIconProvider;
use TYPO3\CMS\Core\Imaging\IconRegistry;
use TYPO3\CMS\Core\Utility\GeneralUtility;

defined('TYPO3') || die();

GeneralUtility::makeInstance(IconRegistry::class)->registerIcon(
    'sitepackage-house',
    SvgIconProvider::class,
    ['source' => 'EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/svgs/solid/house.svg']
);
```

Do not keep both registration methods for the same identifier. `t3skin-icon` is not a modern T3X Iconpack configuration key. Old skin CSS/sprite names are not automatically mapped to packs. Migrate those references to Core identifiers as above; do not invent a `t3skin-icon` mapping array. The old Core `FontawesomeIconProvider` was removed in TYPO3 12; these examples use SVG providers. [TYPO3 Icon API and migration](https://docs.typo3.org/m/typo3/reference-coreapi/13.4/en-us/ApiOverview/Icon/Index.html).

## Backend module iconIdentifier and legacy ext_tables.php

For an existing TYPO3 12+ module, update its entry in `packages/sitepackage/Configuration/Backend/Modules.php`, preserving its real controller, routes and access rules:

```php
<?php

use Vendor\Sitepackage\Controller\IconModuleController;

return [
    'sitepackage_icons' => [
        'parent' => 'web',
        'access' => 'user',
        'iconIdentifier' => 'sitepackage-house',
        'labels' => [
            'title' => 'Site icons',
            'description' => 'Manage site icons',
            'shortDescription' => 'Site icons',
        ],
        'routes' => [
            '_default' => ['target' => IconModuleController::class . '::handleRequest'],
        ],
    ],
];
```

The example assumes that controller already exists and is registered as a service. Check the target TYPO3's parent module identifier; TYPO3 14 reorganizes backend modules, so retain the existing module's correct parent rather than assuming `web`. [TYPO3 module configuration](https://docs.typo3.org/m/typo3/reference-coreapi/13.4/en-us/ApiOverview/Backend/BackendModules/ModuleConfiguration/Index.html).

For an **existing TYPO3 11 Extbase module**, the historical registration in `packages/sitepackage/ext_tables.php` references the installed SVG with the legacy `icon` option:

```php
<?php

use TYPO3\CMS\Extbase\Utility\ExtensionUtility;
use Vendor\Sitepackage\Controller\IconController;

defined('TYPO3') || die();

ExtensionUtility::registerModule(
    'Sitepackage',
    'web',
    'icons',
    '',
    [IconController::class => 'index'],
    [
        'access' => 'user,group',
        'icon' => 'EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/svgs/solid/house.svg',
        'labels' => 'LLL:EXT:sitepackage/Resources/Private/Language/locallang_mod.xlf',
    ]
);
```

This assumes a working Extbase `indexAction` and module labels file. It is migration guidance, not code for TYPO3 12+. Modern Iconpack does not require setup in `ext_tables.php`; use `ext_localconf.php` for pack registration, `Configuration/Icons.php` for Core icons, and TCA overrides for table changes. [TYPO3 11 registerModule source](https://github.com/TYPO3/typo3/blob/v11.5.41/typo3/sysext/extbase/Classes/Utility/ExtensionUtility.php).

## TCA records, content types and icon picker

For an already registered custom content type `sitepackage_feature`, `packages/sitepackage/Configuration/TCA/Overrides/tt_content.php`:

```php
<?php

use TYPO3\CMS\Core\Utility\ExtensionManagementUtility;

defined('TYPO3') || die();

$GLOBALS['TCA']['tt_content']['ctrl']['typeicon_classes']['sitepackage_feature']
    = 'sitepackage-house';

ExtensionManagementUtility::addTCAcolumns('tt_content', [
    'tx_sitepackage_icon' => [
        'exclude' => true,
        'label' => 'Icon',
        'config' => [
            'type' => 'user',
            'renderType' => 'IconpackWizard',
            'formElementStyle' => 'iconInputButton',
            'buttonIcon' => 'sitepackage-house',
            'buttonLabel' => 'Choose icon',
            'buttonTooltip' => 'Select an icon from an installed pack',
        ],
    ],
]);
ExtensionManagementUtility::addToAllTCAtypes(
    'tt_content',
    'tx_sitepackage_icon',
    'sitepackage_feature',
    'after:header'
);
```

Add storage for the user-type field in `packages/sitepackage/ext_tables.sql` if it does not already exist:

```sql
CREATE TABLE tt_content (
    tx_sitepackage_icon varchar(255) DEFAULT '' NOT NULL
);
```

Run the project's schema setup/database analyzer. The picker stores an iconfig string, not SVG or a Core identifier. Honor editor field permissions (`exclude`) and existing type registration. For a custom table with no type discriminator, its TCA `ctrl.typeicon_classes.default` can point to `sitepackage-house`. New content element wizard Page TSconfig can likewise use `iconIdentifier = sitepackage-house` where that TYPO3 version supports the wizard configuration; the TCA icon is the durable base. [Iconpack TCA renderer](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Configuration/TCA/Overrides/tt_content.php).

## Fluid and PHP rendering

An Iconpack template, for example `packages/sitepackage/Resources/Private/Partials/Icons/House.html`:

```html
{namespace i=Quellenform\Iconpack\ViewHelpers}
<i:icon iconfig="fa7:solid,house"
        preferredRenderTypes="svgInline,svgSprite,webfont"
        additionalAttributes="{class: 'navigation-icon', 'aria-hidden': 'true'}" />
<span>Home</span>
<i:icon iconfig="{data.tx_sitepackage_icon}" />
<i:icon iconfig="siteicons:cloud" />
```

XML namespace alternative:

```html
<html xmlns:i="http://typo3.org/ns/Quellenform/Iconpack/ViewHelpers"
      data-namespace-typo3-fluid="true">
  <i:icon iconfig="fa7:brands,github" />
</html>
```

A Core backend template uses the separately registered identifier:

```html
{namespace core=TYPO3\CMS\Core\ViewHelpers}
<core:icon identifier="sitepackage-house" size="small" />
```

The Iconpack ViewHelper arguments in this release are `iconfig`, `additionalAttributes`, and `preferredRenderTypes`. Put styles inside `additionalAttributes`, not a nonexistent standalone `style` argument. Meaningful icons need nearby text or suitable accessible labels; hide decorative icons from assistive technology. [ViewHelper signature](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Classes/ViewHelpers/IconViewHelper.php).

Equivalent PHP inside a bootstrapped controller/service:

```php
$factory = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(
    \Quellenform\Iconpack\IconpackFactory::class
);
$markup = $factory->getIconMarkup(
    'fa7:solid,house',
    'native',
    ['aria-hidden' => 'true'],
    'svgInline,svgSprite,webfont'
);
```

Use dependency injection where the project already does so. Never instantiate the factory in a bare CLI file without TYPO3 bootstrap.

## CSS, webfonts and SVG sprites

Prefer automatic CSS inclusion (`autoAddAssets = 1`) and Iconpack rendering. Core backend SVG icons need no Font Awesome webfont CSS. If manual frontend loading is needed, put this in the active site-package setup:

```typoscript
page.includeCSS {
  iconpackBase = EXT:iconpack/Resources/Public/Css/Iconpack.min.css
  faCore = EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/css/fontawesome.min.css
  faSolid = EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/css/solid.min.css
  faRegular = EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/css/regular.min.css
  faBrands = EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/css/brands.min.css
}
```

Load only used styles. Font files are relative to those CSS files under `../webfonts/`; keep the shipped directory structure. If a ViewHelper forces `webfont` while the global preference selects SVG, explicitly include the font CSS instead of assuming the automatic collector follows that per-call preference.

A frontend plugin can register CSS from its Fluid template:

```html
<f:asset.css identifier="site-fa-core"
             href="EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/css/fontawesome.min.css" />
<f:asset.css identifier="site-fa-solid"
             href="EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/css/solid.min.css" />
```

For a backend module, add styles to its PageRenderer before rendering the existing ModuleTemplate:

```php
$pageRenderer = \TYPO3\CMS\Core\Utility\GeneralUtility::makeInstance(
    \TYPO3\CMS\Core\Page\PageRenderer::class
);
$pageRenderer->addCssFile('EXT:iconpack/Resources/Public/Css/Iconpack.min.css');
$pageRenderer->addCssFile('EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/css/fontawesome.min.css');
$pageRenderer->addCssFile('EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/css/solid.min.css');
```

Provider CSS normally reaches the backend through Iconpack's renderer hook too; add manually when the module's rendering bypasses it or needs a different font style. Avoid including the same file twice.

An SVG sprite is referenced by `<use>`; it is not included as a stylesheet or JavaScript file. Normally let `<i:icon preferredRenderTypes="svgSprite" ... />` build it. For a controlled direct reference in a backend or frontend Fluid template:

```html
<svg width="1em" height="1em" aria-hidden="true" viewBox="0 0 512 512">
  <use href="{f:uri.resource(path: 'Public/Vendor/fa7/sprites/solid.svg', extensionName: 'IconpackFontawesome')}#house" />
</svg>
```

The viewBox above matches the baseline `house` icon; take other symbols' viewBox from their actual asset. Keep sprite requests on the site's origin and confirm the symbol exists. `f:uri.resource`, `EXT:` and TYPO3 asset APIs resolve `public/_assets/<hash>/...` in modern Composer installations; never hard-code the hash. [TYPO3 asset handling](https://docs.typo3.org/m/typo3/tutorial-sitepackage/main/en-us/Assets/Index.html).

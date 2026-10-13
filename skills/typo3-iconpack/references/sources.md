# Verified sources and compatibility baseline

Checked on **2026-10-12**. Package examples were verified against the released source tags below, not inferred from extension names or an older manual. Consult the installed source and version-specific TYPO3 documentation when changing releases.

| Component | Verified baseline | Source revision |
| --- | --- | --- |
| Iconpack extension | 1.5.5 | `2e2ce0956461df30ee390eb338917504dda4e31e` |
| Font Awesome provider | 1.3.1 | `51b67dbcc511735f684350cd120258b32c9f358b` |
| Bundled Font Awesome assets | 7.1.0 by default; 6.7.2 and 5.15.4 selectable | Provider YAML and `ext_conf_template.txt` in 1.3.1 |
| TYPO3 example API | Modern 12–14 branches; detailed Core examples checked against 13.4 docs | Check target major for module parents, CLI and asset publication |
| Legacy Extbase module registration | TYPO3 11.5.41 source | `ExtensionUtility::registerModule()`; migration guidance only |

## Iconpack primary sources

- [Composer manifest](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/composer.json): package name, extension key and dependency constraints.
- [Extension settings](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/ext_conf_template.txt): exact keys/defaults.
- [Boot configuration](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/ext_localconf.php): FormEngine registration, caching, sanitizer, older persistence XCLASS and backend asset hook.
- [Registry](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Classes/IconpackRegistry.php): PHP registration arguments, duplicate-key handling and shallow override merge.
- [Provider model](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Classes/Domain/Model/IconpackProvider.php): render preferences, styles and `rteSvg` behavior.
- [Factory](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Classes/IconpackFactory.php): iconfig rendering, preferences and scoped asset queries.
- [TypoScript setup](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Configuration/TypoScript/setup.typoscript) and [constants](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Configuration/TypoScript/constants.typoscript): frontend integration and CSS defaults.
- [Site set](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Configuration/Sets/Iconpack/config.yaml): actual set name `quellenform/iconpack`.
- [Custom pack documentation](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Documentation/Tutorials/CustomIconpack.rst): pack YAML schema, categories and registration.
- [ViewHelper implementation](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Classes/ViewHelpers/IconViewHelper.php): actual arguments; no standalone `style` argument.
- [Asset hook](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Classes/Hooks/AssetRenderer.php): automatic frontend/backend CSS loading.
- [CKEditor 5 YAML](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Configuration/RTE/IconpackConfig-v12.yaml) and [module mapping](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Configuration/JavaScriptModules.php): exact import module, export and toolbar item.
- [CKEditor plugin](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Build/Sources/TypeScript/v12/CKEditor/plugin.ts): schema, conversion, button definition and command.
- [Page TSconfig](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Configuration/page.tsconfig): retained span attributes, including `data-iconfig`.
- [Persistence parser](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Classes/Html/IconpackHtmlParser.php), [newer persistence listener](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Classes/EventListener/IconpackBeforeTransformTextForPersistence.php), and [RTE processor](https://github.com/quellenform/t3x-iconpack/blob/1.5.5/Classes/DataProcessing/IconpackProcessor.php): stored placeholders and reconstructed markup.

## Font Awesome provider primary sources

- [Composer manifest](https://github.com/quellenform/t3x-iconpack-fontawesome/blob/1.3.1/composer.json): package/extension names and required Iconpack version.
- [Provider settings](https://github.com/quellenform/t3x-iconpack-fontawesome/blob/1.3.1/ext_conf_template.txt) and [registration](https://github.com/quellenform/t3x-iconpack-fontawesome/blob/1.3.1/ext_localconf.php): version selection, configFile and automatic registration.
- [FontAwesome7.yaml](https://github.com/quellenform/t3x-iconpack-fontawesome/blob/1.3.1/Configuration/Iconpack/FontAwesome7.yaml): `fa7`, `fa5/fa6` replacements, style names, metadata and exact asset paths.
- [Provider preprocessor](https://github.com/quellenform/t3x-iconpack-fontawesome/blob/1.3.1/Classes/Configuration/IconpackConfiguration.php): nonempty extension `stylesEnabled` overrides YAML.
- [House SVG asset](https://github.com/quellenform/t3x-iconpack-fontawesome/blob/1.3.1/Resources/Public/Vendor/fa7/svgs/solid/house.svg): confirmed path and `viewBox="0 0 512 512"`.

## TYPO3 primary documentation and source

- [Core Icon API, 13.4](https://docs.typo3.org/m/typo3/reference-coreapi/13.4/en-us/ApiOverview/Icon/Index.html): Core identifiers, `Icons.php`, SVG/sprite providers and removed Fontawesome provider.
- [Backend module configuration, 13.4](https://docs.typo3.org/m/typo3/reference-coreapi/13.4/en-us/ApiOverview/Backend/BackendModules/ModuleConfiguration/Index.html): modern `iconIdentifier` and routes.
- [TYPO3 11 Extbase utility](https://github.com/TYPO3/typo3/blob/v11.5.41/typo3/sysext/extbase/Classes/Utility/ExtensionUtility.php): legacy `ext_tables.php` registration signature.
- [Project directory layout, 13.4](https://docs.typo3.org/m/typo3/reference-coreapi/13.4/en-us/Administration/DirectoryStructure/Index.html): config, var/log, cache and generated public assets.
- [Assets in site packages](https://docs.typo3.org/m/typo3/tutorial-sitepackage/main/en-us/Assets/Index.html): public resources and TYPO3 URL resolution.
- [Default CKEditor preset, 13.4.19](https://github.com/TYPO3/typo3/blob/v13.4.19/typo3/sysext/rte_ckeditor/Configuration/RTE/Default.yaml): default imports and toolbar baseline.
- [Current extension installation guide](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Administration/ExtensionManagement/Composer/Index.html): Composer and extension setup workflow; check installed CLI availability for older versions.

## Reverification and limits

Read the project's lockfile first. Check changes to registration signatures, extension keys/settings, YAML merge semantics, pack keys/styles/replacements, CKEditor module names, persistence events/XCLASS, sanitizer and asset publication. Treat provider assets and Core backend identifier registration as separate integrations.

`rteSvg` adds SVG render choices to backend RTE defaults; an explicit provider `preferredRenderTypes.backend.rte` overrides those defaults. Use a webfont-only preference when webfont output is required; `rteSvg = 0` is not a security boundary against explicit YAML overrides.

Source/API and structural checks were feasible in this plugin repository. It contains no running TYPO3 site, database or editor session. A real installation, client discovery, asset HTTP behavior and RTE save/reopen/frontend round trip must be verified when using the skill. Evaluation prompts are maintainer scenarios, not a claim that isolated agent benchmarks have run.

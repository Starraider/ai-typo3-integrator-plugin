# TYPO3 v14 project-template options

This reference is for choosing and assembling the initializer payload. TYPO3's documentation calls a full quick-start package a **distribution**: an extension enriched with data/actions that install a ready-to-explore site. The official Introduction Package is the canonical example; it provides a page tree and content and depends on a package that supplies the frontend theme.

## Delivery models

| Model | Include | Installation | Use it when |
| --- | --- | --- | --- |
| Repository template | Root `composer.json`/lock, local packages, DDEV, CI, deployment, config, documentation | Clone/use-template, then Composer install | Deployment and developer environment are part of the reusable product |
| Distribution extension | A thin package plus dependencies, initial data, optional EM images | Composer require + `extension:setup`; optionally Extension Manager | Consumers need an Introduction Package-style quick start |
| Sitepackage demo payload | Sitepackage code plus `Initialisation/` | Require sitepackage + `extension:setup` | The theme/site configuration itself is the reusable unit |

Combining the first and third is common: the repository template owns infrastructure while the sitepackage owns TYPO3-specific assets and demo content. A separate distribution extension is valuable when the same sitepackage should be consumable both with and without demo data.

## What belongs where

| Artifact | Location | Behavior and boundary |
| --- | --- | --- |
| Page tree, content elements, records, relations | `Initialisation/data.xml` | Export from the root page through the Export module. Exclude users/logs and unrelated records. |
| Images/media referenced by exported FAL relations | `Initialisation/data.xml.files/` | Export with files in a folder beside the XML. Keep only the FAL assets the export references. |
| Editor-facing files not referenced by exported records | `Initialisation/Files/` | Copied to `fileadmin/<extension-key>/`; suitable for files such as form YAML. |
| Basic site configuration | `Initialisation/Site/<site-identifier>/config.yaml` | Copied to `config/sites/<site-identifier>/config.yaml` if that identifier does not already exist. |
| Site settings, route enhancers, language and site configuration | Site YAML, normally alongside `config.yaml` when needed | Include only when the starter site requires them; use an unambiguous site identifier. |
| TypoScript, Site Sets, Page TSconfig, TCA, PHP, Fluid, Content Blocks, CSS/JS, source logos | Sitepackage `Configuration/`, `Resources/`, `ContentBlocks/`, `Classes/` | Version-controlled implementation; not `fileadmin/`. |
| Composer/runtime dependencies | Root or extension `composer.json` | Use `require` for required packages; keep local sitepackages in a Composer path repository during development. |
| Extension configuration or system configuration | Explicit documented deployment configuration | Avoid copying production `config/system/settings.php`; it is instance-wide and may hold installation-specific state. |
| Optional custom code after activation | Service listener for `PackageInitializationEvent` | Use only for an idempotent action that data/files/config cannot model. |
| Legacy additional packaged extensions | `Initialisation/Extensions/` | Historic distribution option for dependencies unavailable normally; prefer Composer dependencies in a v14 Composer project. It does not overwrite an already installed extension. |
| Extension Manager artwork | `Resources/Public/Images/Distribution.png` and `DistributionWelcome.png` | Optional only for an EM-distributed distribution. |

## Export and import rules

1. Start with an intentionally clean source instance whose active extensions exactly match the target template.
2. In the Export module, right-click the intended root page and select **More Options > Export**. Include all required tables and relations but no static relations.
3. Inspect the calculated records before export. Exclude `be_users`, `sys_log`, temporary `fileadmin` exports, and data outside template scope.
4. In advanced options, select the setting that writes referenced files to a folder beside the export. Save the XML as `data.xml`, and preserve the generated `data.xml.files/` directory.
5. Save the export preset so that later revisions are reproducible. Regenerate the export whenever page records or FAL file references change.

The Core documentation notes a `data.xml` size limitation of 10 MB. When this applies, use the documented `data.t3d` fallback and explain the compatibility choice in the template documentation.

## Site configuration minimum

The `Initialisation/Site/<identifier>/config.yaml` file should at least declare `base`, the default language, `rootPageId`, and `websiteTitle`. If the sitepackage exposes a Site Set, list its Composer package name in `dependencies`:

```yaml
base: '/'
dependencies:
  - acme/example-sitepackage
languages:
  - title: English
    enabled: true
    languageId: 0
    base: /
    locale: en_US.UTF-8
rootPageId: 1
websiteTitle: 'Example site'
```

The identifier is a filesystem path component and must be unique per TYPO3 installation. Core leaves an existing identifier untouched; installation docs should tell users whether to use a new identifier, delete a disposable local configuration, or adapt the configuration manually.

## Initialization lifecycle

`vendor/bin/typo3 extension:setup` handles extension setup across the installation, including activation-related initialization, schema work where required, and cache clearing. `PackageInitializationEvent` is dispatched on package activation (including Composer-mode requiring) and extension setup. A listener can be ordered before/after Core listeners, including `ImportExtensionDataOnPackageInitialization`, and stores its outcome on the event.

Use a listener only when a declarative payload cannot express the need. It must check the extension key, be safe if called twice, leave unrelated projects intact, and never silently provision remote accounts or process secrets. Declare it as a regular TYPO3 service with `#[AsEventListener]`; use `after: ImportExtensionDataOnPackageInitialization::class` only if it consumes imported data.

## Source material

- [Creating a new distribution — TYPO3 Explained](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ExtensionArchitecture/HowTo/CreateNewDistribution.html): distribution concept, exports, `Initialisation/Files`, site config, testing.
- [Project templates for a quick start](https://docs.typo3.org/m/typo3/tutorial-getting-started/main/en-us/ProjectTemplates/Index.html): Introduction Package and official GitLab template options.
- [Introduction Package](https://docs.typo3.org/m/typo3/tutorial-getting-started/main/en-us/ProjectTemplates/IntroductionPackage/Index.html): Composer installation and starter page tree.
- [Create initial pages — Site Package Tutorial](https://docs.typo3.org/m/typo3/tutorial-sitepackage/14.3/en-us/CreatePages/Index.html): sitepackage `Initialisation/` layout and `extension:setup` flow.
- [PackageInitializationEvent](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Events/Events/Core/Package/PackageInitializationEvent.html): v14 activation event API.
- [Installing extensions](https://docs.typo3.org/m/typo3/tutorial-getting-started/main/en-us/Extensions/InstallingExtensions.html): Composer local packages and `extension:setup`.

Check the v14 docs at execution time when behavior is version-sensitive; the distribution documentation has historical Extension Manager guidance that should not override Composer or v14 deprecations.

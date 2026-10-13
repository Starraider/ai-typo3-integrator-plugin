# Verification, troubleshooting, and maintenance

Run project-root commands through the project's wrapper, for example `ddev composer` and `ddev exec vendor/bin/typo3`. Examples assume Composer mode and document root `public/`; verify `composer.json.extra.typo3/cms.web-dir` and actual filesystem layout first.

## Acceptance checks

1. `composer show quellenform/t3x-iconpack` and `composer show quellenform/t3x-iconpack-fontawesome` match the intended constraints/lockfile. Check `composer check-platform-reqs` in the runtime environment.
2. The effective `EXTENSIONS.iconpack` and `EXTENSIONS.iconpack_fontawesome` settings point to existing files and a valid selected provider version. Inspect Settings / Configuration if the project exposes that module.
3. The pack is visible in a native `IconpackWizard` field and the RTE picker. For the baseline provider the expected key is `fa7`; a hidden pack remains usable by direct ViewHelper calls.
4. Flush TYPO3 caches with `vendor/bin/typo3 cache:flush`. Reload backend assets, clear relevant browser cache/local storage for Core icon changes, and verify cold and warm requests.
5. Render one native Fluid icon, one Core backend identifier, a styled/brand icon if enabled, and any custom site pack icon. Confirm real asset URLs and the expected SVG symbol or font family.
6. Insert, save, reopen, modify and resave an RTE icon as the intended editor role. Inspect the persistent `data-iconfig` and corresponding frontend markup. The stored span and rendered SVG need not match byte-for-byte.
7. In browser Network, inspect CSS, font, JavaScript module and SVG requests for status/content type, redirects and CSP errors. In console, inspect module/toolbar failures. Confirm a sprite's `<symbol id>` matches the fragment.
8. Confirm provider/source assets are readable by the webserver, symlink targets are reachable, and TYPO3's configured cache/log/temp directories are writable by the correct runtime user.

These checks establish the actual integration; Composer installation or linting alone does not.

## Commands and locations to inspect

```bash
composer validate --strict
composer check-platform-reqs
composer show quellenform/t3x-iconpack --path
composer show quellenform/t3x-iconpack-fontawesome --path
vendor/bin/typo3 cache:flush
ls -ld public/_assets public/typo3temp var/cache var/log
rg --files -L vendor/quellenform/t3x-iconpack vendor/quellenform/t3x-iconpack-fontawesome
rg -n 'iconpack|parseFunc_RTE|nonTypoTagUserFunc|site_icons' packages config
rg -n -i 'iconpack|permission denied|failed to open|exception' var/log --glob '*.log'
```

Only run commands for paths that exist. `rg --files -L` follows Composer symlinks. Logs may contain sensitive request data; quote only the relevant sanitized error. Use the installed provider's `Configuration/Iconpack/FontAwesome7.yaml`, `ext_conf_template.txt` and `ext_localconf.php` to resolve paths, rather than guessing from outdated documentation.

| Typical modern Composer path | Purpose |
| --- | --- |
| `composer.json`, `composer.lock` | Requirements, selected versions and dependency resolution |
| `config/system/settings.php`, `config/system/additional.php` | Effective extension configuration and site-local overrides |
| `config/sites/<site-identifier>/config.yaml` | Active site-set dependencies |
| `packages/sitepackage/Configuration/Iconpack/*.yaml` | Project pack definitions and merge overrides |
| `packages/sitepackage/Configuration/RTE/*.yaml` | RTE preset and plugin/toolbar/content CSS |
| `packages/sitepackage/Configuration/page.tsconfig` | Preset assignment and processing overrides |
| `vendor/quellenform/t3x-iconpack/` | Installed registry and renderer source; inspect without editing |
| `vendor/quellenform/t3x-iconpack-fontawesome/` | Installed pack YAML and bundled assets |
| `public/_assets/<generated-hash>/` | Published/symlinked `Resources/Public/` assets; use APIs to reference |
| `public/typo3temp/assets/` | Generated public CSS/JS/assets where present |
| `var/cache/` | Private cache data/code in typical Composer installations |
| `var/log/typo3_*.log` | Application exceptions and logs; actual writers/filenames can differ |

Older/classic installations use `typo3conf/LocalConfiguration.php`, `AdditionalConfiguration.php`, and `typo3temp/var/cache/` or `typo3temp/var/log/`, relative to their document root. Custom web/var directories may differ. Also inspect the backend Log module (menu label/version varies), PHP-FPM logs and webserver error/access logs. Do not assume every HTTP 404 is in TYPO3's application log. [TYPO3 directory layout](https://docs.typo3.org/m/typo3/reference-coreapi/13.4/en-us/Administration/DirectoryStructure/Index.html).

## Fixes by symptom

### Pack missing or duplicate key

Confirm the provider package is installed and boots, `version` selects an existing YAML, `configFile` is empty or resolves to a real file, and `hidden` is false. Check valid styles and custom icon/category lists. If the registry reports a key already registered, remove the site's duplicate registration of the automatically registered provider; retain registration for custom packs with unique keys. Flush the `iconpack` cache through the normal cache API/maintenance flush after changing definitions; do not delete unrelated cached data.

### CSS missing or webfont square glyphs

Check the chosen renderer first: SVG output should not require webfont CSS. For webfont output, verify `autoAddAssets = 1` and the frontend hook is reached, or explicitly include the provider's core CSS plus used style CSS. Inspect `@font-face`, computed font family/weight and the font request in browser Network. A per-call webfont preference may require explicit CSS because automatic collection uses configured render preferences.

Baseline manual fix in active setup:

```typoscript
page.includeCSS.faCore = EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/css/fontawesome.min.css
page.includeCSS.faSolid = EXT:iconpack_fontawesome/Resources/Public/Vendor/fa7/css/solid.min.css
```

Check the linked `../webfonts/` files remain in place and the root-template/site-set configuration is actually loaded. Keep CSS and fonts from the same bundled version; do not mix `fa5`, `fa6` and `fa7` directories.

### SVG sprite or backend JavaScript returns 404

Inspect the generated URL and its target, then confirm the installed file and symbol:

```bash
test -r vendor/quellenform/t3x-iconpack-fontawesome/Resources/Public/Vendor/fa7/sprites/solid.svg
rg -o 'id="house"' vendor/quellenform/t3x-iconpack-fontawesome/Resources/Public/Vendor/fa7/sprites/solid.svg
ls -la public/_assets
composer dump-autoload
vendor/bin/typo3 cache:flush
```

For an HTTP check, replace the host and hash with the **observed** URL (not a hard-coded configuration path):

```bash
curl -I 'https://example.test/_assets/OBSERVED_HASH/Vendor/fa7/sprites/solid.svg'
```

Regenerate Composer-managed publication after adding a new `Resources/Public/` directory or moving deployment paths; don't create ad hoc `_assets` links. If that TYPO3 version/deployment uses `asset:publish`, inspect `vendor/bin/typo3 help asset:publish` and use the documented project procedure. Check webroot configuration, symlink support and rewrite rules. Deploy the provider assets, not just PHP/YAML. A 200 response with an HTML login/404 body is still wrong: inspect Content-Type and response body. CSS cannot repair an absent sprite symbol.

### Permission denied / unreadable files

Inspect the actual source asset and each ancestor directory. Example on Linux (replace `www-data` with the actual webserver user):

```bash
ls -ld vendor/quellenform vendor/quellenform/t3x-iconpack-fontawesome/Resources/Public/Vendor/fa7
ls -l vendor/quellenform/t3x-iconpack-fontawesome/Resources/Public/Vendor/fa7/sprites/solid.svg
sudo -u www-data test -r vendor/quellenform/t3x-iconpack-fontawesome/Resources/Public/Vendor/fa7/sprites/solid.svg
```

Fix the deployment process or the offending file/directory according to its owner/group model. A narrow example for an intentionally world-readable public asset is:

```bash
chmod 0644 vendor/quellenform/t3x-iconpack-fontawesome/Resources/Public/Vendor/fa7/sprites/solid.svg
```

An appropriate public directory normally needs traversal permission (often `0755`); private writable directories often use a shared deployment/webserver group instead. Apply fixes only to diagnosed paths and persist the intended ownership in deployment. Avoid whole-tree chmod/chown or giving the webserver write access to all code. Never use `777`.

### Iconpack button missing / module import failure

Confirm TYPO3 12+ uses `IconpackConfig-v12.yaml`, `@quellenform/iconpack-ckeditor.js` exports `Iconpack`, and the toolbar contains `Iconpack`. Select automatic or manual setup; inspect duplicates and preset overrides. Clear compiled container/cache after dependency changes and hard-reload backend JS. Inspect the browser console for missing import-map entries or blocked modules. For TYPO3 10/11 use the extension's legacy CKEditor 4 preset instead.

### Icon disappears after save or on the frontend

Determine where it disappears: editor schema, stored HTML, parsing/transformation, sanitizer, or CSS. Inspect whether the saved field retains `data-iconfig` and whether the persistence listener/XCLASS and Page TSconfig span rule are loaded. If persistence succeeds but frontend output fails, inspect final `lib.parseFunc_RTE.nonTypoTagUserFunc` and the active preset/render preferences. Review custom XCLASS or sanitizer conflicts. Add only the needed attributes/elements at the actual filtering stage; don't disable all processing or render stored HTML raw.

### CSP blocks fonts or SVG / broken cross-origin sprites

Inspect the console's exact policy directive and asset URL. Prefer the shipped same-origin files. Change only the relevant configured policy after understanding the asset need; do not add blanket wildcards or inline-script permissions for icons. Check proxy/CDN base-path handling and whether a sprite is being requested from another origin.

## Pinning, backup, upgrade, and rollback

Example root manifest fragment (merge into existing requirements):

```json
{
  "require": {
    "quellenform/t3x-iconpack": "~1.5.5",
    "quellenform/t3x-iconpack-fontawesome": "~1.3.1"
  }
}
```

These allow patch updates within the verified minor line. Exact pins such as `1.5.5` and `1.3.1` are appropriate when project policy requires them. Always commit `composer.lock`; deploy with `composer install`, not a production `composer update`. Reassess available patches/security notices at upgrade time.

Before upgrading, snapshot the database, uploaded/FAL files (including external storage), current code, `composer.json`/lockfile, system/site config, RTE presets, pack YAML, and representative stored content. Verify backups can be restored and keep them outside the public webroot. A local DDEV example:

```bash
umask 077
mkdir -p .backups/iconpack-before-upgrade
ddev export-db --file=.backups/iconpack-before-upgrade/database.sql.gz
cp composer.json composer.lock .backups/iconpack-before-upgrade/
tar -czf .backups/iconpack-before-upgrade/site-files.tar.gz packages config public/fileadmin
```

Adapt existing paths/storage and large-file backup tooling; `public/fileadmin` does not cover external FAL storage. Exclude private backup directories from Git and public publication.

On a development/staging copy:

```bash
composer outdated quellenform/t3x-iconpack
composer outdated quellenform/t3x-iconpack-fontawesome
composer update quellenform/t3x-iconpack quellenform/t3x-iconpack-fontawesome --with-dependencies --dry-run
composer update quellenform/t3x-iconpack quellenform/t3x-iconpack-fontawesome --with-dependencies
composer check-platform-reqs
vendor/bin/typo3 extension:setup --extension=iconpack
vendor/bin/typo3 extension:setup --extension=iconpack_fontawesome
vendor/bin/typo3 cache:flush
```

If intentionally moving to a new minor/major, first revise requirements on the staging branch using release-specific documentation. Review lockfile changes, TYPO3 compatibility, new bundled asset paths, selected `version`, removed icons, aliases and licenses. Do not change a custom pack's `key` as cleanup. The baseline `fa7` provider declares replacements for `fa5,fa6`; test actual old styled iconfigs and icon aliases rather than assuming every removed name migrates. Retain override structure and the persistence tests.

Deploy the reviewed lockfile and versioned configuration through the normal project procedure. If rollback is needed, restore the previous code/config/manifest/lockfile, run `composer install`, flush caches, and verify old content. Restore the database only when schema/content changes require it and within the user's explicit rollback scope; avoid losing content written since the backup.

## Reusable site-package layout

```text
packages/sitepackage/
├── composer.json
├── ext_localconf.php
├── ext_tables.sql
├── Configuration/
│   ├── Icons.php
│   ├── Iconpack/
│   │   ├── SiteIcons.yaml
│   │   └── FontAwesomeOverrides.yaml
│   ├── RTE/Icons.yaml
│   ├── TCA/Overrides/tt_content.php
│   ├── page.tsconfig
│   └── Sets/Site/
│       ├── config.yaml
│       └── setup.typoscript
└── Resources/
    ├── Private/Partials/Icons/House.html
    └── Public/
        ├── Css/site-icons.css
        └── Icons/
            ├── Site/cloud.svg
            └── site-icons.svg
```

For static-template projects use `Configuration/TypoScript/{constants,setup}.typoscript` instead of set-owned setup. Keep maintained icons and generated sprites in `Resources/Public`, configuration under `Configuration`, and reusable markup in Fluid partials. Preserve stable symbol IDs and pack keys, commit build inputs/tools for generated assets, and preserve licensing notices. Reference shared provider assets through their `EXT:` paths rather than copying unmanaged vendor folders into multiple extensions.

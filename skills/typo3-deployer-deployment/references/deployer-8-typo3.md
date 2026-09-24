# Deployer 8 recipe for TYPO3

Read this file when creating or reviewing a Deployer 8 TYPO3 recipe.

## Runtime requirements

Deployer 8 requires PHP 8.3 or later and Symfony 7.4 or 8.0 components. Install the project-local binary through Composer:

```bash
composer require --dev 'deployer/deployer:^8.0' --with-all-dependencies
```

Use `vendor/bin/dep`, not an unversioned global binary. Commit both Composer files so local runs and GitHub Actions use the same Deployer release.

## Recipe baseline

Start from the bundled TYPO3 recipe:

```php
<?php

declare(strict_types=1);

namespace Deployer;

require 'recipe/typo3.php';

set('repository', 'git@github.com:OWNER/REPOSITORY.git');
set('typo3/public_dir', 'public');
set('keep_releases', 5);

add('shared_files', [
    '.env',
]);

host('production')
    ->set('hostname', 'www.example.org')
    ->set('remote_user', 'deployer')
    ->set('branch', 'main')
    ->set('deploy_path', '/var/www/example');

after('deploy:failed', 'deploy:unlock');
```

Adapt this baseline to the project. Do not copy placeholder values into a live recipe.

The v8 TYPO3 recipe derives the public directory from `composer.json` and otherwise defaults to `public`. Set `typo3/public_dir` only when an explicit value makes the project clearer or the Composer metadata is incomplete. Do not carry `typo3_webroot` forward from the v7 recipe.

## Shared state

The v8 TYPO3 recipe supplies defaults for persistent and writable paths, including `public/fileadmin`, `public/typo3temp/assets`, and TYPO3 runtime paths under `var`. Inspect the installed recipe and the live `shared/` directory before overriding those lists.

- Add `.env` to `shared_files` when TYPO3 reads it from the project root.
- Keep user uploads and generated public assets that must survive a release in `shared_dirs`.
- Keep logs, locks, sessions, and other runtime data outside versioned release directories.
- An empty `shared_dirs` or `writable_dirs` override disables recipe defaults. Preserve it only when the live server layout proves it is intentional.
- Do not share built frontend assets when the project commits or builds a release-specific manifest. Build them before archive creation or as a reviewed release task.

## Source strategy

For an operator's local deployment, the default archive strategy may use the configured repository and target revision. For GitHub Actions, prefer:

```php
set('update_code_strategy', getenv('CI') ? 'local_archive' : 'archive');
```

`local_archive` sends the checkout held by the runner. It avoids a race where CI validates one commit but the server clones a newer branch head. It also removes the need for a server-to-GitHub deploy key. Confirm that required generated files are present before Deployer creates the archive.

If the project deliberately uses `clone`, `archive`, or rsync, document which machine authenticates to GitHub and how the exact revision stays fixed.

## TYPO3 tasks and database changes

The v8 TYPO3 recipe (`recipe/typo3.php`) is based on `recipe/common.php` and defines the complete deployment lifecycle:

1. `deploy:info` – Displays info about deployment
2. `deploy:setup` – Prepares deployment directory structure on host
3. `deploy:lock` – Locks deployment to prevent concurrent runs
4. `deploy:release` – Prepares new release directory
5. `typo3:update_code` – Fetches code via Git or rsync (or `local_archive` in CI)
6. `deploy:shared` – Creates symlinks for shared files and directories
7. `deploy:writable` – Configures permissions on writable directories
8. `deploy:vendors` – Installs Composer packages with production options (`--no-dev --optimize-autoloader`)
9. `typo3:install:fixfolderstructure` – Automatically creates required files and folders for TYPO3
10. `typo3:extension:setup` – Sets up extensions and applies database schema updates
11. `typo3:language:update` – Updates language files for activated extensions
12. `typo3:cache:flush` – Clears all TYPO3 caches
13. `typo3:cache:warmup` – Warms up system caches
14. `deploy:publish` – Atomic symlink swap (`deploy:symlink`), unlocks (`deploy:unlock`), cleans old releases (`deploy:cleanup`), and emits `deploy:success`

Extension setup can mutate the database schema. Before the first production run:

- identify the database backup or snapshot procedure;
- confirm that CLI and web PHP use compatible versions and extensions;
- confirm the web server points to `{{deploy_path}}/current/{{typo3/public_dir}}`;
- verify that the deployment user can write required shared and runtime paths;
- decide whether frontend assets are built in CI, locally, or on the target;
- keep a previous release until the new release and public URL pass checks.

### Ad-hoc TYPO3 commands

Deployer 8 exposes individual TYPO3 maintenance commands:

```bash
vendor/bin/dep typo3:cache:flush <selector>          # Clear all caches
vendor/bin/dep typo3:cache:warmup <selector>         # Warm up system caches
vendor/bin/dep typo3:extension:setup <selector>      # Run schema migration & extension setup
vendor/bin/dep typo3:language:update <selector>      # Update translation files
vendor/bin/dep typo3:install:fixfolderstructure <selector> # Verify folder structure
vendor/bin/dep logs:app <selector>                   # Tail TYPO3 log files (var/log/typo3_*.log)
```

## Deployer 8 modern syntax & features

- **Named arguments:** `run('composer install', timeout: 300, nothrow: true, cwd: '{{release_path}}')`. The v7 `$options` array is removed; `no_throw` is `nothrow`, `real_time_output` is `forceOutput`, and `idle_timeout` is `idleTimeout`.
- **Multiple secrets:** `run('echo %db_pass%', secrets: ['db_pass' => getenv('DB_PASSWORD')])`. Placeholders are securely masked in logs.
- **Quote helper:** Use `quote($arg)` or the template filter `{{ message | quote }}` instead of `escapeshellarg()`.
- **Template escaping:** Output literal `{{` by escaping with a backslash: `run('echo \{{not_interpolated}}')`.
- **Composer version pinning:** Pin remote Composer version with `set('composer_version', '2.7')`.
- **Host shell customization:** `host('prod')->setShellPath('/bin/bash')`.
- **ACL write modes:** Enhanced permissions via `writable_acl_groups` and `writable_acl_force`.
- **MAML recipes:** In addition to PHP and YAML, Deployer 8 supports `deploy.maml` recipes.

## Local validation

These commands load the recipe but must not perform a deployment:

```bash
composer validate --strict --no-check-publish
php -l deploy.php
vendor/bin/dep --version
vendor/bin/dep list
vendor/bin/dep tree deploy
```

Inspect the task tree for project-specific tasks that were previously attached to v7 task names. Verify the chosen selector against the static host or inventory definitions before any remote command.

## Sources

- [Deployer 8 getting started](https://deployer.org/docs/8.x/getting-started)
- [Deployer v8 release overview](https://deployer.org/blog/deployer-v8)
- [Deployer 8 basics](https://deployer.org/docs/8.x/basics)
- [Deployer 8 hosts](https://deployer.org/docs/8.x/hosts)
- [Deployer 8 TYPO3 recipe](https://deployer.org/docs/8.x/recipe/typo3)
- [Deployer 8 update code recipe](https://deployer.org/docs/8.x/recipe/deploy/update_code)

Checked on 2026-09-24.

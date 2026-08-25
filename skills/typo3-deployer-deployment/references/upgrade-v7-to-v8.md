# In-place upgrade from Deployer 7 to 8

Read this file completely when any project evidence points to Deployer 7. The goal is to upgrade the tool and recipe while leaving the remote release structure and shared state intact.

## Detection

Run the read-only inspector first:

```bash
php scripts/inspect-deployer.php --project-root . --format text
```

It checks the direct Composer constraint, locked package, local binary, PHP runtime, recipe files, and common v7 code patterns. Composer lock data is stronger evidence than a broad constraint. If the constraint, lock, and binary disagree, classify the project as mixed and resolve that mismatch before editing the recipe.

Typical v7 evidence includes:

- `deployer/deployer` constrained to `^7` or an exact `7.x` version;
- `composer.lock` containing `deployer/deployer` version `v7.x`;
- `vendor/bin/dep --version` reporting major version 7;
- TYPO3 recipe configuration such as `typo3_webroot`;
- old `run()` option arrays or renamed parameters.

## Preconditions

Stop before changing Composer files when any of these conditions holds:

- CLI PHP is below 8.3.
- Composer reports a package that prevents Deployer 8 or its Symfony requirements.
- the project has uncommitted changes that overlap `composer.json`, `composer.lock`, or the recipe and cannot be preserved safely;
- the deployment recipe is generated from another source that has not been found;
- the live `deploy_path`, shared layout, or current symlink is unknown.

Use Composer's explanation before forcing dependencies:

```bash
composer prohibits deployer/deployer '^8.0'
```

Deployer 8 requires Symfony 7.4 or 8.0 components. Do not solve a dependency conflict by removing application packages without separate authorization.

## Package upgrade

Preview the operation:

```bash
scripts/upgrade-deployer-v8.sh --project-root .
```

Apply the Composer update:

```bash
scripts/upgrade-deployer-v8.sh --project-root . --apply
```

The script only accepts a detected v7 or mixed installation. It backs up the Composer files to a temporary directory, runs `composer require` with all dependency updates allowed, verifies that the lock resolves major version 8, and restores the original Composer files if Composer fails. It does not rewrite PHP recipe logic.

## Recipe migration

Patch each applicable breaking change by meaning:

| Deployer 7 pattern | Deployer 8 form |
| --- | --- |
| `run('cmd', ['timeout' => 5, 'no_throw' => true])` | `run('cmd', timeout: 5, nothrow: true)` |
| `no_throw` | `nothrow` |
| `real_time_output` | `forceOutput` |
| `idle_timeout` | `idleTimeout` |
| `secret: $value` and `%secret%` | `secrets: ['name' => $value]` and `%name%` |
| `escapeshellarg($value)` inside commands | Deployer's `quote($value)` |
| literal `{{` in a command | escape it as `\{{` |
| `Httpie::send()` treated as a string | call `->send()->body()` when the body is needed |
| `Httpie::getJson()` | `sendJson()` |
| self-update tasks or instructions | remove them and manage Deployer through Composer |

Review custom wrappers around `run()` and `runLocally()`. A simple text replacement cannot reliably distinguish option arrays from normal PHP arguments. The inspector reports candidate lines, but the agent must read the surrounding task.

For TYPO3 recipes:

- replace `typo3_webroot` with `typo3/public_dir` when the override is still needed;
- treat `web_path` and `public_path` as project-specific until their readers are found, then remove only obsolete values;
- compare `shared_files`, `shared_dirs`, and `writable_dirs` with Deployer 8's TYPO3 defaults;
- remove empty overrides unless the live layout proves that disabling the defaults is intentional;
- inspect hooks attached to `deploy:prepare`, update-code tasks, extension setup, and publish tasks against the v8 task tree;
- consider `local_archive` for CI so the checked-out revision becomes the deployed source.

Do not run `dep init`. It can replace the recipe and lose host aliases, custom tasks, shared state, or hooks.

## Release continuity

The v7 to v8 guide does not require a release-number migration like the older v6 to v7 transition. Keep these remote paths untouched during the tool upgrade:

- `{{deploy_path}}/current`
- `{{deploy_path}}/shared`
- `{{deploy_path}}/releases`
- `{{deploy_path}}/.dep`

Do not delete releases to make a test pass. Keep the same `deploy_path` and verify that the current symlink points to the expected pre-upgrade release before the first v8 deployment.

## Verification gate

After editing, require all applicable checks:

```bash
composer validate --strict --no-check-publish
php -l deploy.php
vendor/bin/dep --version
vendor/bin/dep list
vendor/bin/dep tree deploy
php scripts/inspect-deployer.php --project-root . --format text
```

The version must be 8.x. No high-severity v7 recipe finding may remain. Review informational TYPO3 findings rather than suppressing them blindly.

The first production deployment is a separate authorized operation. Record the previous release, database backup state, selected revision, and rollback command before running it.

## Sources

- [Official Deployer major-version upgrade guide](https://github.com/deployphp/deployer/blob/master/docs/UPGRADE.md)
- [Deployer 8 TYPO3 recipe](https://deployer.org/docs/8.x/recipe/typo3)

Checked on 2026-08-25.

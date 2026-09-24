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

| Deployer 7 pattern | Deployer 8 form | Notes |
| --- | --- | --- |
| `run('cmd', ['timeout' => 5, 'no_throw' => true])` | `run('cmd', timeout: 5, nothrow: true)` | Named arguments replace `$options` array |
| `no_throw` | `nothrow` | Renamed parameter |
| `real_time_output` | `forceOutput` | Renamed parameter |
| `idle_timeout` | `idleTimeout` | Renamed parameter |
| `cd('{{release_path}}'); run('cmd');` | `run('cmd', cwd: '{{release_path}}')` | New `cwd` parameter avoids manual `cd()` |
| `secret: $value` and `%secret%` | `secrets: ['name' => $value]` and `%name%` | Supports multiple named secrets |
| `escapeshellarg($value)` inside commands | Deployer's `quote($value)` | Safer ANSI-C `$'...'` quoting |
| Template string escaping | `{{ message \| quote }}` | Built-in quote filter for template strings |
| Literal `{{` in commands or templates | Escape as `\{{` | Prevents unintended config interpolation |
| `Httpie::send()` treated as a string | call `->send()->body()` | Returns an `HttpResponse` with `status()`, `header()`, `body()` |
| `Httpie::getJson()` | `sendJson()` | `getJson()` is deprecated |
| `Httpie` fluent methods | In-place mutation (no clone) | Methods mutate and return `$this` |
| self-update tasks or instructions | remove them | `self-update` command removed; manage via Composer |
| YAML recipes with imprecise error locations | `deploy.maml` | MAML format supported alongside PHP and YAML |
| Remote Composer version pinning | `set('composer_version', '2.7')` | Enforces exact Composer version on target host |
| Host shell configuration | `Host::setShellPath('/bin/bash')` | Customizes shell executable per host |
| ACL write permissions | `writable_acl_groups`, `writable_acl_force` | Enhanced multi-group and reset support |

Review custom wrappers around `run()` and `runLocally()`. A simple text replacement cannot reliably distinguish option arrays from normal PHP arguments. The inspector reports candidate lines, but the agent must read the surrounding task.

For TYPO3 recipes:

- replace `typo3_webroot` with `typo3/public_dir` when the override is still needed (in Deployer 8, `typo3/public_dir` is automatically detected from `composer.json` or defaults to `public`);
- treat `web_path` and `public_path` as project-specific until their readers are found, then remove only obsolete values;
- compare `shared_files`, `shared_dirs`, and `writable_dirs` with Deployer 8's TYPO3 defaults;
- remove empty overrides unless the live layout proves that disabling the defaults is intentional;
- inspect hooks attached to `deploy:prepare`, update-code tasks, extension setup, and publish tasks against the v8 task tree;
- configure `update_code_strategy` to `local_archive` in CI so the checked-out revision becomes the deployed source.

Do not run `dep init`. It can replace the recipe and lose host aliases, custom tasks, shared state, or hooks.

## Upgrading a Deployer v7 CI/CD pipeline to v8

When a repository runs Deployer from GitHub Actions, GitLab CI, or Bitbucket Pipelines, upgrading the pipeline is as critical as upgrading the PHP recipe. Deployer 8 changes execution requirements, update strategies, and command options.

### Pipeline breaking changes and behavioral shifts

1. **Runner PHP runtime must be 8.3 or higher:**
   Deployer 7 pipelines frequently ran on PHP 8.0, 8.1, or 8.2 runners. Deployer 8 strictly requires PHP >= 8.3. A CI runner running an older PHP version will fail during Composer install or syntax execution.
   - *GitHub Actions:* Update `shivammathur/setup-php` to `php-version: '8.3'` (or `'8.4'`).
   - *GitLab CI / Docker:* Update container image from `php:8.1-cli` or `php:8.2-cli` to `php:8.3-cli`.

2. **Self-update is removed:**
   Deployer 7 workflows often included `dep self-update` or `vendor/bin/dep self-update`. In Deployer 8, `self-update` has been completely removed. Running it causes a fatal CLI command error. Remove this step and manage Deployer deterministically through Composer `require-dev`.

3. **Global phar downloads should be replaced by `vendor/bin/dep`:**
   Many v7 pipelines downloaded Deployer on the fly via `curl -LO https://deployer.org/deployer.phar`. In v8, rely on `composer install` installing `deployer/deployer:^8.0` into `vendor/bin/dep`. This guarantees the CI runner runs the exact version pinned in `composer.lock`.

4. **Adopt `local_archive` update strategy:**
   - *Deployer 7 behavior:* Deployer typically executed `deploy:update_code` by performing `git clone` or `git archive` on the *remote target server*. This required placing GitHub/GitLab deployment keys on the remote production server, using SSH agent forwarding, or managing tokens.
   - *Deployer 8 behavior:* Set `set('update_code_strategy', getenv('CI') ? 'local_archive' : 'archive');`. In CI, Deployer builds a tarball from the runner's current checked-out Git workspace and uploads it directly to the remote release folder via SSH.
   - *Benefits:*
     - Eliminates Git authentication and deploy keys on the production server.
     - Guarantees the release matches the exact commit tested in CI (no race condition if someone pushes to the branch while CI is running).
     - Keeps production server network egress locked down.
   - *Asset build requirement:* Because `local_archive` packages the runner's local files, all frontend assets (e.g. `npm ci && npm run build`) must be compiled on the runner *before* `dep deploy` is called.

5. **Automatic CI author detection:**
   Deployer 8 automatically detects CI author information from environment variables in GitHub Actions (`GITHUB_ACTOR`), GitLab CI (`GITLAB_USER_LOGIN`), CircleCI, and Drone CI. In v7, pipelines often needed custom `-o user=...` arguments; these can be removed in v8.

6. **Host selector and CLI arguments:**
   - Deployer 7 pipelines often invoked: `dep deploy prod` or `dep deploy stage=production` or passed options like `dep deploy production -o branch=main`.
   - In Deployer 8, invoke: `vendor/bin/dep deploy "$DEPLOYER_SELECTOR" --no-interaction -vvv`. The selector maps to the host alias (e.g. `host('production')`) or label query.

7. **SSH security hardening:**
   - Never disable host checking with `-o StrictHostKeyChecking=no` in CI.
   - Never append `ssh-keyscan` dynamically to `known_hosts` without verification.
   - Store verified host keys in a repository or environment secret (`DEPLOY_KNOWN_HOSTS`) and use a dedicated unencrypted Ed25519 deploy key (`DEPLOY_SSH_PRIVATE_KEY`).

### Step-by-step pipeline upgrade checklist

- [ ] Run `php scripts/inspect-deployer.php --project-root . --format text` and inspect pipeline findings.
- [ ] Update CI runner PHP version to 8.3 or higher.
- [ ] Remove any `dep self-update` or dynamic `curl ... deployer.phar` download steps.
- [ ] Ensure `composer install` installs dependencies including `deployer/deployer:^8.0` in `require-dev`.
- [ ] In `deploy.php`, configure `set('update_code_strategy', getenv('CI') ? 'local_archive' : 'archive');`.
- [ ] If frontend assets were previously built on the target server, move the build steps (`npm ci && npm run build`) into the CI workflow before Deployer runs.
- [ ] Replace any legacy CLI flags with `vendor/bin/dep deploy "$DEPLOYER_SELECTOR" --no-interaction -vvv`.
- [ ] Ensure the deployment job has a concurrency group with `cancel-in-progress: false` to prevent parallel releases.
- [ ] Verify SSH host authentication with strict host checking (`StrictHostKeyChecking yes`).

### Pipeline comparison: Deployer 7 vs Deployer 8 (GitHub Actions)

#### Legacy Deployer 7 workflow (Hotspots to fix)

```yaml
# BEFORE (Deployer 7 - anti-patterns)
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.1' # HOTSPOT: Deployer 8 requires PHP 8.3+
      - run: curl -LO https://deployer.org/deployer.phar # HOTSPOT: Unversioned global phar
      - run: php deployer.phar self-update # HOTSPOT: Removed in Deployer 8
      - name: Deploy
        run: |
          # HOTSPOT: Insecure SSH host checking, target server must clone Git
          php deployer.phar deploy prod -o StrictHostKeyChecking=no
```

#### Modern Deployer 8 workflow

```yaml
# AFTER (Deployer 8 - secure & modern)
name: Deploy TYPO3 production
on:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: deploy-typo3-production
  cancel-in-progress: false

jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-24.04
    timeout-minutes: 30
    environment:
      name: production
      url: ${{ vars.DEPLOY_URL }}
    steps:
      - name: Check out the selected revision
        uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
        with:
          persist-credentials: false

      - name: Set up PHP 8.3
        uses: shivammathur/setup-php@f3e473d116dcccaddc5834248c87452386958240 # v2
        with:
          php-version: '8.3'
          tools: composer:v2
          coverage: none

      - name: Install dependencies
        run: composer install --no-interaction --prefer-dist --no-progress

      # Build assets on the runner so local_archive packages them into the release
      - name: Build frontend assets
        run: |
          if [ -f package.json ]; then
            npm ci
            npm run build
          fi

      - name: Configure and verify deployment SSH
        env:
          DEPLOY_SSH_PRIVATE_KEY: ${{ secrets.DEPLOY_SSH_PRIVATE_KEY }}
          DEPLOY_KNOWN_HOSTS: ${{ secrets.DEPLOY_KNOWN_HOSTS }}
          DEPLOY_HOST: ${{ vars.DEPLOY_HOST }}
          DEPLOY_USER: ${{ vars.DEPLOY_USER }}
          DEPLOY_PORT: ${{ vars.DEPLOY_PORT }}
        run: .github/scripts/configure-deployer-ssh.sh --verify

      - name: Deploy via Deployer 8 local_archive
        env:
          DEPLOYER_SELECTOR: ${{ vars.DEPLOYER_SELECTOR }}
        run: vendor/bin/dep deploy "$DEPLOYER_SELECTOR" --no-interaction -vvv
```

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

The version must be 8.x. No high-severity v7 recipe or pipeline finding may remain. Review informational TYPO3 findings rather than suppressing them blindly.

The first production deployment is a separate authorized operation. Record the previous release, database backup state, selected revision, and rollback command before running it.

## Sources

- [Official Deployer major-version upgrade guide](https://github.com/deployphp/deployer/blob/master/docs/UPGRADE.md)
- [Deployer 8 Upgrade Documentation](https://deployer.org/docs/8.x/UPGRADE)
- [Deployer v8 Announcement and Features](https://deployer.org/blog/deployer-v8)
- [Deployer 8 Getting Started](https://deployer.org/docs/8.x/getting-started)
- [Deployer 8 TYPO3 recipe](https://deployer.org/docs/8.x/recipe/typo3)

Checked on 2026-09-24.

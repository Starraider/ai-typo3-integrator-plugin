---
name: typo3-deployer-deployment
description: Configure and operate Deployer 8 for Composer-based TYPO3 projects, including new deploy.php recipes, safe in-place upgrades from Deployer 7, and GitHub Actions SSH deployments. Use when deploying TYPO3 with Deployer, migrating deployer/deployer from v7 to v8, or adding a CI deployment workflow. Do not use for TYPO3 core upgrades, server provisioning, or non-Deployer release systems.
license: CC-BY-4.0
compatibility: Requires PHP 8.3 or later, Composer 2, Git, OpenSSH, and network access to the deployment host. GitHub Actions setup also requires repository administration access for environments, secrets, and variables.
---

# TYPO3 Deployer 8 deployment

## Outcome

Produce a Composer-based TYPO3 deployment that uses `deployer/deployer:^8.0`, a Deployer 8-compatible recipe, and, when requested, a GitHub Actions workflow with pinned SSH host authentication. Preserve an existing Deployer 7 release layout during an in-place upgrade.

Do not provision servers, upgrade TYPO3 core, invent production credentials, or replace another deployment system unless the user expands the scope.

## Workflow

1. Inspect the project before changing it.

   Read repository instructions, `composer.json`, `composer.lock`, every Deployer recipe or inventory, deployment documentation, and existing workflows. Run:

   ```bash
   php scripts/inspect-deployer.php --project-root . --format json
   ```

   Resolve the deployment target, web root, deploy path, remote user, release trigger, shared files and directories, writable directories, build steps, database update policy, and rollback expectations. Treat host names and paths as configuration. Treat private keys, passphrases, tokens, and application `.env` contents as secrets.

   Completion: the current Deployer state is classified as absent, v7, v8, mixed, or unknown, and every value that could direct a deployment to the wrong server is known or left as an explicit placeholder.

2. Select the matching implementation branch.

   - For a new setup, read [the TYPO3 recipe guide](references/deployer-8-typo3.md). Add Deployer to `require-dev`, create or adapt `deploy.php`, and preserve the project's existing build and shared-state conventions.
   - For a v7 installation, read [the v7 to v8 upgrade guide](references/upgrade-v7-to-v8.md) completely. Run `scripts/upgrade-deployer-v8.sh` without `--apply`, review the report, then run it with `--apply` when the requested change authorizes dependency updates. Migrate every reported recipe hotspot by meaning. Do not run `dep init` over the existing recipe.
   - For GitHub Actions, also read [the GitHub Actions deployment guide](references/github-actions.md). Copy [the workflow template](templates/deploy-typo3.yml) to `.github/workflows/deploy-typo3.yml` and copy `scripts/configure-ci-ssh.sh` to `.github/scripts/configure-deployer-ssh.sh`. Adapt names and paths without placing secret values in Git.

   When CI deploys the checked-out commit, prefer Deployer 8's `local_archive` update strategy. This avoids a second GitHub credential on the target server. Keep another strategy only when the repository already relies on it and its authentication path is verified.

   Completion: `composer.json` and `composer.lock` resolve Deployer 8, the recipe contains no unresolved v7 breaking patterns, TYPO3 shared state remains outside release directories, and the CI workflow calls the repository's Deployer binary with one unambiguous selector.

3. Validate without deploying.

   Run the checks that apply:

   ```bash
   composer validate --strict --no-check-publish
   php -l deploy.php
   vendor/bin/dep --version
   vendor/bin/dep list
   vendor/bin/dep tree deploy
   bash -n .github/scripts/configure-deployer-ssh.sh
   ruby -e 'require "yaml"; YAML.parse_file(ARGV.fetch(0))' .github/workflows/deploy-typo3.yml
   ```

   Run `actionlint` and `shellcheck` when available. Inspect the recipe or inventory to confirm that the intended selector names the expected host. Review `git diff` for changed host names, deploy paths, shared paths, task order, secrets, and workflow triggers. Do not use an actual deployment as a syntax check.

   Completion: local validation passes, `vendor/bin/dep --version` reports major version 8, the recipe loads, the configured host supports the intended selector, the workflow parses, and no secret value appears in tracked files or logs.

4. Cross the deployment boundary only with explicit authorization.

   A request to configure, upgrade, or create a workflow does not authorize a live deployment or a workflow dispatch. Before an authorized deployment, state the environment, selector, Git revision, tasks that can mutate the database or shared files, and rollback command. Use the project's required test and build gates first. Run one deployment at a time.

   Completion: either the requested configuration work is handed off without contacting the server, or an explicitly authorized deployment completes and its release, URL, and rollback state are verified.

## Safety rules

- Never commit a private key, application secret, `.env` contents, or generated SSH config.
- Require a dedicated deployment key and a preverified `known_hosts` entry. Never set `StrictHostKeyChecking=no` and never trust `ssh-keyscan` output without checking its fingerprint through another channel.
- Preserve `deploy_path`, `shared/`, `current`, `.dep`, and release history during a v7 to v8 upgrade. Do not delete old releases as part of the migration.
- Do not replace non-empty `shared_dirs`, `shared_files`, or `writable_dirs` with recipe defaults without checking the live layout.
- Treat TYPO3 extension setup and schema updates as database mutations. Require the project's backup and maintenance policy before the first production run.
- Run `deploy:unlock` only after confirming that no deployment is active and the stale lock's cause is understood.

## Resources

- `scripts/inspect-deployer.php`: read-only Deployer version and recipe hotspot detection.
- `scripts/upgrade-deployer-v8.sh`: transactional Composer dependency upgrade from v7 to v8. Recipe migration remains an explicit reviewed step.
- `scripts/configure-ci-ssh.sh`: non-interactive GitHub runner SSH setup with a pinned host key.
- [Deployer 8 and TYPO3](references/deployer-8-typo3.md): recipe design and TYPO3 release checks.
- [Upgrade from Deployer 7](references/upgrade-v7-to-v8.md): breaking changes and in-place migration sequence.
- [GitHub Actions deployment](references/github-actions.md): credentials, environment settings, secrets, variables, and workflow operation.
- [Workflow template](templates/deploy-typo3.yml): manual production deployment through Deployer 8.

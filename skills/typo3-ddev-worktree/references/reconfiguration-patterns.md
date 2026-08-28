# Reconfiguration patterns

Use this reference after the audit reports a blocker or when the repository has custom DDEV services.

## DDEV project identity

Remove the top-level `name:` from tracked `.ddev/config.yaml`. Do not replace it with a branch name. DDEV will derive a distinct project name from each worktree directory.

Choose worktree directory names that normalize cleanly to lowercase letters, digits, and hyphens. Before starting a target, compare its expected name with `ddev list` and every existing worktree.

Do not set fixed router, web, database, Mailpit, Vite, or debugger host ports in tracked configuration when worktrees must run together. Let DDEV allocate ports unless the service has a tested worktree-aware strategy.

## TYPO3 site base

Prefer a relative site base:

```yaml
base: /
```

Preserve a real subpath when the site uses one:

```yaml
base: /members/
```

For `base: '%env(SITE_BASE)%'`, trace the variable through tracked and ignored environment files plus DDEV `web_environment`. A relative local value is worktree-safe. A value containing the original `*.ddev.site` host is not.

If production requires an absolute value, keep production configuration outside the local worktree default. Valid approaches include a deployment-supplied environment variable or an ignored worktree-local DDEV config generated from the current DDEV name. Do not replace a production URL with `/` without proving where production gets its value.

Avoid a start/stop pair that edits a tracked site file and later calls `git restore`. A stop hook can erase a developer's legitimate edit. Generate an ignored override or make the tracked local default hostname-independent.

## Generated DDEV configuration and add-ons

Treat `#ddev-generated` as ownership metadata. Find the add-on command and version before editing the output. Reconfigure or regenerate the add-on after removing the fixed DDEV name.

Review all of these locations:

- `.ddev/config*.yaml`
- `.ddev/docker-compose*.yaml`
- `.ddev/apache/`, `.ddev/nginx_full/`, and `.ddev/traefik/`
- `.ddev/commands/` and add-on metadata
- Vite, BrowserSync, Playwright, Selenium, Solr, Redis, Mailpit, and phpMyAdmin additions

In Docker Compose files, use `${DDEV_SITENAME}`, `${DDEV_APPROOT}`, and DDEV-provided host variables where supported. A literal `container_name`, named volume, network, or `*.ddev.site` hostname can collide.

Some `.ddev/config*.yaml` fields do not expand runtime variables. In that case:

1. Remove the fixed value from tracked configuration.
2. Add a narrow ignored file such as `.ddev/config.worktree.yaml` to `.gitignore`.
3. Generate it from a documented bootstrap command after the worktree exists.
4. Validate the merged result with `ddev get-config` or the equivalent command supported by the installed DDEV version.

Never put secrets in the generated file or print environment-file contents in logs.

## Writable paths

Each DDEV project already gets separate default volumes when its project name differs. Check custom Compose files for volumes with literal names or bind mounts outside the worktree. Shared read-only caches are usually fine. Shared databases, upload directories, cache directories, and generated assets are not.

TYPO3 commonly writes to:

- `var/`
- `public/typo3temp/`
- `public/fileadmin/`
- generated public assets
- project-specific private or secure upload directories

Keep those paths inside the target worktree or its DDEV volumes. Do not symlink a target's writable storage back to the source checkout merely to save disk space.

## Readiness diff

After editing:

1. Run the audit again.
2. Inspect `git diff -- .ddev config/sites .env* .gitignore`.
3. Run repository config linting.
4. Start the original checkout and verify its URL before creating a second worktree.
5. Ensure the target start point contains the readiness changes. Uncommitted source changes do not appear in a new worktree.

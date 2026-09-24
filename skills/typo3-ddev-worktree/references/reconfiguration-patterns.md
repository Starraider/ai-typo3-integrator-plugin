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
2. Add a narrow ignored file such as `.ddev/config.worktree.yaml` or `.ddev/config.vite.yaml` to `.gitignore`.
3. Generate it from a documented bootstrap command after the worktree exists.
4. Validate the merged result with `ddev get-config` or the equivalent command supported by the installed DDEV version.

Never put secrets in the generated file or print environment-file contents in logs.

## Frontend development servers (Vite, HMR, SSL subdomains, and reverse proxying)

### When is this section needed? (Asset architecture detection)
Frontend dev server configuration is **strictly optional**. Many TYPO3 projects rely on traditional asset approaches that do not require any reverse proxies, dev servers, or extra subdomains:
- **`EXT:bootstrap_package` (SCSS processing via TYPO3)**: Assets are compiled by TYPO3 into `public/typo3temp/assets/` or served from extension `Resources/Public/`. DDEV routes everything through the primary domain (`https://<project>.ddev.site`). No extra proxy, subdomains, or Vite configuration are needed.
- **Plain CSS / JavaScript**: Static assets placed in `Resources/Public/` or site package folders are served directly by Apache/Nginx in DDEV without dev-server infrastructure.
- **External / Pre-compiled builds**: If assets are compiled outside DDEV or via npm build scripts into `Resources/Public/`, standard DDEV web serving suffices.
- **Vite with dev server (`praetorius/vite-asset-collector` / `vite-plugin-typo3`)**: When a project opts for Vite in development mode to enable Hot Module Replacement (HMR), follow the patterns below to avoid port, hostname, and certificate collisions in worktrees.

The `bootstrap-ddev-worktree.sh` template automatically detects whether Vite is used (by checking for `vite.config.*`, `praetorius/vite-asset-collector` in `composer.json`, or `"vite"` in `package.json`). If Vite is absent, it skips Vite proxy setup, keeping non-Vite worktrees lean and standard.

### 1. Automated provisioning via DDEV hooks
Avoid requiring developers to manually run bootstrap scripts whenever creating or switching worktrees. Add a host `pre-start` hook in `.ddev/config.yaml`:

```yaml
hooks:
  pre-start:
    - exec-host: "./scripts/bootstrap-ddev-worktree.sh"
```

DDEV executes this before starting containers, ensuring that `.ddev/config.vite.yaml`, `.ddev/apache/vite.conf`, and `.ddev/nginx_full/vite.conf` exist with the exact derived `${project_name}`.

### 2. Worktree-specific Vite configuration (.ddev/config.vite.yaml)
Generate an untracked (git-ignored) configuration file:

```yaml
# Generated by scripts/bootstrap-ddev-worktree.sh; do not commit.
additional_hostnames:
  - vite.${project_name}
web_environment:
  - VITE_SERVER_URI=https://vite.${project_name}.ddev.site
  - VITE_PACKAGE_MANAGER=npm
```

### 3. Apache and Nginx reverse proxy directives
In `.ddev/apache/vite.conf`:
- Use `ServerName vite.${project_name}.ddev.site` and `ServerAlias vite.*` so subdomains route cleanly.
- Set `ProxyPreserveHost On` so the incoming hostname reaches Vite.
- Enable WebSocket upgrades on the proxy: `ProxyPass / http://localhost:5173/ upgrade=websocket` alongside standard `RewriteCond %{HTTP:Upgrade} websocket [NC]` rewrite rules.
- Ensure `DocumentRoot` and `<Directory>` permissions are set for `/var/www/html/.ddev/vite/` and `/mnt/ddev_config/vite/`.

### 4. Two-level subdomains and stale Traefik router cleanup
- Hostnames such as `vite.<project>.ddev.site` have two subdomain levels. The default `*.ddev.site` wildcard certificate only matches single-level subdomains (`<project>.ddev.site`).
- DDEV uses `mkcert` to issue multi-domain SAN certificates including `vite.<project>.ddev.site` based on `additional_hostnames`.
- **Trap**: Stale files in `.ddev/traefik/config/*.yaml` or `.ddev/traefik/certs/*.crt` (e.g. from previous renames or copied worktrees) cause DDEV's merged Traefik configuration to conflict, resulting in Traefik falling back to the `localhost` certificate (`ERR_CERT_COMMON_NAME_INVALID`).
- The bootstrap script must purge any files in `.ddev/traefik/config/` and `.ddev/traefik/certs/` that do not match the current `${project_name}`.

### 5. Vite HMR configuration for reverse-proxied HTTPS
In `vite.config.js`, configure `server` dynamically from `process.env.VITE_SERVER_URI`:

```javascript
const serverUri = process.env.VITE_SERVER_URI ? new URL(process.env.VITE_SERVER_URI) : null;

export default defineConfig({
    // ...
    server: {
        host: '0.0.0.0',
        port: 5173,
        strictPort: true,
        cors: true,
        origin: serverUri ? serverUri.origin : undefined,
        hmr: serverUri ? {
            host: serverUri.hostname,
            protocol: serverUri.protocol === 'https:' ? 'wss' : 'ws',
            clientPort: serverUri.port ? parseInt(serverUri.port, 10) : (serverUri.protocol === 'https:' ? 443 : 80),
        } : true,
    },
});
```

Without `protocol: 'wss'` and `clientPort: 443`, Vite's client script attempts to connect to `wss://vite.<project>.ddev.site:?token=...` (syntax error due to missing port) or falls back to port 5173 (which is internal to the container), breaking HMR.

### 6. TYPO3 `vite_asset_collector` dev server mode & graceful fallback
- In `Development` context, `vite_asset_collector` injects `<script>` tags for `@vite/client` and entrypoints instead of static `<link rel="stylesheet">` tags. If requests to the Vite dev server fail, the browser injects zero CSS into the DOM, leaving the website completely unstyled.
- In `config/system/additional.php`, dynamically derive `devServerUri` from `DDEV_HOSTNAME` if `VITE_SERVER_URI` is unset.
- Provide a `TYPO3_USE_VITE_DEV_SERVER` environment variable check so developers can test production compiled assets (`manifest.json`) in `Development` context by setting `TYPO3_USE_VITE_DEV_SERVER=0` in `.env`.

### 7. Relative Sass path resolution vs symlinks
When extensions live in `packages/*` and are symlinked into `vendor/*` via Composer path repositories:
- Deep relative imports (e.g. `@import "../../../../../vendor/..."`) rely on the 5-level realpath depth from `packages/<ext>/Resources/Private/Scss/`.
- Enabling `resolve.preserveSymlinks: true` in Vite changes the evaluated path to `vendor/<ext>/...`, shifting the relative depth and breaking SCSS compilation (HTTP 500). Keep `preserveSymlinks: false` (the default) unless paths are rewritten or aliased.

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

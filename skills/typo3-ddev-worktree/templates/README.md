# Worktree Setup Templates for TYPO3 & DDEV

These templates configure Composer-based TYPO3 projects for parallel Git worktrees in DDEV.

> **Note on Asset Pipelines**: Vite and `praetorius/vite-asset-collector` are **strictly optional**.
> - If your project uses standard TYPO3 assets (`EXT:bootstrap_package`, Fluid styled content, plain CSS in `Resources/Public/`, or static build output), standard DDEV serves these out of the box from the primary domain (`https://<project>.ddev.site`). You only need the core worktree rules (omit `name:` in `.ddev/config.yaml`, relative `base: /`).
> - The `scripts/bootstrap-ddev-worktree.sh` script automatically detects whether Vite is in use. If no Vite configuration is found, it cleanly skips Vite proxy generation and purges stale Traefik files.

## Files

- **`scripts/bootstrap-ddev-worktree.sh`**:
  Copy to `<project-root>/scripts/bootstrap-ddev-worktree.sh`.
  Derives `project_name` from current checkout directory. Auto-detects whether Vite is used; if so, generates `.ddev/config.vite.yaml`, `.ddev/apache/vite.conf`, and `.ddev/nginx_full/vite.conf`. In all cases, cleans up stale Traefik router/certificate files.
  Make it executable: `chmod +x scripts/bootstrap-ddev-worktree.sh`.

- **`.ddev/config.yaml.snippet`**:
  Add `hooks.pre-start` to `.ddev/config.yaml`. Ensures DDEV runs `bootstrap-ddev-worktree.sh` automatically before containers start in any checkout.

- **`vite.config.js`** *(optional, only if using Vite)*:
  Reference configuration for Vite. Dynamically configures `server.origin` and `server.hmr` (`protocol: 'wss'`, `clientPort: 443`, `host: serverUri.hostname`) from `process.env.VITE_SERVER_URI`.

- **`config/system/additional.php`** *(optional, only if using Vite / `vite-asset-collector`)*:
  Add to TYPO3's `config/system/additional.php`. Dynamically derives Vite dev-server URI from `DDEV_HOSTNAME` if `VITE_SERVER_URI` is unset, and provides `TYPO3_USE_VITE_DEV_SERVER` environment toggle.

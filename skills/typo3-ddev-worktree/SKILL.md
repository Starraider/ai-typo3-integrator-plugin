---
name: typo3-ddev-worktree
description: Prepare and create independent Git worktrees for Composer-based DDEV TYPO3 projects. Use when an agent must make a TYPO3 repository worktree-safe, create a feature worktree, copy local database and file state, or diagnose DDEV hostname, site-base, add-on, port, or container collisions between worktrees.
compatibility: Requires Git, DDEV, Docker, Python 3.10 or later, and a Composer-based TYPO3 project. Database and file cloning require enough local disk space.
---

# DDEV TYPO3 worktree

Make a DDEV TYPO3 repository safe for parallel Git worktrees, then create and verify an isolated feature checkout when the user asks for one.

## 1. Establish the requested scope

Determine whether the user wants:

- a readiness audit only;
- tracked project reconfiguration;
- a new worktree without local content;
- or a runnable worktree cloned from the source project's database and file storage.

Resolve the source repository, start point, feature branch, destination, and required local data. Derive a sibling destination and a lowercase hyphenated branch name when the request makes the intent clear. Ask only when a collision or a materially different data choice remains.

Do not treat this skill as permission to deploy, change production configuration, publish secrets, remove an existing worktree, delete Docker volumes, or overwrite a destination.

Completion: the requested outcome and every path or branch that could be changed are known.

## 2. Audit before changing anything

Read all applicable `AGENTS.md` files and inspect the repository status. Run:

```bash
python3 scripts/audit_worktree_readiness.py --project /absolute/path/to/project
```

Also inspect `git worktree list --porcelain`, ignored local configuration, DDEV hooks, custom Compose services, router files, add-ons, TYPO3 site configurations, upload directories, and frontend development servers. Read [reconfiguration patterns](references/reconfiguration-patterns.md) for every reported blocker.

Probe the running source before selecting verification commands. Capture `ddev describe -j`; list the available TYPO3 CLI commands when `ddev typo3` is installed; and request the response status of one public route plus any protected route relevant to the requested work. Use only commands that the source project supports. Treat a protected route's expected redirect, `401`, or `403` as an access-boundary result, not a failed public smoke check.

Classify unrelated dirty files as user-owned. Do not modify, stage, stash, or commit them.

Completion: every fixed project name, hostname, port, container name, TYPO3 base, shared writable path, and required untracked file has a disposition.

## 3. Reconfigure the repository

Apply the smallest tracked changes that make future worktrees independent:

1. Remove the top-level `name:` from `.ddev/config.yaml`. Do not set a replacement name in tracked configuration.
2. Make each TYPO3 site base hostname-independent. Prefer a relative base such as `/` or `/subpath/`. If production needs an absolute base, keep production input separate and generate an ignored worktree-local override instead of rewriting a tracked file on every start.
3. Replace fixed DDEV hostnames, project-specific container names, router service names, and host ports. Use DDEV runtime variables where the owning file supports them. Generate an ignored per-worktree config where it does not.
4. Make add-on and frontend-server hostnames derive from the worktree's DDEV project name:
   - **Identify asset architecture (Vite is optional)**: Many TYPO3 projects rely on standard asset pipelines such as `EXT:bootstrap_package` (SCSS compiled by TYPO3 into `typo3temp/assets/`), Fluid styled content, plain CSS/JS in `Resources/Public/`, or static pre-compiled build assets. For these projects, DDEV serves all assets directly through the primary domain (`https://<project>.ddev.site`). Skip Vite proxy configuration entirely — standard DDEV serves these out of the box with zero extra configuration.
   - **When Vite (or a similar dev server) is detected** (e.g. `praetorius/vite-asset-collector` in `composer.json` or `vite.config.*` present):
     - The bootstrap script auto-detects Vite and generates untracked `.ddev/config.vite.yaml` with `additional_hostnames: [vite.${project_name}]` and `VITE_SERVER_URI=https://vite.${project_name}.ddev.site`.
     - Configures the web server proxy (`.ddev/apache/vite.conf`) with `ServerAlias vite.*`, `ProxyPreserveHost On`, and `upgrade=websocket`.
     - Configures `vite.config.js` with dynamic `server.origin` and `server.hmr` (`protocol: 'wss'`, `clientPort: 443`, `host: serverUri.hostname`) to prevent broken WebSocket URLs and port 5173 fallback.
     - Purges stale Traefik files in `.ddev/traefik/` that do not match `${project_name}` to prevent Traefik falling back to the `localhost` certificate (`ERR_CERT_COMMON_NAME_INVALID`).
     - In TYPO3 `config/system/additional.php`, adds dynamic fallback from `DDEV_HOSTNAME` for `devServerUri` and allows toggling dev-server mode via `TYPO3_USE_VITE_DEV_SERVER`.
     - Ready-to-use templates are provided in `templates/`.
5. Keep databases, upload directories, caches, generated assets, dependency trees, and other writable runtime state out of shared paths.
6. Automate untracked local configuration so developers and agents do not need manual bootstrap steps:
   - Add a `pre-start` host hook in `.ddev/config.yaml` to execute `./scripts/bootstrap-ddev-worktree.sh` automatically before containers start.
   - Provide a documented bootstrap script (`scripts/bootstrap-ddev-worktree.sh`) that auto-detects Vite, handles Traefik cleanup, is repeatable, and never embeds secrets.

Do not use a `post-stop` hook that runs `git restore` on tracked files. It can discard legitimate worktree changes. A hook may update an ignored generated override.

Run the audit again. Review the diff and the repository's existing config checks. If the new worktree must inherit uncommitted readiness changes, either obtain permission to commit them or apply the same changes in the new worktree. Never imply that `git worktree add` includes uncommitted files.

Completion: the audit has no blockers, tracked configuration is stable across simultaneous worktrees, and the readiness changes will exist in the target checkout.

## 4. Capture local state when requested

Read [data and bootstrap](references/data-and-bootstrap.md) before copying a database, file storage, `.env` file, private package credentials, or other local-only state.

Create the export directory outside every Git worktree. Export the source database once. Archive only the configured TYPO3 writable storage that the target needs, normally `public/fileadmin`. Record the source revision and checksums. Restrict permissions on the export and evidence artifacts themselves; do not set a process-wide restrictive umask before creating the Git worktree or a Docker build context, because it can remove required executable bits. Do not add exports to Git.

Copy ignored local configuration only when the target needs it. Keep it on the same machine, preserve restrictive permissions, and report which files were copied without printing their values.

Completion: requested imports have readable, non-empty source artifacts outside Git, or the user has chosen a clean installation.

## 5. Create and bootstrap the worktree

Validate that the destination does not exist and the branch is not checked out elsewhere. Use one of these forms:

```bash
git worktree add -b <new-branch> <absolute-destination> <start-point>
git worktree add <absolute-destination> <existing-branch>
```

Inside the target:

1. Generate required ignored local overrides.
2. Start DDEV and capture the assigned project name and primary URL.
3. Install locked Composer dependencies before running project TYPO3 CLI commands. Install locked frontend dependencies only when the application or requested verification needs them.
4. Import the database and file archive when requested.
5. Run project-owned TYPO3 setup, cache, schema, asset, and build commands in the order documented by the repository.

When DDEV uses custom Compose build contexts or entrypoint scripts, verify that tracked executable files remain executable in the target before starting the affected service. On a failed stateful command, capture sanitized failure evidence explicitly rather than relying only on shell error traps.

Do not import into the source project's DDEV instance. Before an import, verify that the current directory and `DDEV_SITENAME` belong to the target worktree.

Completion: DDEV reports healthy target services, dependencies exist, and TYPO3 commands run in the target container.

## 6. Verify isolation and application health

Verify all of the following:

- source and target resolve to different worktree paths, DDEV project names, primary URLs, containers, and database volumes;
- the target TYPO3 site base resolves to the target URL and does not redirect to the source;
- `ddev describe` and a basic database query succeed;
- TYPO3 cache flush and the project's normal smoke checks succeed;
- one canonical public frontend route returns the source project's expected response after a warm-up request of up to 60 seconds; protected routes retain their source project's expected redirect, `401`, or `403` behavior;
- asset delivery and styling:
  - for projects using `EXT:bootstrap_package`, plain CSS, or static build assets: verify that standard stylesheets load with HTTP 200 from the primary DDEV domain and the page renders fully styled;
  - for projects using a frontend dev server (e.g. Vite): verify that `https://vite.<project>.ddev.site/@vite/client` and entrypoint scripts return HTTP 200 without SSL certificate errors, CSS stylesheets are injected into the DOM, and WebSocket HMR (`wss://`) connects;
- relevant DDEV, web server, PHP, and TYPO3 logs contain no new startup error;
- `git status --short` in both worktrees contains only expected changes.

Follow repository-specific browser instructions for UI verification. Treat timeouts and infrastructure failures separately from application failures.

If verification fails, preserve the worktree and logs. Do not remove the worktree, delete volumes, or overwrite exports unless the user asks.

If the user authorizes cleanup after a failed attempt, wait for DDEV cleanup to finish and verify that the target worktree, branch, project, containers, and volumes are gone before retrying. Report any host-alias cleanup that needs an interactive privilege prompt separately from project cleanup.

Completion: the target runs independently and the verification evidence names the checked URL and commands, or the exact remaining blocker is reported.

## Resources

- `scripts/audit_worktree_readiness.py` performs a read-only, repeatable readiness audit.
- [Reconfiguration patterns](references/reconfiguration-patterns.md) covers TYPO3 bases, DDEV naming, fixed ports, add-ons, Vite/frontend dev servers, and generated local overrides.
- [Data and bootstrap](references/data-and-bootstrap.md) covers safe database and file transfer, dependency installation, and verification.
- [Templates](templates/README.md) provides ready-to-copy scripts and snippets for Vite, Apache proxying, TYPO3 configuration, and DDEV hooks.

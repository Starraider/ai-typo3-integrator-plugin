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

Classify unrelated dirty files as user-owned. Do not modify, stage, stash, or commit them.

Completion: every fixed project name, hostname, port, container name, TYPO3 base, shared writable path, and required untracked file has a disposition.

## 3. Reconfigure the repository

Apply the smallest tracked changes that make future worktrees independent:

1. Remove the top-level `name:` from `.ddev/config.yaml`. Do not set a replacement name in tracked configuration.
2. Make each TYPO3 site base hostname-independent. Prefer a relative base such as `/` or `/subpath/`. If production needs an absolute base, keep production input separate and generate an ignored worktree-local override instead of rewriting a tracked file on every start.
3. Replace fixed DDEV hostnames, project-specific container names, router service names, and host ports. Use DDEV runtime variables where the owning file supports them. Generate an ignored per-worktree config where it does not.
4. Make add-on and frontend-server hostnames derive from the worktree's DDEV project name. Regenerate `#ddev-generated` files when the add-on owns them; do not hand-edit generated output unless the add-on documents that as supported.
5. Keep databases, upload directories, caches, generated assets, dependency trees, and other writable runtime state out of shared paths.
6. Add a documented bootstrap command or script when a clean worktree needs untracked local configuration. It must be repeatable and must not embed credentials.

Do not use a `post-stop` hook that runs `git restore` on tracked files. It can discard legitimate worktree changes. A hook may update an ignored generated override.

Run the audit again. Review the diff and the repository's existing config checks. If the new worktree must inherit uncommitted readiness changes, either obtain permission to commit them or apply the same changes in the new worktree. Never imply that `git worktree add` includes uncommitted files.

Completion: the audit has no blockers, tracked configuration is stable across simultaneous worktrees, and the readiness changes will exist in the target checkout.

## 4. Capture local state when requested

Read [data and bootstrap](references/data-and-bootstrap.md) before copying a database, file storage, `.env` file, private package credentials, or other local-only state.

Create the export directory outside every Git worktree. Export the source database once. Archive only the configured TYPO3 writable storage that the target needs, normally `public/fileadmin`. Record the source revision and checksums. Do not add exports to Git.

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
3. Install locked Composer dependencies. Install locked frontend dependencies only when the application or requested verification needs them.
4. Import the database and file archive when requested.
5. Run project-owned TYPO3 setup, cache, schema, asset, and build commands in the order documented by the repository.

Do not import into the source project's DDEV instance. Before an import, verify that the current directory and `DDEV_SITENAME` belong to the target worktree.

Completion: DDEV reports healthy target services, dependencies exist, and TYPO3 commands run in the target container.

## 6. Verify isolation and application health

Verify all of the following:

- source and target resolve to different worktree paths, DDEV project names, primary URLs, containers, and database volumes;
- the target TYPO3 site base resolves to the target URL and does not redirect to the source;
- `ddev describe` and a basic database query succeed;
- TYPO3 cache flush and the project's normal smoke checks succeed;
- one canonical frontend route returns the expected response after a warm-up request of up to 60 seconds;
- relevant DDEV, web server, PHP, and TYPO3 logs contain no new startup error;
- `git status --short` in both worktrees contains only expected changes.

Follow repository-specific browser instructions for UI verification. Treat timeouts and infrastructure failures separately from application failures.

If verification fails, preserve the worktree and logs. Do not remove the worktree, delete volumes, or overwrite exports unless the user asks.

Completion: the target runs independently and the verification evidence names the checked URL and commands, or the exact remaining blocker is reported.

## Resources

- `scripts/audit_worktree_readiness.py` performs a read-only, repeatable readiness audit.
- [Reconfiguration patterns](references/reconfiguration-patterns.md) covers TYPO3 bases, DDEV naming, fixed ports, add-ons, and generated local overrides.
- [Data and bootstrap](references/data-and-bootstrap.md) covers safe database and file transfer, dependency installation, and verification.

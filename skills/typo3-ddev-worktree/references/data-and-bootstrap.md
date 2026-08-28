# Data and bootstrap

Read this reference only when creating a worktree or copying local runtime state.

## Choose the data model

Use a clean installation when fixtures or migrations can create the required state. Clone local state when the feature depends on realistic content, accounts, FAL relations, or extension data.

Copy only what the requested work needs. A database export and `fileadmin` archive may contain personal or confidential data. Keep them local, outside Git, and restrict permissions.

## Export from the source

Create a dedicated directory outside every worktree. Use an explicit absolute path. Do not place exports under the repository if a broad Git command could add them.

Record:

- source repository and revision;
- source DDEV project name;
- export time;
- database file path and checksum;
- each archived upload directory and checksum.

Export the database with DDEV:

```bash
ddev export-db --file=/absolute/private/export/db.sql.gz
```

Archive the configured upload directory. For a standard TYPO3 project:

```bash
tar -C public/fileadmin -czf /absolute/private/export/fileadmin.tar.gz .
```

List and test archives before importing. Do not log record contents or filenames when they may expose personal data.

## Create and start the target

Create the worktree from an explicit start point. A new branch and an existing branch require different `git worktree add` forms. Never force a branch already checked out in another worktree.

Generate ignored local config before `ddev start` when startup depends on it. Then start DDEV in the target and verify identity before importing:

```bash
ddev describe
ddev exec printenv DDEV_SITENAME
```

The printed name and current directory must identify the target, not the source.

Install dependencies from lock files. Prefer `ddev composer install` for Composer and the repository's locked package-manager command for frontend dependencies. Do not run an unconstrained update.

## Import into the target

Import the database only after target identity is proven:

```bash
ddev import-db --file=/absolute/private/export/db.sql.gz
```

Use `ddev import-files` when the project's `upload_dirs` matches the archive layout and the installed DDEV version supports the required source form. Otherwise extract into a validated staging directory inside the target and move it into place only after confirming the destination. Preserve any pre-existing target files until the import succeeds.

Run TYPO3 cache flush after import. Run schema updates only when the target code requires them and the imported database is isolated. Schema updates mutate the target database, so record the command and result.

## Local configuration

Worktrees do not receive ignored files. Inventory required `.env`, authentication, license, and package-manager files. Copy only the allowlisted files required to boot. Never display secret values.

For reusable setup, prefer a bootstrap script that creates non-secret defaults and reports missing secret inputs. Do not commit a developer's private `.env`, Composer credentials, SSH material, private keys, or production database dump.

## Verification order

1. `git worktree list --porcelain` shows distinct paths and branches.
2. Source and target `ddev describe` show distinct project names and URLs.
3. Target services are healthy.
4. A basic target database query succeeds.
5. TYPO3 CLI and cache flush succeed.
6. Required build and automated checks succeed.
7. Warm one canonical frontend route for up to 60 seconds, then verify it with the repository's preferred browser.
8. Inspect recent target logs after a timeout or server error.
9. Check source and target Git status for unexpected edits.

Do not tear down a failed target automatically. The worktree, containers, and logs are diagnostic evidence.

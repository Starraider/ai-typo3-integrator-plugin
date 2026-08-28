# typo3-ddev-worktree

This skill prepares Composer-based DDEV TYPO3 repositories for independent Git worktrees and can create a runnable feature worktree with its own DDEV project, database, file storage, dependencies, hostname, and TYPO3 routing.

## What this skill solves

DDEV normally gives each checkout a project name derived from its directory. A tracked `name:` defeats that isolation. TYPO3 can then add a second failure: an absolute site `base` still points at the original checkout. Fixed add-on hostnames, router files, ports, or container names create the same collision in less obvious places.

The skill audits those settings before changing anything. It then guides the agent through stable tracked fixes, optional local data cloning, worktree creation, and runtime verification.

## Use when

- Preparing a DDEV TYPO3 repository so multiple worktrees can run together.
- Creating a feature or bug-fix worktree that must boot as a separate DDEV project.
- Copying a source checkout's local database and `fileadmin` state into a new worktree.
- Diagnosing why a TYPO3 worktree redirects to the original hostname, returns a routing error, or collides with another DDEV project.

Do not use it for production deployment, non-DDEV Docker projects, ordinary branch switching, or removing worktrees.

## Expected outputs

- A readiness report with blockers, warnings, and evidence paths.
- Reviewed project configuration changes when preparation is requested.
- An optional Git worktree with an independent DDEV URL and runtime data.
- Verification evidence for DDEV, TYPO3, the database, and one canonical frontend route.

## Context requirements

- Git, DDEV, Docker, and Python 3.10 or later.
- A Composer-based TYPO3 repository with `.ddev/config.yaml`.
- A branch or feature intent and enough disk space for another database and file tree.
- Explicit user intent before copying local data, committing readiness changes, deleting an existing worktree, or deleting DDEV volumes.

## Installation

Place the `typo3-ddev-worktree` directory in a skill directory discovered by an Agent Skills-compatible client.

Common locations:

- User installation: `~/.agents/skills/typo3-ddev-worktree/`
- Repository installation: `<repository>/.agents/skills/typo3-ddev-worktree/`

The skill uses only portable Agent Skills metadata. Client-specific installation and discovery rules still apply.

## Example prompts

- "Prepare this DDEV TYPO3 repository for parallel Git worktrees, then create `codex/member-search` in a sibling directory."
- "Audit this TYPO3 project for worktree collisions. Production uses an absolute site base, so do not replace its production URL."
- "Create a runnable worktree for the existing `bugfix/vite-host` branch and clone the current local database and fileadmin into it."
- "Why does my second DDEV TYPO3 worktree redirect to the first project's hostname? Diagnose only."

## Validation

Validate the package structure:

```bash
/path/to/new-skill/scripts/validate-skill.sh /path/to/typo3-ddev-worktree --strict-portable
skills-ref validate /path/to/typo3-ddev-worktree
```

Run the audit's tests:

```bash
python3 -m unittest discover -s /path/to/typo3-ddev-worktree/tests -p 'test_*.py'
```

Audit a project without changing it:

```bash
python3 /path/to/typo3-ddev-worktree/scripts/audit_worktree_readiness.py --project /path/to/project
```

## Design sources

The workflow follows DDEV's guidance to omit a tracked project name, use directory-derived project names, give each worktree its own database and files, and avoid an absolute TYPO3 base tied to the original hostname:

- [Using `git worktree` with TYPO3](https://ddev.com/blog/git-worktree-with-typo3/)
- [Contributor Training: `git worktree` for Multiple DDEV Projects](https://ddev.com/blog/git-worktree-contributor-training/)
- [Agent Skills specification](https://agentskills.io/specification)

## Related skills

`file-search` can help locate repository-specific configuration. `new-skill` owns revisions to this skill. Neither replaces the DDEV/TYPO3 workflow here.

## License

No license has been assigned. Treat the skill as private unless the owner adds one.

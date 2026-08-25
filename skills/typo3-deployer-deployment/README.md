# TYPO3 Deployer deployment

This skill configures Deployer 8 for Composer-based TYPO3 projects. It can create a recipe, detect and upgrade a Deployer 7 installation in place, and add a GitHub Actions deployment that authenticates to the target over SSH.

## What this skill solves

Deployer upgrades touch more than a Composer constraint. Deployer 8 requires PHP 8.3, changes several recipe APIs, and ships a different TYPO3 recipe configuration. CI adds a second source of mistakes around SSH keys, host verification, environment protections, and the exact revision being released. This skill handles those parts as one reviewed workflow while keeping the live deployment behind a separate authorization step.

## Use when

- A Composer-based TYPO3 project needs a new Deployer 8 recipe.
- `composer.json`, `composer.lock`, or `vendor/bin/dep` still reports Deployer 7 and the project must move to v8 without resetting its releases.
- A repository needs a GitHub Actions workflow that invokes `vendor/bin/dep` against staging or production.
- An existing Deployer 8 setup needs its TYPO3 shared paths, SSH handling, workflow controls, or validation repaired.

Do not use this skill for TYPO3 core upgrades, general server provisioning, Kubernetes or container-platform releases, or a project that has deliberately chosen another deployment tool.

## Expected outputs

- A Deployer state report with the installed, locked, and constrained versions.
- Updated `composer.json` and `composer.lock` resolving `deployer/deployer:^8.0` when an upgrade is requested.
- A reviewed `deploy.php` based on `recipe/typo3.php` and Deployer 8 configuration names.
- `.github/workflows/deploy-typo3.yml` plus `.github/scripts/configure-deployer-ssh.sh` when CI deployment is requested.
- A list of required GitHub environment secrets and variables. Secret values never appear in committed files.
- Validation evidence. A live deployment occurs only when the user separately asks for it.

## Context requirements

The agent needs the project root and access to its Composer files, Deployer recipe, deployment docs, and workflows. A full v8 install or upgrade requires PHP 8.3 or later, Composer 2, Git, and network access to Packagist. CI setup requires the deployment host, SSH user, port, Deployer selector, deployment URL, and repository administrator access to configure the GitHub environment.

For an actual deployment, the user must supply or configure the deployment credentials outside Git and authorize the target environment explicitly.

## Installation

The skill follows the portable Agent Skills format.

- Codex, Cursor, Antigravity, and compatible project clients: place it at `.agents/skills/typo3-deployer-deployment/`.
- Codex user installation: place it at `~/.agents/skills/typo3-deployer-deployment/`.
- Claude Code project installation: place it at `.claude/skills/typo3-deployer-deployment/`.
- OpenCode project installation: place it at `.opencode/skills/typo3-deployer-deployment/` or `.agents/skills/typo3-deployer-deployment/`.
- ChatGPT Desktop: upload the complete directory or a ZIP through Plugins, Skills, Create.

The included GitHub workflow expects `configure-ci-ssh.sh` to be copied into the target repository at `.github/scripts/configure-deployer-ssh.sh`. A globally installed skill is not available on a GitHub runner unless its required script is copied into the repository.

## Example prompts

- "Set up Deployer 8 for this TYPO3 project. Keep `.env` and `public/fileadmin` shared, add a production host, and validate the recipe without deploying."
- "This project has `deployer/deployer` 7.4 in `require-dev`. Upgrade it in place to Deployer 8, migrate the custom `run()` calls, and preserve the current release layout."
- "Add a manual GitHub Action that deploys this TYPO3 project to production with Deployer 8. Use environment secrets, a pinned SSH host key, and a protected production environment."
- "Audit our Deployer 8 workflow. Check that CI deploys the checked-out commit and cannot run two production releases at once."

## GitHub environment contract

The workflow template uses a GitHub environment named `production`.

Environment secrets:

- `DEPLOY_SSH_PRIVATE_KEY`: dedicated unencrypted OpenSSH private key for the deployment user.
- `DEPLOY_KNOWN_HOSTS`: verified `known_hosts` line for the target host and port.

Environment variables:

- `DEPLOY_HOST`: DNS name or IP used by the Deployer recipe.
- `DEPLOY_USER`: remote deployment user.
- `DEPLOY_PORT`: SSH port, normally `22`.
- `DEPLOYER_SELECTOR`: Deployer host alias or label selector, such as `production`.
- `DEPLOY_URL`: public URL shown in GitHub's deployment view.

See [the GitHub Actions guide](references/github-actions.md) for key creation, host fingerprint verification, environment protections, and workflow installation.

## Validation

From the repository containing this skill:

```bash
/path/to/new-skill/scripts/validate-skill.sh .agents/skills/typo3-deployer-deployment --strict-portable
skills-ref validate .agents/skills/typo3-deployer-deployment
bash .agents/skills/typo3-deployer-deployment/scripts/tests/test-scripts.sh
```

The structural validator checks frontmatter, links, documentation, and support files. The script test uses temporary fixtures and a fake Composer executable. It does not contact a server or Packagist.

For a project configured by the skill, also run the validation commands in `SKILL.md`. Use `actionlint` and `shellcheck` when installed.

## Related skills

- `typo3-v12-to-v13-upgrade` and `typo3-v13-to-v14-upgrade` handle TYPO3 core compatibility. They do not own deployment setup.
- `new-skill` maintains the skill structure and evaluation files. It does not perform deployments.

## Primary references

- [Deployer 8 getting started](https://deployer.org/docs/8.x/getting-started)
- [Deployer 8 TYPO3 recipe](https://deployer.org/docs/8.x/recipe/typo3)
- [Deployer 7 to 8 upgrade guide](https://github.com/deployphp/deployer/blob/master/docs/UPGRADE.md)
- [GitHub Actions deployment environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments)
- [GitHub Actions secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)

Sources were checked on 2026-08-25.

## License

Licensed under [CC BY 4.0](../../LICENSE).

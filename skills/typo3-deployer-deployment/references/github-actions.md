# Deploy TYPO3 with GitHub Actions

Read this file when a GitHub-hosted or self-hosted runner will call Deployer.

## Authentication model

Keep the two possible SSH connections separate.

1. The GitHub runner connects to the deployment host. This always needs a private key on the runner, its public key in the deployment user's `authorized_keys`, and a verified host key.
2. The deployment host may connect to GitHub when Deployer clones or archives a remote repository. Deployer 8's `local_archive` strategy avoids this second credential by uploading the runner's checkout.

Use a dedicated Ed25519 key for each repository and environment. Generate it on a trusted machine:

```bash
ssh-keygen -t ed25519 -f typo3-production-actions -C 'github-actions:OWNER/REPOSITORY:production'
```

Use an unencrypted key because the non-interactive runner cannot answer a passphrase prompt. Compensate with a dedicated deployment account, narrow server permissions, protected GitHub environment access, key rotation, and audit logs. Add only the `.pub` file to the deployment user's `authorized_keys`.

Collect the host key with the real host and port:

```bash
ssh-keyscan -H -p 22 www.example.org > production_known_hosts
ssh-keygen -lf production_known_hosts
```

`ssh-keyscan` does not authenticate the server. Compare the displayed fingerprint with a value obtained through the hosting control panel, server console, or an administrator on another trusted channel. Store the verified file contents, not only the fingerprint.

## GitHub environment

Create an environment named `production` before enabling the workflow. Restrict it to the intended protected branch or tags and add required reviewers for a live site. GitHub withholds environment secrets until protection rules pass.

Add these environment secrets:

- `DEPLOY_SSH_PRIVATE_KEY`: contents of `typo3-production-actions`.
- `DEPLOY_KNOWN_HOSTS`: contents of `production_known_hosts`.

Add these environment variables:

- `DEPLOY_HOST`: the host name recorded in `known_hosts` and used by the recipe.
- `DEPLOY_USER`: the SSH deployment user.
- `DEPLOY_PORT`: the SSH port.
- `DEPLOYER_SELECTOR`: the exact alias or label selector passed to Deployer.
- `DEPLOY_URL`: the deployed site's HTTPS URL.

With GitHub CLI, secrets can be read from files without placing them on the command line:

```bash
gh secret set --env production DEPLOY_SSH_PRIVATE_KEY < typo3-production-actions
gh secret set --env production DEPLOY_KNOWN_HOSTS < production_known_hosts
```

Use GitHub's environment settings UI for variables, or `gh variable set` after checking the installed CLI's syntax. Never print the secret values to confirm them.

## Install the workflow files

Copy the supplied files into the target repository:

```bash
mkdir -p .github/workflows .github/scripts
cp templates/deploy-typo3.yml .github/workflows/deploy-typo3.yml
cp scripts/configure-ci-ssh.sh .github/scripts/configure-deployer-ssh.sh
chmod 0755 .github/scripts/configure-deployer-ssh.sh
```

Then adapt the workflow's environment name, branch guard, validation commands, build step, and Deployer selector contract. Keep `permissions: contents: read`, one deployment concurrency group, a bounded timeout, and `cancel-in-progress: false`. Canceling a running deployment can leave a lock or a half-completed release.

The template pins external actions to full commit SHAs. When updating a pin, verify that the commit belongs to the action's official repository and record the matching release tag in the comment.

## Recipe setting for CI

Make the checked-out Git revision the deployment source:

```php
set('update_code_strategy', getenv('CI') ? 'local_archive' : 'archive');
```

Build all release assets before invoking Deployer so `local_archive` includes them. Do not edit generated artifacts by hand. If the project builds on the target instead, add a reviewed Deployer task with explicit tool versions and resource limits.

## Workflow call

The deployment step must quote the selector and call the Composer-installed binary:

```bash
vendor/bin/dep deploy "$DEPLOYER_SELECTOR" --no-interaction -vvv
```

Before that call, the workflow checks that the binary reports major version 8, validates the SSH material with `configure-deployer-ssh.sh --verify`, and loads the recipe task tree. Do not add `--no-interaction` to hide missing recipe values. Resolve every required value before the deployment step.

## Security review

- Do not trigger a secret-bearing deployment from `pull_request`, `pull_request_target`, Dependabot, or untrusted forks.
- Protect the workflow and copied SSH script through branch review. Code in either file can read the runner's deployment key.
- Scope secrets to the deployment environment rather than the whole repository when the GitHub plan supports it.
- Keep the default `GITHUB_TOKEN` permission read-only.
- Pin third-party actions to full commit SHAs.
- Use a self-hosted runner only when its persistence, network access, and cleanup policy have been reviewed. Environment secrets do not make a self-hosted runner isolated.
- Never disable SSH host checking. A changed host key must stop the job and prompt an infrastructure investigation.

## Validation and first run

Validate locally:

```bash
bash -n .github/scripts/configure-deployer-ssh.sh
ruby -e 'require "yaml"; YAML.parse_file(ARGV.fetch(0))' .github/workflows/deploy-typo3.yml
actionlint .github/workflows/deploy-typo3.yml
shellcheck .github/scripts/configure-deployer-ssh.sh
```

`actionlint` and `shellcheck` are optional tools, but fix their findings when available. The first workflow run should use `workflow_dispatch`, a protected environment approval, and a known rollback target. Watch the complete Deployer output. Verify the public URL and current release before considering the run complete.

## Sources

- [Using secrets in GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)
- [Deploying with GitHub Actions](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments)
- [Deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Deployer 8 hosts](https://deployer.org/docs/8.x/hosts)
- [Deployer 8 update code recipe](https://deployer.org/docs/8.x/recipe/deploy/update_code)

Checked on 2026-08-25.

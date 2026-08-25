#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf 'test-scripts: %s\n' "$1" >&2
  exit 1
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
fixture_root="$(mktemp -d "${TMPDIR:-/tmp}/typo3-deployer-skill-test.XXXXXX")"
trap 'rm -rf "$fixture_root"' EXIT

create_v7_fixture() {
  local target="$1"
  mkdir -p "$target"
  printf '%s\n' \
    '{' \
    '  "name": "example/typo3-project",' \
    '  "require-dev": {' \
    '    "deployer/deployer": "7.4.1"' \
    '  }' \
    '}' > "$target/composer.json"
  printf '%s\n' \
    '{' \
    '  "packages": [],' \
    '  "packages-dev": [' \
    '    {"name": "deployer/deployer", "version": "v7.4.1"}' \
    '  ]' \
    '}' > "$target/composer.lock"
  printf '%s\n' \
    '<?php' \
    'namespace Deployer;' \
    "require 'recipe/typo3.php';" \
    "set('typo3_webroot', 'public');" \
    "set('shared_dirs', []);" \
    "task('legacy', function (): void {" \
    "    run('sync', ['timeout' => 5, 'no_throw' => true]);" \
    '});' > "$target/deploy.php"
}

fixture="$fixture_root/project"
create_v7_fixture "$fixture"

inspection="$(php "$script_dir/inspect-deployer.php" --project-root "$fixture" --format json)"
grep -q '"state": "v7"' <<<"$inspection" || fail 'inspector did not detect v7'
grep -q '"id": "run-options-array"' <<<"$inspection" || fail 'inspector missed run options array'
grep -q '"id": "typo3-webroot-v7"' <<<"$inspection" || fail 'inspector missed typo3_webroot'

fake_composer="$fixture_root/fake-composer"
# shellcheck disable=SC2016
printf '%s\n' \
  '#!/usr/bin/env bash' \
  'set -euo pipefail' \
  'if [[ "${1:-}" == "prohibits" ]]; then' \
  '  exit 0' \
  'fi' \
  '[[ "${1:-}" == "require" ]] || exit 9' \
  "php -r '\$path = \"composer.json\"; \$data = json_decode(file_get_contents(\$path), true, 512, JSON_THROW_ON_ERROR); \$data[\"require-dev\"][\"deployer/deployer\"] = \"^8.0\"; file_put_contents(\$path, json_encode(\$data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . PHP_EOL);'" \
  "php -r '\$data = [\"packages\" => [], \"packages-dev\" => [[\"name\" => \"deployer/deployer\", \"version\" => \"v8.0.5\"]]]; file_put_contents(\"composer.lock\", json_encode(\$data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . PHP_EOL);'" > "$fake_composer"
chmod 0755 "$fake_composer"

"$script_dir/upgrade-deployer-v8.sh" --project-root "$fixture" --composer "$fake_composer" --apply >/dev/null
updated="$(php "$script_dir/inspect-deployer.php" --project-root "$fixture" --format json)"
grep -q '"state": "v8"' <<<"$updated" || fail 'upgrader did not produce a v8 lock state'

rollback_fixture="$fixture_root/rollback-project"
create_v7_fixture "$rollback_fixture"
before_json="$(shasum -a 256 "$rollback_fixture/composer.json" | awk '{print $1}')"
before_lock="$(shasum -a 256 "$rollback_fixture/composer.lock" | awk '{print $1}')"
failing_composer="$fixture_root/failing-composer"
# shellcheck disable=SC2016
printf '%s\n' \
  '#!/usr/bin/env bash' \
  'set -euo pipefail' \
  'if [[ "${1:-}" == "prohibits" ]]; then exit 0; fi' \
  'printf "broken\n" > composer.json' \
  'exit 1' > "$failing_composer"
chmod 0755 "$failing_composer"

if "$script_dir/upgrade-deployer-v8.sh" --project-root "$rollback_fixture" --composer "$failing_composer" --apply >/dev/null 2>&1; then
  fail 'upgrader unexpectedly accepted a failing Composer run'
fi
after_json="$(shasum -a 256 "$rollback_fixture/composer.json" | awk '{print $1}')"
after_lock="$(shasum -a 256 "$rollback_fixture/composer.lock" | awk '{print $1}')"
[[ "$before_json" == "$after_json" ]] || fail 'composer.json was not restored after failure'
[[ "$before_lock" == "$after_lock" ]] || fail 'composer.lock was not restored after failure'

ssh_fixture="$fixture_root/ssh"
mkdir -p "$ssh_fixture"
ssh-keygen -q -t ed25519 -N '' -f "$fixture_root/deploy_key"
ssh-keygen -q -t ed25519 -N '' -f "$fixture_root/host_key"
host_key_fields="$(awk '{print $1 " " $2}' "$fixture_root/host_key.pub")"
known_hosts_line="example.test $host_key_fields"

DEPLOY_SSH_DIR="$ssh_fixture" \
DEPLOY_SSH_PRIVATE_KEY="$(<"$fixture_root/deploy_key")" \
DEPLOY_KNOWN_HOSTS="$known_hosts_line" \
DEPLOY_HOST='example.test' \
DEPLOY_USER='deployer' \
DEPLOY_PORT='22' \
  "$script_dir/configure-ci-ssh.sh" >/dev/null

[[ -f "$ssh_fixture/id_ed25519" ]] || fail 'SSH helper did not write the private key'
[[ -f "$ssh_fixture/known_hosts" ]] || fail 'SSH helper did not write known_hosts'
ssh-keygen -F example.test -f "$ssh_fixture/known_hosts" >/dev/null || fail 'SSH helper lost the expected host entry'

printf '%s\n' 'All script tests passed.'

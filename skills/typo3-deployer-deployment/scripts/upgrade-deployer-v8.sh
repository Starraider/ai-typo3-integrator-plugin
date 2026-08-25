#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' \
    'Usage: upgrade-deployer-v8.sh [--project-root PATH] [--composer PATH] [--apply]' \
    '' \
    'Without --apply, inspect the project and print the Composer command.' \
    'With --apply, upgrade a detected Deployer 7 dependency to ^8.0.' \
    'Composer files are restored if the update or version check fails.'
}

fail() {
  printf 'upgrade-deployer-v8: %s\n' "$1" >&2
  exit "${2:-1}"
}

project_root='.'
composer_bin='composer'
apply=0

while (($# > 0)); do
  case "$1" in
    --project-root)
      (($# >= 2)) || fail '--project-root requires a value' 2
      project_root="$2"
      shift 2
      ;;
    --project-root=*)
      project_root="${1#*=}"
      shift
      ;;
    --composer)
      (($# >= 2)) || fail '--composer requires a value' 2
      composer_bin="$2"
      shift 2
      ;;
    --composer=*)
      composer_bin="${1#*=}"
      shift
      ;;
    --apply)
      apply=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      fail "unknown argument: $1" 2
      ;;
  esac
done

project_root="$(cd "$project_root" && pwd -P)" || fail "project root does not exist: $project_root" 2
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
inspector="$script_dir/inspect-deployer.php"

[[ -f "$project_root/composer.json" ]] || fail "composer.json not found under $project_root" 2
[[ -x "$inspector" || -f "$inspector" ]] || fail "inspector not found: $inspector" 2

report="$(php "$inspector" --project-root "$project_root" --format json)"

json_value() {
  local path="$1"
  # shellcheck disable=SC2016
  php -r '
    $data = json_decode(stream_get_contents(STDIN), true, 512, JSON_THROW_ON_ERROR);
    $value = $data;
    foreach (explode(".", $argv[1]) as $part) {
        $value = is_array($value) && array_key_exists($part, $value) ? $value[$part] : null;
    }
    if (is_bool($value)) {
        echo $value ? "true" : "false";
    } elseif ($value !== null) {
        echo $value;
    }
  ' "$path" <<<"$report"
}

state="$(json_value deployer.state)"
constraint="$(json_value deployer.constraint)"
constraint_section="$(json_value deployer.constraint_section)"
php_supported="$(json_value php.supports_deployer_8)"

printf 'Detected Deployer state: %s\n' "$state"
printf 'Composer constraint: %s\n' "${constraint:-none}"
printf 'PHP supports Deployer 8: %s\n' "$php_supported"

case "$state" in
  v8)
    printf '%s\n' 'Deployer 8 is already resolved. No Composer change is needed.'
    exit 0
    ;;
  v7|mixed)
    ;;
  absent)
    fail 'no existing Deployer installation was detected; use the new-install workflow instead' 3
    ;;
  *)
    fail 'the Deployer major version is unknown; resolve conflicting or missing version evidence first' 3
    ;;
esac

[[ "$php_supported" == 'true' ]] || fail 'Deployer 8 requires PHP 8.3 or later' 4

if [[ "$constraint_section" == 'require' ]]; then
  require_args=('require' 'deployer/deployer:^8.0' '--with-all-dependencies' '--no-interaction')
else
  require_args=('require' '--dev' 'deployer/deployer:^8.0' '--with-all-dependencies' '--no-interaction')
fi

printf 'Planned command in %s: ' "$project_root"
printf '%q ' "$composer_bin" "${require_args[@]}"
printf '\n'

if ((apply == 0)); then
  printf '%s\n' 'Dry run only. Review recipe findings, then rerun with --apply.'
  php "$inspector" --project-root "$project_root" --format text
  exit 0
fi

command -v "$composer_bin" >/dev/null 2>&1 || [[ -x "$composer_bin" ]] || fail "Composer executable not found: $composer_bin" 5

(
  cd "$project_root"
  "$composer_bin" prohibits 'deployer/deployer' '^8.0' || true
)

backup_dir="$(mktemp -d "${TMPDIR:-/tmp}/deployer-v8-upgrade.XXXXXX")"
had_lock=0
cp "$project_root/composer.json" "$backup_dir/composer.json"
if [[ -f "$project_root/composer.lock" ]]; then
  cp "$project_root/composer.lock" "$backup_dir/composer.lock"
  had_lock=1
fi

restore_composer_files() {
  cp "$backup_dir/composer.json" "$project_root/composer.json"
  if ((had_lock == 1)); then
    cp "$backup_dir/composer.lock" "$project_root/composer.lock"
  elif [[ -f "$project_root/composer.lock" ]]; then
    rm "$project_root/composer.lock"
  fi
}

cleanup_backup() {
  rm -rf "$backup_dir"
}

trap cleanup_backup EXIT

if ! (
  cd "$project_root"
  "$composer_bin" "${require_args[@]}"
); then
  restore_composer_files
  fail 'Composer failed; restored composer.json and composer.lock' 6
fi

if ! updated_report="$(php "$inspector" --project-root "$project_root" --format json)"; then
  restore_composer_files
  fail 'could not verify the Composer result; restored Composer files' 7
fi
# shellcheck disable=SC2016
if ! updated_state="$(php -r '
  $data = json_decode(stream_get_contents(STDIN), true, 512, JSON_THROW_ON_ERROR);
  echo $data["deployer"]["state"] ?? "unknown";
' <<<"$updated_report")"; then
  restore_composer_files
  fail 'could not read the verified Deployer state; restored Composer files' 7
fi

if [[ "$updated_state" != 'v8' ]]; then
  restore_composer_files
  fail "Composer completed but Deployer state is $updated_state; restored Composer files" 7
fi

printf '%s\n' 'Composer dependency upgraded to Deployer 8.'
printf '%s\n' 'Review and migrate every recipe finding before running a deployment:'
php "$inspector" --project-root "$project_root" --format text

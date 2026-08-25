#!/usr/bin/env bash
set -euo pipefail
set +x

usage() {
  printf '%s\n' \
    'Usage: configure-ci-ssh.sh [--verify]' \
    '' \
    'Required environment variables:' \
    '  DEPLOY_SSH_PRIVATE_KEY  Dedicated unencrypted OpenSSH private key' \
    '  DEPLOY_KNOWN_HOSTS      Preverified known_hosts content' \
    '  DEPLOY_HOST             Hostname or IP in the Deployer recipe' \
    '  DEPLOY_USER             Remote deployment user' \
    '' \
    'Optional environment variable:' \
    '  DEPLOY_PORT             SSH port, default 22' \
    '  DEPLOY_SSH_DIR          SSH directory, default user .ssh directory' \
    '' \
    '--verify opens a non-interactive SSH connection and runs true.'
}

fail() {
  printf 'configure-ci-ssh: %s\n' "$1" >&2
  exit "${2:-1}"
}

verify=0
while (($# > 0)); do
  case "$1" in
    --verify)
      verify=1
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

: "${DEPLOY_SSH_PRIVATE_KEY:?DEPLOY_SSH_PRIVATE_KEY is required}"
: "${DEPLOY_KNOWN_HOSTS:?DEPLOY_KNOWN_HOSTS is required}"
: "${DEPLOY_HOST:?DEPLOY_HOST is required}"
: "${DEPLOY_USER:?DEPLOY_USER is required}"
DEPLOY_PORT="${DEPLOY_PORT:-22}"

[[ "$DEPLOY_PORT" =~ ^[0-9]+$ ]] || fail 'DEPLOY_PORT must be numeric' 2
((DEPLOY_PORT >= 1 && DEPLOY_PORT <= 65535)) || fail 'DEPLOY_PORT must be between 1 and 65535' 2

ssh_dir="${DEPLOY_SSH_DIR:-$HOME/.ssh}"
private_key="$ssh_dir/id_ed25519"
known_hosts="$ssh_dir/known_hosts"
ssh_config="$ssh_dir/config"

install -d -m 0700 "$ssh_dir"
for target in "$private_key" "$known_hosts" "$ssh_config"; do
  [[ ! -e "$target" ]] || fail "refusing to overwrite existing file: $target" 3
done

umask 077
printf '%s\n' "$DEPLOY_SSH_PRIVATE_KEY" | sed 's/\r$//' > "$private_key"
printf '%s\n' "$DEPLOY_KNOWN_HOSTS" | sed 's/\r$//' > "$known_hosts"
printf '%s\n' \
  'Host *' \
  '  BatchMode yes' \
  '  IdentitiesOnly yes' \
  "  IdentityFile $private_key" \
  '  StrictHostKeyChecking yes' \
  "  UserKnownHostsFile $known_hosts" > "$ssh_config"
chmod 0600 "$private_key" "$known_hosts" "$ssh_config"

ssh-keygen -y -P '' -f "$private_key" >/dev/null 2>&1 || fail 'private key is invalid or passphrase-protected' 4

host_lookup="$DEPLOY_HOST"
if [[ "$DEPLOY_PORT" != '22' ]]; then
  host_lookup="[$DEPLOY_HOST]:$DEPLOY_PORT"
fi
ssh-keygen -F "$host_lookup" -f "$known_hosts" >/dev/null 2>&1 || fail "known_hosts does not contain $host_lookup" 5

if ((verify == 1)); then
  ssh -F "$ssh_config" -p "$DEPLOY_PORT" -o ConnectTimeout=15 "$DEPLOY_USER@$DEPLOY_HOST" true
fi

printf 'SSH configured for %s@%s:%s with strict host checking.\n' "$DEPLOY_USER" "$DEPLOY_HOST" "$DEPLOY_PORT"

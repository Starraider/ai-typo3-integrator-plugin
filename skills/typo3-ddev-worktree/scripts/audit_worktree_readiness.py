#!/usr/bin/env python3
"""Read-only readiness audit for Composer-based DDEV TYPO3 worktrees."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None
    line: int | None = None
    remediation: str | None = None


TEXT_SUFFIXES = {".conf", ".env", ".json", ".toml", ".yaml", ".yml"}
HOST_RE = re.compile(r"(?i)\b(?:[a-z0-9-]+\.)+ddev\.site(?![a-z0-9-])")
ENV_REF_RE = re.compile(r"^%env\(([A-Za-z_][A-Za-z0-9_]*)\)%$")
TOP_LEVEL_NAME_RE = re.compile(r"^name\s*:\s*(\S.*?)\s*$")
TYPE_RE = re.compile(r"^type\s*:\s*['\"]?typo3['\"]?\s*(?:#.*)?$")
BASE_RE = re.compile(r"^\s*base\s*:\s*(.*?)\s*$")
FIXED_PORT_RE = re.compile(
    r"^(?:host_(?:https|webserver|db|mailpit)_port|router_(?:http|https)_port)\s*:\s*['\"]?\d+"
)
CONTAINER_RE = re.compile(r"^\s*container_name\s*:\s*(.*?)\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit a Composer-based DDEV TYPO3 project for Git worktree collisions."
    )
    parser.add_argument(
        "--project",
        default=".",
        help="Project directory to audit. Defaults to the current directory.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text.",
    )
    return parser.parse_args()


def clean_scalar(value: str) -> str:
    value = value.split(" #", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_lines(path: Path) -> list[str]:
    try:
        if path.stat().st_size > 2_000_000:
            return []
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except (OSError, UnicodeError):
        return []


def repository_files(root: Path) -> set[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return set()
    return {(root / line).resolve() for line in result.stdout.splitlines() if line}


def candidate_files(root: Path) -> Iterable[Path]:
    seen: set[Path] = set()
    paths: list[Path] = []
    included = repository_files(root)

    ddev = root / ".ddev"
    if ddev.is_dir():
        for path in ddev.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if path.resolve() not in included:
                continue
            if any(part in {"backup", "data"} for part in path.parts):
                continue
            paths.append(path)

    sites = root / "config" / "sites"
    if sites.is_dir():
        paths.extend(
            path for path in sites.glob("*/config.y*ml")
            if path.is_file() and path.resolve() in included
        )

    paths.extend(
        path for path in root.glob(".env*")
        if path.is_file() and path.resolve() in included
    )

    for path in sorted(paths):
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        try:
            resolved.relative_to(root)
        except ValueError:
            continue
        yield path


def git_root(project: Path) -> Path | None:
    result = subprocess.run(
        ["git", "-C", str(project), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


def read_env_values(root: Path) -> dict[str, tuple[str, Path, int]]:
    values: dict[str, tuple[str, Path, int]] = {}
    for path in sorted(root.glob(".env*")):
        if not path.is_file():
            continue
        for number, raw in enumerate(read_lines(path), start=1):
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
                values[key] = (clean_scalar(value), path, number)
    return values


def audit(project: Path) -> tuple[Path, list[Finding]]:
    requested = project.expanduser().resolve()
    findings: list[Finding] = []

    if not requested.is_dir():
        return requested, [
            Finding("blocker", "project-missing", "Project directory does not exist.", str(requested))
        ]

    root = git_root(requested)
    if root is None:
        return requested, [
            Finding("blocker", "not-git", "Project is not inside a Git worktree.", str(requested))
        ]

    config = root / ".ddev" / "config.yaml"
    if not config.is_file():
        return root, [
            Finding("blocker", "ddev-config-missing", "Missing .ddev/config.yaml.", ".ddev/config.yaml")
        ]

    config_lines = read_lines(config)
    if not any(TYPE_RE.match(line) for line in config_lines):
        findings.append(
            Finding(
                "blocker",
                "not-ddev-typo3",
                "DDEV config does not declare type: typo3.",
                ".ddev/config.yaml",
                remediation="Use this skill only for DDEV TYPO3 projects or correct the project type.",
            )
        )

    if not (root / "composer.json").is_file():
        findings.append(
            Finding(
                "blocker",
                "composer-missing",
                "Missing composer.json at the Git worktree root.",
                "composer.json",
            )
        )

    for number, raw in enumerate(config_lines, start=1):
        if raw.startswith((" ", "\t", "#")):
            continue
        if TOP_LEVEL_NAME_RE.match(raw):
            findings.append(
                Finding(
                    "blocker",
                    "fixed-ddev-name",
                    "Tracked DDEV config has a fixed top-level project name.",
                    ".ddev/config.yaml",
                    number,
                    "Remove the top-level name so DDEV derives it from each worktree directory.",
                )
            )
        if FIXED_PORT_RE.match(raw):
            findings.append(
                Finding(
                    "blocker",
                    "fixed-host-port",
                    "Tracked DDEV config reserves a fixed host or router port.",
                    ".ddev/config.yaml",
                    number,
                    "Remove the fixed port or document a tested per-worktree allocation strategy.",
                )
            )

    for ddev_yaml in sorted((root / ".ddev").glob("config*.y*ml")):
        in_fixed_hosts = False
        for number, raw in enumerate(read_lines(ddev_yaml), start=1):
            if re.match(r"^(additional_hostnames|additional_fqdns)\s*:\s*$", raw):
                in_fixed_hosts = True
                continue
            if in_fixed_hosts and raw and not raw.startswith((" ", "\t")):
                in_fixed_hosts = False
            if not in_fixed_hosts:
                continue
            match = re.match(r"^\s+-\s+(.+?)\s*$", raw)
            if not match:
                continue
            value = clean_scalar(match.group(1))
            if not value or "${" in value or value.startswith("#"):
                continue
            findings.append(
                Finding(
                    "blocker",
                    "fixed-additional-hostname",
                    f"Tracked DDEV config reserves the same additional hostname in every worktree: {value}.",
                    relative_path(ddev_yaml, root),
                    number,
                    "Generate the hostname per worktree or use an add-on configuration that derives it from DDEV_SITENAME.",
                )
            )

    env_values = read_env_values(root)
    site_configs = sorted((root / "config" / "sites").glob("*/config.y*ml"))
    if not site_configs:
        findings.append(
            Finding(
                "blocker",
                "site-config-missing",
                "No TYPO3 config/sites/*/config.yaml file was found.",
                "config/sites",
            )
        )

    for site_config in site_configs:
        found_base = False
        for number, raw in enumerate(read_lines(site_config), start=1):
            match = BASE_RE.match(raw)
            if not match:
                continue
            found_base = True
            base = clean_scalar(match.group(1))
            env_match = ENV_REF_RE.match(base)
            if base.startswith("/"):
                continue
            if env_match:
                variable = env_match.group(1)
                resolved = env_values.get(variable)
                if resolved is None:
                    findings.append(
                        Finding(
                            "warning",
                            "typo3-base-env-unresolved",
                            f"TYPO3 site base uses {variable}, but no root .env* definition was found.",
                            relative_path(site_config, root),
                            number,
                            "Verify that every worktree receives a relative or target-specific value.",
                        )
                    )
                elif resolved[0].startswith("/"):
                    continue
                else:
                    findings.append(
                        Finding(
                            "blocker",
                            "typo3-base-env-absolute",
                            f"TYPO3 site base variable {variable} resolves to a non-relative value in {relative_path(resolved[1], root)}.",
                            relative_path(resolved[1], root),
                            resolved[2],
                            "Use a relative local value or a generated per-worktree override.",
                        )
                    )
            elif re.match(r"(?i)^https?://", base):
                findings.append(
                    Finding(
                        "blocker",
                        "typo3-base-absolute",
                        "TYPO3 site base is an absolute URL and will not follow a worktree hostname.",
                        relative_path(site_config, root),
                        number,
                        "Use a relative base or keep the absolute production value outside local defaults.",
                    )
                )
            else:
                findings.append(
                    Finding(
                        "warning",
                        "typo3-base-unknown",
                        "TYPO3 site base is neither relative, an HTTP URL, nor a simple environment reference.",
                        relative_path(site_config, root),
                        number,
                        "Trace the value and prove that it resolves to the target worktree URL.",
                    )
                )
        if not found_base:
            findings.append(
                Finding(
                    "blocker",
                    "typo3-base-missing",
                    "TYPO3 site config has no base entry.",
                    relative_path(site_config, root),
                )
            )

    seen_hosts: set[tuple[str, int, str]] = set()
    for path in candidate_files(root):
        rel = relative_path(path, root)
        for number, raw in enumerate(read_lines(path), start=1):
            stripped = raw.strip()
            if not stripped or stripped.startswith("#"):
                continue

            container_match = CONTAINER_RE.match(raw)
            if container_match and "DDEV_SITENAME" not in container_match.group(1):
                findings.append(
                    Finding(
                        "blocker",
                        "fixed-container-name",
                        "Custom Compose service has a container_name that does not use DDEV_SITENAME.",
                        rel,
                        number,
                        "Use ddev-${DDEV_SITENAME}-<service> or remove container_name.",
                    )
                )

            for host in HOST_RE.findall(stripped):
                key = (rel, number, host.lower())
                if key in seen_hosts:
                    continue
                seen_hosts.add(key)
                findings.append(
                    Finding(
                        "blocker",
                        "fixed-ddev-hostname",
                        f"Tracked local configuration contains fixed DDEV hostname {host}.",
                        rel,
                        number,
                        "Derive the hostname from the worktree DDEV name or generate an ignored local override.",
                    )
                )

    if not any(re.match(r"^upload_dirs\s*:", line) for line in config_lines):
        findings.append(
            Finding(
                "warning",
                "upload-dirs-implicit",
                "DDEV upload_dirs is not explicit; confirm the TYPO3 file storage before cloning files.",
                ".ddev/config.yaml",
                remediation="Document or configure the intended upload directory, commonly public/fileadmin.",
            )
        )

    severity_order = {"blocker": 0, "warning": 1, "info": 2}
    findings.sort(
        key=lambda item: (
            severity_order.get(item.severity, 9),
            item.path or "",
            item.line or 0,
            item.code,
        )
    )
    return root, findings


def print_text(root: Path, findings: list[Finding]) -> None:
    blockers = sum(item.severity == "blocker" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)
    print(f"Project: {root}")
    print(f"Result: {blockers} blocker(s), {warnings} warning(s)")
    if not findings:
        print("READY: no worktree-readiness findings")
        return
    for item in findings:
        location = ""
        if item.path:
            location = f" {item.path}"
            if item.line:
                location += f":{item.line}"
        print(f"{item.severity.upper()} [{item.code}]{location}: {item.message}")
        if item.remediation:
            print(f"  Fix: {item.remediation}")


def main() -> int:
    args = parse_args()
    root, findings = audit(Path(args.project))
    blockers = sum(item.severity == "blocker" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "project": str(root),
                    "ready": blockers == 0,
                    "summary": {"blockers": blockers, "warnings": warnings},
                    "findings": [asdict(item) for item in findings],
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print_text(root, findings)

    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())

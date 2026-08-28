from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_worktree_readiness.py"


class AuditWorktreeReadinessTest(unittest.TestCase):
    def make_project(
        self,
        ddev_config: str = "type: typo3\n",
        site_config: str = "base: /\n",
        env: str | None = None,
        compose: str | None = None,
    ) -> Path:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, True)
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        (root / ".ddev").mkdir()
        (root / ".ddev" / "config.yaml").write_text(ddev_config, encoding="utf-8")
        (root / "composer.json").write_text("{}\n", encoding="utf-8")
        site = root / "config" / "sites" / "main"
        site.mkdir(parents=True)
        (site / "config.yaml").write_text(site_config, encoding="utf-8")
        if env is not None:
            (root / ".env").write_text(env, encoding="utf-8")
        if compose is not None:
            (root / ".ddev" / "docker-compose.extra.yaml").write_text(compose, encoding="utf-8")
        return root

    def run_audit(self, root: Path) -> tuple[int, dict]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--project", str(root), "--format", "json"],
            check=False,
            capture_output=True,
            text=True,
        )
        return result.returncode, json.loads(result.stdout)

    def test_relative_base_and_dynamic_container_are_ready(self) -> None:
        root = self.make_project(
            compose="services:\n  worker:\n    container_name: ddev-${DDEV_SITENAME}-worker\n"
        )
        code, report = self.run_audit(root)
        self.assertEqual(0, code)
        self.assertTrue(report["ready"])
        self.assertEqual(0, report["summary"]["blockers"])

    def test_fixed_identity_base_port_and_container_are_blockers(self) -> None:
        root = self.make_project(
            ddev_config="name: original\ntype: typo3\nhost_db_port: '3307'\nadditional_hostnames:\n  - vite.original\n",
            site_config="base: https://original.ddev.site/\n",
            compose="services:\n  worker:\n    container_name: original-worker\n",
        )
        code, report = self.run_audit(root)
        codes = {item["code"] for item in report["findings"]}
        self.assertEqual(1, code)
        self.assertFalse(report["ready"])
        self.assertTrue(
            {
                "fixed-ddev-name",
                "fixed-host-port",
                "fixed-additional-hostname",
                "typo3-base-absolute",
                "fixed-container-name",
                "fixed-ddev-hostname",
            }.issubset(codes)
        )

    def test_environment_backed_absolute_base_is_a_blocker(self) -> None:
        root = self.make_project(
            site_config="base: '%env(SITE_BASE)%'\n",
            env="SITE_BASE='https://original.ddev.site/'\n",
        )
        code, report = self.run_audit(root)
        codes = {item["code"] for item in report["findings"]}
        self.assertEqual(1, code)
        self.assertIn("typo3-base-env-absolute", codes)
        self.assertIn("fixed-ddev-hostname", codes)


if __name__ == "__main__":
    unittest.main()

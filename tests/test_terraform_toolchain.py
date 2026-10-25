import os
import json
import pathlib
import subprocess
import tempfile
import unittest

import yaml


class TerraformToolchainTests(unittest.TestCase):
    def check_pin(self, pin, requested="", lock=True, tracked=True, other_checkout=False):
        template = pathlib.Path(__file__).parents[1] / "tasks" / "terraform-toolchain.yml"
        script = yaml.safe_load(template.read_text())["steps"][0]["inputs"]["script"]
        with tempfile.TemporaryDirectory(prefix="ado-terraform-pin-") as temporary:
            directory = pathlib.Path(temporary)
            subprocess.run(["git", "init", "--quiet", str(directory)], check=True)
            if pin is not None:
                (directory / ".terraform-version").write_text(pin)
            if lock:
                (directory / ".terraform.lock.hcl").write_text("# Fixture lock\n")
            if tracked:
                subprocess.run(["git", "-C", str(directory), "add", "."], check=True)
            build_root = directory
            if other_checkout:
                build_root = directory / "other-checkout"
                subprocess.run(["git", "init", "--quiet", str(build_root)], check=True)
            program = directory / "verify.ps1"
            program.write_text(script)
            return subprocess.run(
                ["pwsh", "-NoProfile", "-NonInteractive", "-File", str(program)],
                env=dict(os.environ, TF_ROOT=str(directory), TF_REQUESTED_VERSION=requested,
                         BUILD_REPOSITORY_LOCALPATH=str(build_root)),
                capture_output=True, text=True)

    def test_selects_committed_exact_pin(self):
        result = self.check_pin("1.17.0\n")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("terraformSelectedVersion]1.17.0", result.stdout)

    def test_rejects_conflicting_explicit_version(self):
        result = self.check_pin("1.17.0", requested="1.15.8")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("does not match", result.stderr)

    def test_rejects_floating_or_missing_pin(self):
        for pin in ("latest", "1.17.x", "1.17.0-rc1", None):
            with self.subTest(pin=pin):
                self.assertNotEqual(0, self.check_pin(pin).returncode)

    def test_rejects_missing_or_untracked_lock(self):
        for lock, tracked in ((False, True), (True, False)):
            with self.subTest(lock=lock, tracked=tracked):
                self.assertNotEqual(0, self.check_pin("1.17.0", lock=lock, tracked=tracked).returncode)

    def test_rejects_a_different_checked_out_repository_before_execution(self):
        result = self.check_pin("1.17.0", other_checkout=True)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("triggering build repository", result.stderr)

    def test_receipt_records_actual_selection_without_private_inputs(self):
        template = pathlib.Path(__file__).parents[1] / "tasks" / "terraform-execution-receipt.yml"
        script = yaml.safe_load(template.read_text())["steps"][0]["inputs"]["script"]
        with tempfile.TemporaryDirectory(prefix="ado-terraform-receipt-") as temporary:
            directory = pathlib.Path(temporary)
            subprocess.run(["git", "init", "--quiet", str(directory)], check=True)
            (directory / ".terraform-version").write_text("1.17.0")
            (directory / ".terraform.lock.hcl").write_text("# Fixture lock\n")
            (directory / "terraform.tfstate").write_text("private fixture state")
            subprocess.run(["git", "-C", str(directory), "add", ".terraform-version", ".terraform.lock.hcl"], check=True)
            subprocess.run(["git", "-C", str(directory), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                            "commit", "--quiet", "-m", "fixture"], check=True)
            program = directory / "receipt.ps1"
            version = json.dumps({"terraform_version": "1.17.0", "platform": "linux_amd64",
                                  "provider_selections": {"registry.terraform.io/hashicorp/random": "3.9.1"}})
            program.write_text("function terraform { $global:LASTEXITCODE = 0; '" + version + "' }\n" + script)
            result = subprocess.run(
                ["pwsh", "-NoProfile", "-NonInteractive", "-File", str(program)],
                env=dict(os.environ, TF_ROOT=str(directory), TF_OPERATION="apply",
                         AGENT_TEMPDIRECTORY=str(directory), SYSTEM_JOBID="fixture-job", BUILD_BUILDID="42",
                         BUILD_REPOSITORY_NAME="fixture/repository", BUILD_SOURCEBRANCH="refs/heads/main",
                         BUILD_REPOSITORY_LOCALPATH=str(directory),
                         PRIVATE_FIXTURE_INPUT="never export this value"),
                capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            receipt_file, = directory.glob("terraform-execution-*.json")
            raw = receipt_file.read_text()
            receipt = json.loads(raw)
            self.assertEqual("1.17.0", receipt["terraformVersion"])
            self.assertEqual({"registry.terraform.io/hashicorp/random": "3.9.1"}, receipt["providerSelections"])
            self.assertEqual("apply", receipt["operation"])
            self.assertEqual("success", receipt["outcome"])
            self.assertNotIn("private fixture", raw)
            self.assertNotIn("never export", raw)
            self.assertEqual({
                "schemaVersion", "repository", "sourceCommit", "rootDirectory", "buildId", "job", "ref",
                "operation", "outcome", "observedAt", "terraformVersion", "platform", "providerSelections", "lockSha256"
            }, set(receipt))
            repeated = subprocess.run(
                ["pwsh", "-NoProfile", "-NonInteractive", "-File", str(program)],
                env=dict(os.environ, TF_ROOT=str(directory), TF_OPERATION="apply",
                         AGENT_TEMPDIRECTORY=str(directory), SYSTEM_JOBID="fixture-job", BUILD_BUILDID="42",
                         BUILD_REPOSITORY_NAME="fixture/repository", BUILD_SOURCEBRANCH="refs/heads/main",
                         BUILD_REPOSITORY_LOCALPATH=str(directory)),
                capture_output=True, text=True)
            self.assertEqual(0, repeated.returncode, repeated.stderr)
            self.assertEqual(2, len(list(directory.glob("terraform-execution-*.json"))))


if __name__ == "__main__":
    unittest.main()

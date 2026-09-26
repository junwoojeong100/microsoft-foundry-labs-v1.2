import csv
import hashlib
import io
import json
import re
import unittest

from . import ROOT

ARTIFACTS = ROOT / "docs/assets/live-guide-audit-20260926"


class LiveGuideAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = json.loads((ARTIFACTS / "results.json").read_text())
        cls.matrix = json.loads((ARTIFACTS / "guide-checks.json").read_text())

    def test_all_lab_and_workbook_statuses_are_explicit_without_an_all_pass_claim(self):
        rows = self.matrix["guides"]
        self.assertEqual(len(rows), 62)
        self.assertEqual(len({row["guide"] for row in rows}), 62)
        allowed = {
            "verified",
            "partial",
            "blocked",
            "design-only",
            "verified-audit-handoff",
            "reviewed-not-run",
            "verified-local",
            "verified-delivery",
            "blocked-after-probe",
            "blocked-before-write",
        }
        for language, directory in (("en", "docs"), ("ko", "docs/ko")):
            expected = {
                path.relative_to(ROOT).as_posix()
                for path in (ROOT / directory / "labs").rglob("*.md")
            }
            expected |= {
                f"{directory}/reference/{name}.md"
                for name in ("evaluation-workbook", "iq-workbook")
            }
            selected = [row for row in rows if row["language"] == language]
            self.assertEqual({row["guide"] for row in selected}, expected)
            for row in selected:
                self.assertIn(row["status"], allowed)
                self.assertTrue(row["detail"])
        for field in (
            "default_subscription_changed",
            "roles_assigned",
            "company_or_microsoft365_data_accessed",
            "all_features_live_verified",
            "human_acceptance_granted",
            "new_recording_created",
        ):
            self.assertIs(self.results[field], False)

    def test_independent_real_cohorts_keep_complete_denominators_and_acceptance_limits(self):
        all_ids = set()
        for language in ("en", "ko"):
            evidence = self.results["languages"][language]["evidence"]
            for label, total in (("baseline", 6), ("candidate", 6), ("final-holdout", 4)):
                raw = evidence[f"outputs/{label}/responses.jsonl"]
                self.assertEqual(
                    hashlib.sha256(raw["content"].encode()).hexdigest(), raw["source_sha256"]
                )
                rows = [json.loads(line) for line in raw["content"].splitlines()]
                self.assertEqual(len(rows), total)
                self.assertEqual(len({row["case_id"] for row in rows}), total)
                self.assertTrue(all(row["status"] == "ok" for row in rows))
                ids = {row["response_id"] for row in rows}
                self.assertTrue(all(ids))
                self.assertTrue(all_ids.isdisjoint(ids))
                all_ids |= ids
                manifest = evidence[f"outputs/{label}/manifest.json"]["content"]
                self.assertEqual(manifest["mode"], "live")
                self.assertEqual(manifest["language"], language)
                grade = evidence[f"outputs/{label}/business-evaluation.json"]["content"]
                self.assertEqual(
                    (grade["total"], grade["passed"], grade["errors"]), (total, total, 0)
                )
            verdict = evidence["outputs/final-holdout/acceptance.json"]["content"]
            self.assertEqual(verdict["recommendation"], "ready-for-human-review")
            self.assertIs(verdict["deployment_approved"], False)

    def test_browser_evidence_and_review_are_not_a_human_approval_or_translated_response(self):
        all_ids = set()
        for language in ("en", "ko"):
            browser = self.results["browser"]
            snapshot = browser[f"{language}-instructions-baseline.json"]["content"]
            source = ROOT / "data/learner" / language / "instructions-with-policies.txt"
            self.assertEqual(
                snapshot["instructions_sha256"], hashlib.sha256(source.read_bytes()).hexdigest()
            )
            self.assertEqual(snapshot["instructions_text"], source.read_text())
            for stage, total in (("lab03", 4), ("lab07", 6)):
                batch = browser[f"{language}-{stage}-responses.json"]["content"]
                self.assertEqual(batch["agent_version"], "2")
                self.assertEqual(batch["language"], language)
                self.assertEqual(batch["expected_count"], total)
                self.assertEqual(len(batch["responses"]), total)
                ids = {row["response_id"] for row in batch["responses"]}
                self.assertTrue(all_ids.isdisjoint(ids))
                all_ids |= ids
            reviewed = self.results["languages"][language]["browser_review"]
            self.assertEqual(reviewed["human_authorization"], "not-granted")
            self.assertTrue(reviewed["not_a_learner_pilot"])
            csv_text = self.results["languages"][language]["browser_assessment"]["content"]
            rows = list(csv.DictReader(io.StringIO(csv_text.lstrip("\ufeff"))))
            self.assertEqual(len(rows), 6)
            self.assertTrue(all("not human approval" in row["review_note"] for row in rows))

    def test_real_deployments_and_idle_sessions_are_distinct_language_evidence(self):
        checks = (
            ("en", "e08-show", "e08-session-status", "mfv2-live260926-en-hosted"),
            ("ko", "k08-show", "k08-idle-check", "mfv2-live260926-ko-hosted"),
            ("en", "ex-workflow-show", "ex-workflow-session-status", "mfv2-live260926-en-workflow"),
        )
        sessions = set()
        for language, show, status, name in checks:
            evidence = self.results["languages"][language]["evidence"]
            agent = evidence[f"outputs/live-audit/{show}/stdout.txt"]["content"]
            session = evidence[f"outputs/live-audit/{status}/stdout.txt"]["content"]
            self.assertEqual(
                (agent["name"], agent["version"], agent["status"]), (name, "1", "active")
            )
            self.assertEqual(agent["definition"]["kind"], "hosted")
            self.assertEqual(session["status"], "idle")
            self.assertNotIn(session["agent_session_id"], sessions)
            sessions.add(session["agent_session_id"])

    def test_actual_failures_and_unpinned_evaluator_versions_remain_visible(self):
        english = self.results["languages"]["en"]
        evidence = english["evidence"]
        failure = evidence["outputs/toolbox-runs/toolbox-direct-query/failure.json"]["content"]
        self.assertIn("Access denied", failure["message"])
        self.assertIs(failure["fallback_used"], False)
        failure = evidence["outputs/openapi-runs/openapi-policy/service-error.json"]["content"]
        self.assertEqual(failure["status_code"], 400)
        self.assertIn("403", failure["response_body"])
        self.assertIs(failure["provider_fallback_used"], False)
        self.assertTrue(any(row["exit_code"] != 0 for row in english["command_receipts"]))
        for language in ("en", "ko"):
            result = self.results["languages"][language]["evidence"][
                f"outputs/learner-notes-{language}/maf-tool-evaluation.json"
            ]["content"]
            self.assertIs(result["evaluator_versions_pinned"], False)
        for row in self.matrix["guides"]:
            if row["guide"].endswith("evaluation-workbook.md"):
                self.assertEqual(row["status"], "blocked")
        for record in self.results["browser"].values():
            self.assertRegex(record["source_sha256"], r"^[a-f0-9]{64}$")
        self.assertRegex(self.results["source_commit"], r"^[a-f0-9]{40}$")
        text = (ARTIFACTS / "results.json").read_text()
        self.assertIsNone(
            re.search(r"/Users/|@MngEnv|access_token|refresh_token|BEGIN PRIVATE KEY", text)
        )

    def test_live_report_is_linked_from_each_languages_current_evidence_pages(self):
        for directory in ("docs", "docs/ko"):
            for name in (
                "coverage.md",
                "live-run.md",
                "reference/validation.md",
                "labs/08-hosted.md",
            ):
                text = (ROOT / directory / name).read_text()
                self.assertIn("live-audit-20260926.md", text)
            report = (ROOT / directory / "reference/live-audit-20260926.md").read_text()
            self.assertIn("guide-checks.json", report)
            self.assertIn("results.json", report)
            self.assertIn("OutputQuality", report)

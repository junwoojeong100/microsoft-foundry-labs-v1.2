import hashlib
import json
import unittest

from foundry_workshop.profiles import RuntimeProfile

from . import ROOT

ASSETS = ROOT / "docs/assets/approved-resume-20260927"


class ApprovedResumeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = json.loads((ASSETS / "results.json").read_text())
        cls.matrix = json.loads((ASSETS / "guide-checks.json").read_text())

    def evidence(self, language, path):
        return self.result["languages"][language]["evidence"][path]["content"]

    def test_previous_evidence_and_current_boundaries_remain_explicit(self):
        previous = ROOT / "docs/assets/live-guide-audit-20260926/results.json"
        self.assertEqual(
            self.result["previous_evidence_sha256"],
            hashlib.sha256(previous.read_bytes()).hexdigest(),
        )
        self.assertTrue(self.result["main_answer_deployment_unchanged"])
        self.assertTrue(self.result["default_subscription_unchanged"])
        self.assertFalse(self.result["human_production_approval"])
        self.assertFalse(self.result["company_or_microsoft365_data_used"])
        self.assertFalse(self.result["new_recording"])
        rows = self.matrix["guides"]
        self.assertEqual(len(rows), 62)
        self.assertEqual(len({row["guide"] for row in rows}), 62)
        self.assertTrue(any(row["status"] == "prior-evidence-only" for row in rows))
        for row in rows:
            self.assertTrue((ROOT / row["guide"]).is_file())
            self.assertIn("previous_status", row)
            self.assertIn(row["checked_date"], ("2026-09-26", "2026-09-27"))

    def test_model_pins_and_role_scopes_do_not_hide_broader_grants(self):
        cases = (
            ("r27-pin-iq-model", "gpt-5.6-luna", "2026-07-09", 30),
            ("r27-pin-optimizer-model", "gpt-5.5", "2026-04-24", 50),
        )
        for step, model, version, capacity in cases:
            data = self.evidence("en", f"guide/outputs/live-audit/{step}/stdout.txt")
            self.assertEqual((data["model"]["name"], data["model"]["version"]), (model, version))
            self.assertEqual((data["state"], data["upgrade"]), ("Succeeded", "NoAutoUpgrade"))
            self.assertEqual(
                (data["sku"]["name"], data["sku"]["capacity"]), ("DataZoneStandard", capacity)
            )
            self.assertEqual(data["rai"], "Microsoft.DefaultV2")
        roles = self.result["roles"]
        self.assertEqual(len(roles), 8)
        self.assertEqual(len({role["id"] for role in roles}), 8)
        allowed_roles = {
            "7ca78c08-252a-4471-8644-bb5ff32d4ba0",
            "1407120a-92aa-4202-b7e9-c0e197c71c8f",
            "5e0bd9bd-7b93-4f28-af87-19fc36ad61bd",
            "53ca6127-db72-4b80-b1b0-d745d6d5456d",
        }
        for role in roles:
            self.assertIn(role["roleDefinitionId"].rsplit("/", 1)[-1], allowed_roles)
            self.assertIn("/resourceGroups/rg-mfv2-g6luna-swc-20260923/providers/", role["scope"])
            self.assertTrue(
                "/Microsoft.Search/searchServices/" in role["scope"]
                or "/Microsoft.CognitiveServices/accounts/" in role["scope"]
            )

    def test_real_tools_and_iq_preserve_distinct_identity_and_version_contracts(self):
        for language, version in (("en", "3"), ("ko", "2")):
            toolbox = self.evidence(
                language, "guide/outputs/toolbox-runs/r27-skilled-answer/summary.json"
            )
            self.assertEqual(toolbox["toolbox_version"], version)
            self.assertTrue(toolbox["tool_invoked"])
            self.assertTrue(toolbox["skill_load_verified"])
            self.assertEqual(toolbox["skill_ref"]["version"], "1")
            self.assertIn("load_skill", {item["name"] for item in toolbox["function_calls"]})
            api = self.evidence(
                language, "guide/outputs/openapi-runs/openapi-r27-explicit-query/summary.json"
            )
            self.assertTrue(api["openapi_calls"])
            for call in api["openapi_calls"]:
                self.assertEqual(call["status"], "completed")
                self.assertEqual(json.loads(call["arguments"])["api-version"], "2024-07-01")
            iq = self.evidence(language, "guide/outputs/iq-chat/iq-chat-r27/summary.json")
            self.assertEqual(iq["authentication"], "search-system-assigned-identity")
            self.assertEqual(iq["model_deployment"]["model"]["version"], "2026-07-09")
            self.assertTrue(iq["model_planning_verified"])
            self.assertTrue(iq["model_synthesis_verified"])

    def test_matrix_keeps_all_rows_and_distinguishes_execution_from_quality(self):
        all_ids = set()
        for language in ("en", "ko"):
            for label, expected in (("wf-baseline", 12), ("wf-candidate", 12), ("wf-final", 8)):
                base = f"matrix/outputs/benchmarks/{label}"
                manifest = self.evidence(language, base + "/manifest.json")
                rows = self.evidence(language, base + "/responses.jsonl")
                report = self.evidence(language, base + "/business-evaluation.json")
                self.assertEqual(manifest["actual_rows"], expected)
                self.assertEqual(manifest["expected_rows"], expected)
                self.assertEqual(manifest["status"], "completed")
                profile = RuntimeProfile.from_dict(manifest["runtime_contract"]["profile"])
                self.assertEqual(profile.language, language)
                self.assertEqual(profile.protocol, "invocations")
                self.assertEqual(report["errors"], 0)
                self.assertEqual(len(rows), expected)
                ids = {row["response_id"] for row in rows}
                self.assertEqual(len(ids), expected)
                self.assertTrue(all_ids.isdisjoint(ids))
                all_ids |= ids
            verdict = self.result["languages"][language]["matrix_verdict"]
            self.assertTrue(verdict["execution_gate_passed"])
            self.assertFalse(verdict["deployment_approved"])
            self.assertEqual(verdict["selected_model_keys"], ["a", "b"])
            self.assertEqual(verdict["calibration"]["correct"], 2)
            for trace in verdict["traces"].values():
                self.assertTrue(trace["trace_export_verified"])
                self.assertEqual(trace["verified_traces"], trace["expected_traces"])
        english = self.result["languages"]["en"]["matrix_verdict"]
        korean = self.result["languages"]["ko"]["matrix_verdict"]
        self.assertFalse(english["gate_passed"])
        self.assertEqual(english["recommendation"], "reject")
        self.assertTrue(korean["gate_passed"])
        self.assertEqual(korean["recommendation"], "review-native-findings")
        self.assertFalse(korean["native_quality_passed"])

    def test_optimizer_invalid_reference_is_not_promoted_or_repaired(self):
        data = self.result["optimizer"]
        review = data["evaluation/binding-review.json"]["content"]
        self.assertEqual((review["expected_rows"], review["actual_rows"]), (6, 6))
        self.assertFalse(review["grounding_binding_valid"])
        self.assertFalse(review["promotion_performed"])
        grounding = [
            item
            for row in review["rows"]
            for item in row["evaluators"]
            if item["name"] == "groundedness"
        ]
        self.assertEqual(len(grounding), 6)
        self.assertTrue(all(item["context_equals_response"] for item in grounding))
        self.assertTrue(all(not item["context_matches_source"] for item in grounding))
        run = data["result.json"]["content"]
        self.assertEqual(run["inputs"]["options"]["max_candidates"], 2)
        self.assertEqual(run["inputs"]["options"]["target_attributes"], ["instruction"])
        self.assertEqual(run["result"]["baseline"], run["result"]["best"])
        self.assertEqual(len(run["result"]["candidate_ids"]), 1)
        self.assertFalse(data["korean_run"]["performed"])

    def test_ci_and_owned_session_cleanup_are_separate_from_local_code(self):
        ci = self.result["ci"]
        for language, version in (("en", "1"), ("ko", "2")):
            state = ci[f"{language}-result.json"]["content"]
            self.assertEqual(state["head_sha"], self.result["runtime_source_commit"])
            self.assertEqual(state["conclusion"], "success")
            binding = ci[f"{language}/ci-binding.json"]["content"]
            self.assertEqual(binding["WORKSHOP_HOSTED_AGENT_VERSION"], version)
            self.assertEqual(binding["WORKSHOP_HOSTED_AGENT_NAME"], "mfv2-r27-ci-hosted")
            report = ci[f"{language}/benchmarks/ci-dev/business-evaluation.json"]["content"]
            self.assertTrue(report["business_gate_passed"])
            self.assertEqual(report["errors"], 0)
            self.assertEqual(self.result["cleanup"]["ci-" + language]["status"], "idle")
            for kind in ("toolbox", "matrix"):
                cleanup = self.result["cleanup"][f"{language}-{kind}"]
                self.assertTrue(cleanup["all_idle"])
                self.assertTrue(all(item["status"] == "idle" for item in cleanup["sessions"]))
        self.assertTrue(ci["restoration.json"]["content"]["verified"])

    def test_new_report_and_export_procedure_are_linked_in_both_languages(self):
        for directory in ("docs", "docs/ko"):
            report = (ROOT / directory / "reference/approved-resume-20260927.md").read_text()
            for fragment in (
                "reject",
                "review-native-findings",
                "grounding_binding_valid",
                "export_evaluation.py",
            ):
                self.assertIn(fragment, report)
            for name in ("coverage.md", "live-run.md", "reference/validation.md"):
                self.assertIn("approved-resume-20260927.md", (ROOT / directory / name).read_text())
            optimizer = (ROOT / directory / "labs/extensions/agent-optimizer.md").read_text()
            self.assertIn("--require-judge-inputs", optimizer)
            self.assertIn("--expected-rows 6", optimizer)

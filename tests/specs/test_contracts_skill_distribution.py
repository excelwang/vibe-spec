import unittest
from pathlib import Path

from tests.specs.conftest import verify_spec


class TestContractsSkillDistribution(unittest.TestCase):
    """Verifies CONTRACTS.SKILL_DISTRIBUTION requirements."""

    @verify_spec("CONTRACTS.SKILL_DISTRIBUTION")
    def test_skill_md_existence(self):
        """CONTRACTS.SKILL_DISTRIBUTION.SKILL_MD: System SHOULD maintain a SKILL.md file."""
        repo_root = Path(__file__).parent.parent.parent
        self.assertTrue((repo_root / "src" / "skills" / "vibespec" / "SKILL.md").exists())

    @verify_spec("CONTRACTS.SKILL_DISTRIBUTION")
    def test_vibespec_skill_entry_points(self):
        """CONTRACTS.SKILL_DISTRIBUTION.ENTRY_POINT: vibespec SKILL.md MUST define idea, reflect, distill."""
        skill_path = Path(__file__).parent.parent.parent / "src" / "skills" / "vibespec" / "SKILL.md"
        content = skill_path.read_text()

        self.assertIn("vibespec idea", content)
        self.assertIn("vibespec reflect", content)
        self.assertIn("vibespec distill", content)
        forbidden = ["gate" + "-loop", "fix " + "gate", "triage " + "gate"]
        for phrase in forbidden:
            self.assertNotIn(phrase, content)

    @verify_spec("CONTRACTS.SKILL_DISTRIBUTION")
    def test_workflow_references_exist(self):
        """CONTRACTS.SKILL_DISTRIBUTION.PROGRESSIVE_DISCLOSURE: SKILL.md SHOULD route to references."""
        skill_root = Path(__file__).parent.parent.parent / "src" / "skills" / "vibespec"
        skill_content = (skill_root / "SKILL.md").read_text()

        references = [
            "references/ingest_workflows.md",
            "references/review_workflows.md",
            "references/review_and_quality.md",
            "references/testing_protocol.md",
        ]

        for ref in references:
            self.assertTrue((skill_root / ref).exists(), f"{ref} MUST exist")
            self.assertIn(ref, skill_content, f"SKILL.md MUST reference {ref}")

    @verify_spec("CONTRACTS.SKILL_DISTRIBUTION")
    def test_external_repair_entrypoints_are_absent(self):
        """CONTRACTS.SKILL_DISTRIBUTION.PROGRESSIVE_DISCLOSURE: vibespec SHOULD stay focused on spec workflows."""
        skill_root = Path(__file__).parent.parent.parent / "src" / "skills" / "vibespec"
        skill_content = (skill_root / "SKILL.md").read_text()

        self.assertNotIn("plan_workflow", skill_content)
        self.assertFalse((skill_root / "references" / "plan_workflow.md").exists())
        removed_refs = [
            "gate" + "_workflows.md",
            "dual" + "_agent_coordination.md",
            "gate" + "_adapter.md",
        ]
        for ref in removed_refs:
            self.assertFalse((skill_root / "references" / ref).exists())


if __name__ == "__main__":
    unittest.main()

import unittest
import shutil
import tempfile
from pathlib import Path
from tests.specs.conftest import verify_spec
from src.skills.vibespec.scripts.validate import validate_references

class TestContractsValidation(unittest.TestCase):
    """Verifies CONTRACTS.VALIDATION logic"""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.specs_dir = self.test_dir / "specs"
        self.specs_dir.mkdir()
        self.tests_dir = self.test_dir / "tests/specs"
        self.tests_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @verify_spec("CONTRACTS.VALIDATION")
    def test_full_scan_valid(self):
        """CONTRACTS.VALIDATION.FULL_SCAN: System MUST support comprehensive project scan."""
        # Create valid spec
        (self.specs_dir / "L0-VISION.md").write_text("---\nversion: 1.0.0\n---\n# L0\n## VISION.SCOPE\n")
        
        errors, warnings, coverage = validate_references(self.specs_dir, self.tests_dir)
        self.assertEqual(len(errors), 0, f"Valid spec should have 0 errors, got: {errors}")

    @verify_spec("CONTRACTS.VALIDATION")
    def test_report_warnings(self):
        """CONTRACTS.VALIDATION.REPORT: System MUST summarize orphans/warnings."""
        # Create invalid spec (Orphan ID)
        (self.specs_dir / "L1-CONTRACTS.md").write_text("---\nversion: 1.0.0\n---\n# L1\n## CONTRACTS.TIMEOUT\n")
        
        errors, warnings, coverage = validate_references(self.specs_dir, self.tests_dir)
        # Should detect orphan traceability break (missing L0)
        orphan_warnings = [w for w in warnings if "Traceability break" in w]
        self.assertTrue(len(orphan_warnings) > 0, "Should report traceability warning for orphan L1 item")

    @verify_spec("CONTRACTS.VALIDATION")
    def test_group_verify_spec_anchor_is_not_orphan(self):
        """CONTRACTS.VALIDATION.REPORT: Group-level test anchors MUST be accepted without satisfying leaf coverage."""
        (self.specs_dir / "L0-VISION.md").write_text(
            "---\nversion: 1.0.0\n---\n# L0\n### VISION.FULL_SCAN\n- **FULL_SCAN**: group anchor fixture\n",
            encoding="utf-8",
        )
        (self.specs_dir / "L1-CONTRACTS.md").write_text(
            "---\nversion: 1.0.0\n---\n# L1\n## CONTRACTS.VALIDATION\n- **FULL_SCAN**: System MUST scan specs.\n",
            encoding="utf-8",
        )
        (self.tests_dir / "test_group_anchor.py").write_text(
            "from tests.specs.conftest import verify_spec\n\n"
            "@verify_spec(\"CONTRACTS.VALIDATION\")\n"
            "def test_group_anchor():\n"
            "    pass\n",
            encoding="utf-8",
        )

        errors, _warnings, coverage = validate_references(self.specs_dir, self.tests_dir)

        self.assertFalse([error for error in errors if "Orphan @verify_spec" in error])
        self.assertIn("CONTRACTS.VALIDATION.FULL_SCAN", coverage["missing_ids"])

"""Positive and negative controls for the O3 v3 coverage auditor's verdict gate.

Run from this folder: python -m unittest test_audit_v3_gate

Works on a temporary tree (records + journal + output), never on the real o3_v3 data.
The last chunk is used because it is small (341 leaves), so the controls run in well under a second.
"""

import gzip
import hashlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("audit_v3_coverage", HERE / "audit_v3_coverage.py")
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)

# WHY the last chunk: 3 955 841 leaves in chunks of 500 -> chunk 7911 holds exactly 341 leaves.
CHUNK_ID = 7911
N_IN_CHUNK = audit.N_LEAVES - CHUNK_ID * audit.CHUNK


def _build_tree(root, slack_mid, slack_r="2.41e-60", tamper_record=False, manifest_sha=None):
    """Write one consistent chunk (records + journal line). Returns nothing; files live in root."""
    rec_dir = root / "records"
    met_dir = root / "metrics"
    rec_dir.mkdir()
    met_dir.mkdir()
    base = CHUNK_ID * audit.CHUNK
    path = rec_dir / f"chunk_{CHUNK_ID:05d}.jsonl.gz"
    with gzip.open(path, "wt", encoding="utf-8") as gz:
        for i in range(N_IN_CHUNK):
            row = {
                "leaf": base + i,
                "ok": True,
                "slack": f"[{slack_mid} +/- {slack_r}]",
                "bup": "[0.00683 +/- 2.41e-60]",
            }
            gz.write(json.dumps(row) + "\n")
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    if tamper_record:
        sha = "0" * 64
    journal_line = {
        "chunk": CHUNK_ID,
        "n": N_IN_CHUNK,
        "ok": N_IN_CHUNK,
        "fails": 0,
        "record_sha256": sha,
    }
    (met_dir / "o3v3_progress.jsonl").write_text(json.dumps(journal_line) + "\n", encoding="utf-8")
    if manifest_sha is not None:
        # One input from the real code folder, hashed by the real file; only the expected value is faked.
        manifest = {
            "first_chunk": CHUNK_ID,
            "last_chunk": CHUNK_ID,
            "sha256": {"interval_cells_v3.py": manifest_sha},
        }
        (met_dir / "run_manifest_unit.json").write_text(json.dumps(manifest), encoding="utf-8")


def _audit(root):
    """Run the real main() on the temporary tree and return the written report."""
    saved = (audit.O3V3, audit.RECORDS, audit.PROGRESS)
    audit.O3V3 = str(root)
    audit.RECORDS = str(root / "records")
    audit.PROGRESS = str(root / "metrics" / "o3v3_progress.jsonl")
    old_argv = sys.argv
    try:
        sys.argv = ["audit_v3_coverage.py", str(CHUNK_ID), str(CHUNK_ID), "unit"]
        with redirect_stdout(io.StringIO()):
            audit.main()
    finally:
        sys.argv = old_argv
        audit.O3V3, audit.RECORDS, audit.PROGRESS = saved
    return json.loads((root / "metrics" / "audit_unit.json").read_text(encoding="utf-8"))


class VerdictGateControls(unittest.TestCase):
    def _run_case(self, **kwargs):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _build_tree(root, **kwargs)
            return _audit(root)

    def test_positive_control_positive_slack_is_complete(self):
        report = self._run_case(slack_mid="0.0068")
        self.assertIs(report["min_slack_certainly_positive"], True)
        self.assertEqual(report["verdict"], "COMPLETE_STRICT")

    def test_negative_control_negative_slack_is_not_complete(self):
        # All records ok=true, journal consistent, hash matches: only the sign of the certified bound
        # differs. Before the fix this was reported COMPLETE_STRICT.
        report = self._run_case(slack_mid="-0.0001")
        self.assertIs(report["min_slack_certainly_positive"], False)
        self.assertNotEqual(report["verdict"], "COMPLETE_STRICT")

    def test_negative_control_zero_crossing_slack_is_not_complete(self):
        # The enclosure straddles zero: not certainly positive, so not complete.
        report = self._run_case(slack_mid="0", slack_r="1e-30")
        self.assertIs(report["min_slack_certainly_positive"], False)
        self.assertNotEqual(report["verdict"], "COMPLETE_STRICT")

    def test_positive_control_matching_manifest_input_hash_is_checked(self):
        real = audit.sha256_file(str(HERE / "interval_cells_v3.py"))
        report = self._run_case(slack_mid="0.0068", manifest_sha=real)
        self.assertIn(
            "run_manifest_unit.json:interval_cells_v3.py", report["manifest_inputs_checked"]
        )
        self.assertEqual(report["manifest_inputs_mismatch"], [])
        self.assertEqual(report["verdict"], "COMPLETE_STRICT")

    def test_negative_control_wrong_manifest_input_hash_is_not_complete(self):
        report = self._run_case(slack_mid="0.0068", manifest_sha="0" * 64)
        self.assertEqual(
            report["manifest_inputs_mismatch"], ["run_manifest_unit.json:interval_cells_v3.py"]
        )
        self.assertNotEqual(report["verdict"], "COMPLETE_STRICT")

    def test_negative_control_tampered_record_hash_is_not_complete(self):
        report = self._run_case(slack_mid="0.0068", tamper_record=True)
        self.assertNotEqual(report["verdict"], "COMPLETE_STRICT")
        self.assertTrue(any("SHA-256 mismatch" in p for p in report["problems"]))


if __name__ == "__main__":
    unittest.main()

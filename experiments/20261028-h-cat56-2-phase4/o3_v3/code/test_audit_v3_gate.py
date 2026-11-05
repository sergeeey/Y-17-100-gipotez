"""Positive and negative controls for the O3 v3 coverage auditor's verdict gate.

Run from this folder: python -m unittest test_audit_v3_gate

Works on a temporary tree (records + journal + manifests + output), never on the real o3_v3 data.
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
REAL_CODE_HASH = audit.sha256_file(str(HERE / "interval_cells_v3.py"))


def _digest(sha256_dict):
    """Same formula the driver uses for inputs_digest."""
    return hashlib.sha256(json.dumps(sha256_dict, sort_keys=True).encode("utf-8")).hexdigest()


def _build_tree(
    root,
    slack_mid,
    slack_r="2.41e-60",
    tamper_record=False,
    negative_leaf=None,
    manifest_sha=REAL_CODE_HASH,
    write_manifest=True,
    manifest_range=(CHUNK_ID, CHUNK_ID),
    extra_inputs=None,
    journal_digest="match",
):
    """Write one chunk of records, its journal line and (optionally) a run manifest.

    journal_digest: "match" = journal carries the digest of the manifest, "bad" = a different digest,
    "absent" = no inputs_digest field (older runs). negative_leaf: index of one leaf with negative slack.
    """
    rec_dir = root / "records"
    met_dir = root / "metrics"
    rec_dir.mkdir()
    met_dir.mkdir()
    base = CHUNK_ID * audit.CHUNK
    path = rec_dir / f"chunk_{CHUNK_ID:05d}.jsonl.gz"
    with gzip.open(path, "wt", encoding="utf-8") as gz:
        for i in range(N_IN_CHUNK):
            mid = "-0.0001" if i == negative_leaf else slack_mid
            row = {
                "leaf": base + i,
                "ok": True,
                "slack": f"[{mid} +/- {slack_r}]",
                "bup": "[0.00683 +/- 2.41e-60]",
            }
            gz.write(json.dumps(row) + "\n")
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    if tamper_record:
        sha = "0" * 64

    sha256_dict = {"interval_cells_v3.py": manifest_sha}
    if extra_inputs:
        sha256_dict.update(extra_inputs)
    journal_line = {
        "chunk": CHUNK_ID,
        "n": N_IN_CHUNK,
        "ok": N_IN_CHUNK,
        "fails": 0,
        "record_sha256": sha,
    }
    if journal_digest == "match":
        journal_line["inputs_digest"] = _digest(sha256_dict)
    elif journal_digest == "bad":
        journal_line["inputs_digest"] = "f" * 64
    (met_dir / "o3v3_progress.jsonl").write_text(json.dumps(journal_line) + "\n", encoding="utf-8")

    if write_manifest:
        manifest = {
            "first_chunk": manifest_range[0],
            "last_chunk": manifest_range[1],
            "sha256": sha256_dict,
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

    # --- slack gate -------------------------------------------------------------------------------

    def test_positive_control_complete_with_matching_manifest_and_digest(self):
        report = self._run_case(slack_mid="0.0068")
        self.assertIs(report["min_slack_certainly_positive"], True)
        self.assertEqual(report["verdict"], "COMPLETE_STRICT")
        self.assertEqual(report["journal_inputs_digest_ok"], 1)
        self.assertEqual(report["problems"], [])

    def test_negative_control_negative_slack_is_not_complete(self):
        # Everything else consistent: only the sign of the certified bound differs.
        # Before the fix this was reported COMPLETE_STRICT.
        report = self._run_case(slack_mid="-0.0001")
        self.assertIs(report["min_slack_certainly_positive"], False)
        self.assertNotEqual(report["verdict"], "COMPLETE_STRICT")

    def test_negative_control_zero_crossing_slack_is_not_complete(self):
        report = self._run_case(slack_mid="0", slack_r="1e-30")
        self.assertIs(report["min_slack_certainly_positive"], False)
        self.assertNotEqual(report["verdict"], "COMPLETE_STRICT")

    def test_negative_control_one_negative_leaf_among_many_positive_is_not_complete(self):
        # Mixed chunk: 340 positive slacks and one negative. The minimum must catch it.
        report = self._run_case(slack_mid="0.0068", negative_leaf=170)
        self.assertIs(report["min_slack_certainly_positive"], False)
        self.assertNotEqual(report["verdict"], "COMPLETE_STRICT")

    # --- manifest coverage and input hashes ------------------------------------------------------

    def test_negative_control_no_manifest_is_not_complete(self):
        # Review of 6164265 (P1-2): a range with no manifest must not read as a pass.
        report = self._run_case(slack_mid="0.0068", write_manifest=False)
        self.assertGreater(report["manifest_uncovered_chunks"], 0)
        self.assertNotEqual(report["verdict"], "COMPLETE_STRICT")

    def test_negative_control_manifest_for_other_range_is_not_complete(self):
        report = self._run_case(slack_mid="0.0068", manifest_range=(0, 0))
        self.assertGreater(report["manifest_uncovered_chunks"], 0)
        self.assertNotEqual(report["verdict"], "COMPLETE_STRICT")

    def test_negative_control_wrong_manifest_input_hash_is_not_complete(self):
        report = self._run_case(slack_mid="0.0068", manifest_sha="0" * 64)
        self.assertEqual(
            report["manifest_inputs_mismatch"], ["run_manifest_unit.json:interval_cells_v3.py"]
        )
        self.assertNotEqual(report["verdict"], "COMPLETE_STRICT")

    def test_positive_control_manifest_input_hash_is_checked(self):
        report = self._run_case(slack_mid="0.0068")
        self.assertIn(
            "run_manifest_unit.json:interval_cells_v3.py", report["manifest_inputs_checked"]
        )
        self.assertEqual(report["manifest_inputs_mismatch"], [])

    def test_unlocated_external_input_is_reported_and_not_fully_verified(self):
        # Inputs outside the repo cannot be checked here: they are listed, the flag is False, and the
        # verdict stays COMPLETE_STRICT only with that flag read next to it (documented, not hidden).
        report = self._run_case(slack_mid="0.0068", extra_inputs={"R_input.npz": "0" * 64})
        self.assertEqual(
            report["manifest_inputs_unlocated"], ["run_manifest_unit.json:R_input.npz"]
        )
        self.assertIs(report["inputs_fully_verified"], False)

    # --- journal digests --------------------------------------------------------------------------

    def test_negative_control_journal_digest_from_other_inputs_is_not_complete(self):
        report = self._run_case(slack_mid="0.0068", journal_digest="bad")
        self.assertEqual(report["journal_inputs_digest_bad"], 1)
        self.assertNotEqual(report["verdict"], "COMPLETE_STRICT")

    def test_legacy_journal_without_digest_is_counted_not_failed(self):
        # Runs A-D predate the digest field: counted as absent, verdict unaffected by that alone.
        report = self._run_case(slack_mid="0.0068", journal_digest="absent")
        self.assertEqual(report["journal_inputs_digest_absent"], 1)
        self.assertEqual(report["verdict"], "COMPLETE_STRICT")

    # --- records ----------------------------------------------------------------------------------

    def test_negative_control_tampered_record_hash_is_not_complete(self):
        report = self._run_case(slack_mid="0.0068", tamper_record=True)
        self.assertNotEqual(report["verdict"], "COMPLETE_STRICT")
        self.assertTrue(any("SHA-256 mismatch" in p for p in report["problems"]))


if __name__ == "__main__":
    unittest.main()

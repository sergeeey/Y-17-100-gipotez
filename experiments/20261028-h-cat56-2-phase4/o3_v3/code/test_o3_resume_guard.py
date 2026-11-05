"""Controls for the O3 v3 resume guard (_done_chunks refuses journal lines from other inputs).

Run from this folder: python -m unittest test_o3_resume_guard

Uses a temporary journal; never reads or writes the real metrics/o3v3_progress.jsonl.
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
# WHY a separate file: o3_run_v3.py is the driver that produced runs A-D (its sha256 is in
# run_manifest_run*.json) and must stay byte-identical. The resume guard lives in the guarded copy.
_spec = importlib.util.spec_from_file_location(
    "o3_run_v3_resumeguard", HERE / "o3_run_v3_resumeguard.py"
)
run = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run)

DIGEST_A = "a" * 64
DIGEST_B = "b" * 64


def _journal(lines):
    tmp = tempfile.TemporaryDirectory()
    path = Path(tmp.name) / "o3v3_progress.jsonl"
    path.write_text("".join(json.dumps(x) + "\n" for x in lines), encoding="utf-8")
    return tmp, path


class ResumeGuardControls(unittest.TestCase):
    def _done(self, lines, digest=DIGEST_A):
        tmp, path = _journal(lines)
        self.addCleanup(tmp.cleanup)
        saved = run.PROGRESS
        run.PROGRESS = str(path)
        try:
            return run._done_chunks(digest)
        finally:
            run.PROGRESS = saved

    def test_positive_control_matching_digest_is_skipped(self):
        done = self._done(
            [{"chunk": 3, "inputs_digest": DIGEST_A}, {"chunk": 4, "inputs_digest": DIGEST_A}]
        )
        self.assertEqual(done, {3, 4})

    def test_no_journal_means_nothing_done(self):
        saved = run.PROGRESS
        run.PROGRESS = str(Path(tempfile.gettempdir()) / "definitely_absent_o3_journal.jsonl")
        try:
            self.assertEqual(run._done_chunks(DIGEST_A), set())
        finally:
            run.PROGRESS = saved

    def test_negative_control_other_inputs_refuse_to_resume(self):
        # Same chunk numbers, different input digest (e.g. R_input changed): must not be skipped.
        with self.assertRaises(RuntimeError) as ctx:
            self._done([{"chunk": 3, "inputs_digest": DIGEST_B}], digest=DIGEST_A)
        self.assertIn("refuse to resume", str(ctx.exception))

    def test_negative_control_line_without_digest_refuses_to_resume(self):
        # Journals written before this guard carry no digest: they cannot prove their inputs.
        with self.assertRaises(RuntimeError):
            self._done([{"chunk": 3, "n": 500, "ok": 500}])

    def test_negative_control_one_bad_line_among_good_refuses(self):
        with self.assertRaises(RuntimeError):
            self._done(
                [
                    {"chunk": 3, "inputs_digest": DIGEST_A},
                    {"chunk": 4, "inputs_digest": DIGEST_B},
                ]
            )


if __name__ == "__main__":
    unittest.main()

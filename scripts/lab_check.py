"""lab_check.py — validate registry/graph.yaml against registry/SCHEMA.md.

Checks:
  * required fields per node type
  * unique ids, no dangling edge references
  * status / edge-type vocabulary matches SCHEMA
  * evidence_mode / verification_strength vocab (ADR-122, optional fields, checked
    only when present -- see EVIDENCE_MODE/VERIFICATION_STRENGTH module constants)
  * SCHEMA invariants 1-3:
      1. every hypothesis has >=1 incoming `grounds` edge and a non-empty kill_criterion
      2. every `invalidated` artifact has >=1 incoming `invalidates` edge
      3. no `ready` hypothesis has an ancestor (via depends_on/grounds) whose
         status is invalidated / killed / stale   <- the 2026-05-28 stale-PARKED incident

Also prints (informational, never affects exit code): a substrate-diversity report
(ADR-122) -- how many hypothesis/artifact nodes are `tested_on` how many distinct
`substrate` nodes, countering the "N graph nodes = N independent discoveries" illusion.

Usage:  python scripts/lab_check.py            (exit 0 = clean, 1 = violations)
Origin: written inline as the pre-commit check for the very first core commit
        (2026-09-06); promoted to a script because the need recurred immediately
        (pearl_registry entry #2). Not a framework — keep it under ~120 lines.
"""

from __future__ import annotations

# WHY: plain print() instead of structlog — this is a CLI validator whose stdout IS the
# interface (human + exit code). Adding a logging dependency for zero consumers would be
# overengineering (ADR-002). Revisit only if lab_check output is ever consumed by a hook.
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "registry" / "graph.yaml"

REQUIRED = {"id", "type", "title", "status", "evidence", "source", "updated"}
EXTRA = {
    "problem": {"catalog", "catalog_ref"},
    "project": {"path", "owner"},
    "bridge": {"mechanism"},
    "hypothesis": {"l0_type", "kill_criterion", "experiment_dir", "fl_tier"},
    "artifact": {"date_created", "provenance"},
    "question": {"blocks"},
    "substrate": {"category"},
}
STATUS = {
    "problem": {"open", "partially_solved", "solved", "disputed"},
    "project": {"active", "hold", "archived", "unverified_source"},
    "bridge": {"proposed", "verified_grounding", "unverified_source", "rejected"},
    "hypothesis": {
        "proposed",
        "ready",
        "ready_to_scope",
        "needs_formalization",
        "blocked",
        "running",
        "killed",
        "confirmed",
        "lead",
        "parked",
    },
    "artifact": {"valid", "invalidated", "stale", "superseded"},
    "question": {"open", "resolved"},
    "substrate": {"active", "exhausted", "blocked", "archived"},
}
EVIDENCE = {
    "VERIFIED-REAL",
    "VERIFIED-SYNTHETIC",
    "HYPOTHESIS",
    "UNVERIFIED",
    "CONFLICT",
}
EDGE_TYPES = {
    "grounds",
    "depends_on",
    "invalidates",
    "supersedes",
    "blocks",
    "links_to",
    "collides_with",
    "tested_on",
}
DEAD = {"invalidated", "killed", "stale"}
SUBSTRATE_CATEGORY = {"model", "dataset", "theorem_family", "open_problem"}

# ADR-122: orthogonal to `status` -- optional on hypothesis/artifact nodes, checked only
# when present (retrofitting all pre-existing nodes is out of scope, see ADR-122 itself).
EVIDENCE_MODE = {"empirical", "exhaustive", "deductive", "formal", "simulation"}
VERIFICATION_STRENGTH = {"none", "weak", "medium", "strong"}


def main(graph_path: Path = GRAPH) -> int:
    g = yaml.safe_load(graph_path.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in g["nodes"]}
    edges = g["edges"]
    errors: list[str] = []

    if len(nodes) != len(g["nodes"]):
        errors.append("duplicate node ids")

    for n in g["nodes"]:
        t = n.get("type")
        if t not in EXTRA:
            errors.append(f"{n.get('id')}: unknown type {t!r}")
            continue
        missing = (REQUIRED | EXTRA[t]) - set(n)
        if missing:
            errors.append(f"{n['id']}: missing fields {sorted(missing)}")
        if n.get("status") not in STATUS[t]:
            errors.append(f"{n['id']}: status {n.get('status')!r} not allowed for {t}")
        if n.get("evidence") not in EVIDENCE:
            errors.append(f"{n['id']}: evidence {n.get('evidence')!r} not in vocabulary")
        if t == "substrate" and n.get("category") not in SUBSTRATE_CATEGORY:
            errors.append(f"{n['id']}: category {n.get('category')!r} not in vocabulary")
        # ADR-122: optional fields, checked only when present -- see EVIDENCE_MODE/
        # VERIFICATION_STRENGTH comment above for why this is not retrofitted everywhere.
        if "evidence_mode" in n and n["evidence_mode"] not in EVIDENCE_MODE:
            errors.append(f"{n['id']}: evidence_mode {n['evidence_mode']!r} not in vocabulary")
        if "verification_strength" in n and n["verification_strength"] not in VERIFICATION_STRENGTH:
            errors.append(
                f"{n['id']}: verification_strength {n['verification_strength']!r} not in vocabulary"
            )

    for e in edges:
        if e["type"] not in EDGE_TYPES:
            errors.append(f"edge {e['from']}->{e['to']}: unknown type {e['type']!r}")
        for end in ("from", "to"):
            if e[end] not in nodes:
                errors.append(f"edge {e['from']}->{e['to']}: dangling {end}={e[end]!r}")

    # invariant 1
    for h in (n for n in g["nodes"] if n["type"] == "hypothesis"):
        inc = [e for e in edges if e["to"] == h["id"] and e["type"] == "grounds"]
        if not inc:
            errors.append(f"INV1 {h['id']}: no incoming `grounds` edge")
        if not str(h.get("kill_criterion", "")).strip():
            errors.append(f"INV1 {h['id']}: empty kill_criterion")

    # invariant 2
    for a in (n for n in g["nodes"] if n["type"] == "artifact" and n["status"] == "invalidated"):
        if not any(e["to"] == a["id"] and e["type"] == "invalidates" for e in edges):
            errors.append(f"INV2 {a['id']}: invalidated without an `invalidates` edge")

    # invariant 3
    def ancestors(nid: str, seen: set[str] | None = None) -> set[str]:
        seen = seen if seen is not None else set()
        for e in edges:
            if e["to"] == nid and e["type"] in ("depends_on", "grounds") and e["from"] not in seen:
                seen.add(e["from"])
                ancestors(e["from"], seen)
        return seen

    for h in (n for n in g["nodes"] if n["type"] == "hypothesis" and n["status"] == "ready"):
        bad = [a for a in ancestors(h["id"]) if nodes[a]["status"] in DEAD]
        if bad:
            errors.append(f"INV3 {h['id']} is `ready` but depends on dead ancestor(s) {bad}")

    print(f"graph: {len(nodes)} nodes, {len(edges)} edges")
    if errors:
        print(f"FAIL — {len(errors)} violation(s):")
        for err in errors:
            print("  -", err)
        return 1
    print("OK — schema, vocabulary, invariants 1-3 all pass")

    # ADR-122: substrate-diversity report -- informational only, never fails the build.
    # Purpose: make graph inflation visible (N hypothesis nodes vs. M *independent* substrates
    # they actually run on) instead of letting node count alone imply breadth.
    substrates = [n for n in g["nodes"] if n["type"] == "substrate"]
    if substrates:
        tested_on = [e for e in edges if e["type"] == "tested_on"]
        per_substrate: dict[str, int] = {s["id"]: 0 for s in substrates}
        untagged = 0
        hyp_and_art_ids = {n["id"] for n in g["nodes"] if n["type"] in ("hypothesis", "artifact")}
        tagged_sources: set[str] = set()
        for e in tested_on:
            if e["to"] in per_substrate:
                per_substrate[e["to"]] += 1
                tagged_sources.add(e["from"])
        untagged = len(hyp_and_art_ids - tagged_sources)
        print(
            f"substrate diversity: {len(substrates)} substrate(s), "
            f"{len(tagged_sources)}/{len(hyp_and_art_ids)} hypothesis/artifact node(s) tagged "
            f"({untagged} not yet tagged — retrofit is incremental, see ADR-122)"
        )
        for sid, count in sorted(per_substrate.items(), key=lambda kv: -kv[1]):
            print(f"  - {sid}: {count} node(s) tested_on")

    return 0


if __name__ == "__main__":
    sys.exit(main())

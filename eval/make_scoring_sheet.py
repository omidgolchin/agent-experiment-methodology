"""Create a blinded scoring sheet from the raw outputs.

    python make_scoring_sheet.py

Writes:
  scoring/reviews/<blind_id>.md   one review per file, with the design ID but not the condition
  scoring/sheet.csv               one row per review, to fill in by hand
  scoring/_key_DO_NOT_OPEN.csv    blind_id -> run_id and condition (open only after scoring)

Score each review against answer_key.yaml:
  detected      1 if the review names the planted flaw with the right reason, else 0
  as_blocking   1 if that finding is labelled BLOCKING, else 0 (leave blank if detected = 0)
  overflag      clean designs only (C*): 1 if any finding is BLOCKING or the verdict is "not ready"
                and you judge it not to be a genuine claim-threatening problem, else 0
  notes         free text, especially for every overflag decision
"""
from __future__ import annotations

import csv
import random

from common import SCORING_DIR, load_config, read_raw


def main() -> None:
    cfg = load_config()
    runs = read_raw()
    if not runs:
        raise SystemExit("No outputs yet. Run run_eval.py first.")
    rng = random.Random(cfg["master_seed"] + 1)
    rng.shuffle(runs)
    (SCORING_DIR / "reviews").mkdir(parents=True, exist_ok=True)

    used = set()
    sheet, key = [], []
    for r in runs:
        while True:
            blind = f"R{rng.randrange(10000, 99999)}"
            if blind not in used:
                used.add(blind)
                break
        text = r.get("text", "") if r.get("status") == "ok" else "[RUN FAILED: no output]"
        (SCORING_DIR / "reviews" / f"{blind}.md").write_text(
            f"# Review {blind} (design {r['design_id']})\n\n{text}\n", encoding="utf-8")
        sheet.append({"blind_id": blind, "design_id": r["design_id"],
                      "detected": "", "as_blocking": "", "overflag": "", "notes": ""})
        key.append({"blind_id": blind, "run_id": r["run_id"], "condition": r["condition"],
                    "status": r.get("status", "")})

    sheet.sort(key=lambda x: (x["design_id"], x["blind_id"]))
    with open(SCORING_DIR / "sheet.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sheet[0]))
        w.writeheader()
        w.writerows(sheet)
    with open(SCORING_DIR / "_key_DO_NOT_OPEN.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(key[0]))
        w.writeheader()
        w.writerows(key)
    print(f"Wrote {len(sheet)} blinded reviews to {SCORING_DIR}/")


if __name__ == "__main__":
    main()

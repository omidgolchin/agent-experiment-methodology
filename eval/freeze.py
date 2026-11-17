"""Write or verify a SHA-256 manifest of everything that defines the evaluation.

    python freeze.py           # write FREEZE_MANIFEST.txt
    python freeze.py --verify  # check that nothing changed since the freeze

Freeze after you settle config.yaml and before the first real run, and commit the manifest.
Any later change is an amendment: record it in PLAN.md with its date, reason and whether outputs
had been seen, then re-run this script and commit again. Git history keeps both manifests.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys

from common import EVAL_DIR, load_config, sha256_file

MANIFEST = EVAL_DIR / "FREEZE_MANIFEST.txt"


def frozen_files() -> list:
    cfg = load_config()
    files = sorted((EVAL_DIR / "designs").glob("*.md"))
    files += sorted((EVAL_DIR / "prompts").glob("*.md"))
    files += [EVAL_DIR / "answer_key.yaml", EVAL_DIR / "config.yaml", EVAL_DIR / "PLAN.md"]
    files += [(EVAL_DIR / rel).resolve() for rel in cfg["skill_files"]]
    files += sorted(EVAL_DIR.glob("*.py"))
    return files


def rel(path) -> str:
    try:
        return str(path.relative_to(EVAL_DIR.parent))
    except ValueError:
        return str(path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()
    current = {rel(p): sha256_file(p) for p in frozen_files()}

    if args.verify:
        if not MANIFEST.exists():
            sys.exit("No FREEZE_MANIFEST.txt yet. Run `python freeze.py` first.")
        recorded = {}
        for line in MANIFEST.read_text(encoding="utf-8").splitlines():
            if line and not line.startswith("#"):
                digest, name = line.split("  ", 1)
                recorded[name] = digest
        changed = [n for n in current if recorded.get(n) != current[n]]
        missing = [n for n in recorded if n not in current]
        if changed or missing:
            print("Changed since freeze:", *changed, sep="\n  ")
            if missing:
                print("Missing:", *missing, sep="\n  ")
            sys.exit(1)
        print(f"OK: {len(current)} files match the manifest.")
        return

    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    lines = [f"# Freeze manifest, written {stamp}", "# sha256  path"]
    lines += [f"{d}  {n}" for n, d in sorted(current.items())]
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {MANIFEST.name} with {len(current)} files.")


if __name__ == "__main__":
    main()

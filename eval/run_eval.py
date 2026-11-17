"""Run every design under both conditions and save raw outputs.

    python run_eval.py --dry-run   # no API calls; writes placeholder outputs to test the pipeline
    python run_eval.py             # real run (needs the API key named in config.yaml)

The script resumes: runs already present in outputs/raw_runs.jsonl are skipped.
A run that still fails after 3 identical attempts is saved with status "error"; the plan scores
it as "not detected" (see PLAN.md).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import time

from common import (OUT_DIR, RAW_PATH, build_messages, design_ids, load_config, read_raw,
                    sha256_text)

MAX_ATTEMPTS = 3


def run_plan(cfg: dict) -> list[dict]:
    rng = random.Random(cfg["master_seed"])
    runs = []
    for d in design_ids():
        for cond in cfg["conditions"]:
            for rep in range(cfg["reps"]):
                runs.append({"run_id": f"{d}-{cond}-r{rep + 1}", "design_id": d,
                             "condition": cond, "rep": rep + 1,
                             "seed": rng.randrange(1, 2**31 - 1)})
    rng.shuffle(runs)  # interleave conditions and designs over time
    for i, r in enumerate(runs):
        r["order"] = i + 1
    return runs


def call_model(client, cfg: dict, messages: list[dict], seed: int):
    return client.chat.completions.create(
        model=cfg["model"], messages=messages, temperature=cfg["temperature"],
        max_tokens=cfg["max_tokens"], seed=seed)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None, help="stop after N new runs")
    args = ap.parse_args()

    cfg = load_config()
    OUT_DIR.mkdir(exist_ok=True)
    done = {r["run_id"] for r in read_raw()}
    todo = [r for r in run_plan(cfg) if r["run_id"] not in done]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(done)} runs already saved; {len(todo)} to do.")

    client = None
    if not args.dry_run:
        from openai import OpenAI
        client = OpenAI(base_url=cfg["base_url"], api_key=os.environ[cfg["api_key_env"]])

    for r in todo:
        messages = build_messages(cfg, r["design_id"], r["condition"])
        rec = dict(r, model_requested=cfg["model"], temperature=cfg["temperature"],
                   max_tokens=cfg["max_tokens"],
                   prompt_sha256=sha256_text(json.dumps(messages, ensure_ascii=False)),
                   system_chars=len(messages[0]["content"]), dry_run=args.dry_run,
                   started_utc=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))
        if args.dry_run:
            rec.update(status="ok", attempts=1, model_returned="dry-run", finish_reason="stop",
                       text=f"[dry run placeholder for {r['run_id']}]\nVERDICT: not ready",
                       usage={}, latency_s=0.0)
        else:
            for attempt in range(1, MAX_ATTEMPTS + 1):
                t0 = time.time()
                try:
                    resp = call_model(client, cfg, messages, r["seed"])
                    choice = resp.choices[0]
                    rec.update(status="ok", attempts=attempt, model_returned=resp.model,
                               finish_reason=choice.finish_reason,
                               text=choice.message.content or "",
                               usage=resp.usage.model_dump() if resp.usage else {},
                               latency_s=round(time.time() - t0, 2))
                    break
                except Exception as e:  # noqa: BLE001 - record any API failure
                    rec.update(status="error", attempts=attempt, error=repr(e)[:500], text="")
                    time.sleep(5 * attempt)
        with open(RAW_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"[{r['order']:>3}] {r['run_id']}: {rec['status']}")


if __name__ == "__main__":
    main()

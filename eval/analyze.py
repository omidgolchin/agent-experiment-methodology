"""Analyse the scored sheet as pre-specified in PLAN.md.

    python analyze.py

Reads scoring/sheet.csv (filled in), scoring/_key_DO_NOT_OPEN.csv and outputs/raw_runs.jsonl.
Writes results/summary.md and results/detection_by_design.png.
"""
from __future__ import annotations

import re

import matplotlib
import numpy as np
import pandas as pd
from scipy.stats import binomtest

from common import RESULTS_DIR, SCORING_DIR, load_config, read_raw

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

N_BOOT = 10_000


def verdict(text: str) -> str:
    # \W* allows markdown around the label, e.g. "**VERDICT:** not ready" (amendment, PLAN.md).
    m = re.findall(r"VERDICT\W*(ready with conditions|not ready|ready)\b", text or "", flags=re.I)
    return m[-1].lower() if m else "missing"


def main() -> None:
    cfg = load_config()
    sheet = pd.read_csv(SCORING_DIR / "sheet.csv")
    key = pd.read_csv(SCORING_DIR / "_key_DO_NOT_OPEN.csv")
    raw = pd.DataFrame(read_raw())[["run_id", "text", "status"]]
    df = sheet.merge(key, on="blind_id").merge(raw, on=["run_id", "status"], how="left")
    df["words"] = df["text"].fillna("").str.split().str.len()
    df["verdict"] = df["text"].apply(verdict)

    flawed = df[df.design_id.str.startswith("D")].copy()
    clean = df[df.design_id.str.startswith("C")].copy()
    if flawed["detected"].isna().any():
        raise SystemExit("Some flawed-design rows have no 'detected' score yet.")
    # Pre-specified: failed runs count as not detected.
    flawed.loc[flawed.status != "ok", "detected"] = 0

    # Primary estimand: mean over designs of (P(detect | skill) - P(detect | baseline)).
    per = flawed.pivot_table(index="design_id", columns="condition", values="detected", aggfunc="mean")
    per["diff"] = per["skill"] - per["baseline"]
    est = per["diff"].mean()

    rng = np.random.default_rng(cfg["master_seed"])
    diffs = per["diff"].to_numpy()
    boot = [rng.choice(diffs, size=len(diffs), replace=True).mean() for _ in range(N_BOOT)]
    lo, hi = np.percentile(boot, [2.5, 97.5])

    wins, losses = int((per["diff"] > 0).sum()), int((per["diff"] < 0).sum())
    sign_p = binomtest(wins, wins + losses, 0.5).pvalue if wins + losses else float("nan")

    det = flawed[flawed.detected == 1]
    as_block = det.groupby("condition")["as_blocking"].mean()
    words = df.groupby("condition")["words"].median()
    fails = df.groupby("condition")["status"].apply(lambda s: (s != "ok").mean())
    over = clean.groupby("condition")["overflag"].mean() if clean["overflag"].notna().any() else None
    group = (df.design_id.str[0].map({"D": "flawed", "C": "clean"}) + " / " + df.condition).rename("designs / condition")
    verdicts = pd.crosstab(group, df.verdict.rename("verdict"))

    RESULTS_DIR.mkdir(exist_ok=True)
    lines = [
        "# Results",
        "",
        f"Model: `{cfg['model']}`, temperature {cfg['temperature']}, {cfg['reps']} runs per design and condition.",
        "",
        "## Primary: detection of the planted flaw (10 flawed designs)",
        "",
        f"- Detection rate, baseline: {per['baseline'].mean():.2f}",
        f"- Detection rate, with skill: {per['skill'].mean():.2f}",
        f"- Difference (skill minus baseline), averaged over designs: {est:+.2f} "
        f"(95% bootstrap interval over designs: {lo:+.2f} to {hi:+.2f})",
        f"- Designs where the skill did better / worse / the same: {wins} / {losses} / {len(per) - wins - losses} "
        f"(exact sign test p = {sign_p:.3f})",
        "",
        "## Secondary",
        "",
        "Share of detected flaws labelled BLOCKING:",
        "",
        as_block.round(2).to_markdown() if len(as_block) else "(none detected)",
        "",
        "Over-flagging on the 2 clean designs (share of reviews):",
        "",
        over.round(2).to_markdown() if over is not None else "(not scored)",
        "",
        "Verdicts:",
        "",
        verdicts.to_markdown(),
        "",
        "Median review length (words) and failed-run share by condition:",
        "",
        pd.DataFrame({"median_words": words, "failed_share": fails.round(3)}).to_markdown(),
        "",
        "## Per design",
        "",
        per.round(2).to_markdown(),
        "",
        "Interpretation rules are in PLAN.md. The 10 designs were written for this test, so the result "
        "describes these flaws, not experimental designs in general.",
    ]
    (RESULTS_DIR / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(7, 4))
    y = np.arange(len(per))
    ax.scatter(per["baseline"], y, label="baseline", marker="o")
    ax.scatter(per["skill"], y, label="with skill", marker="s")
    for i, (b, s) in enumerate(zip(per["baseline"], per["skill"])):
        ax.plot([b, s], [i, i], color="grey", lw=0.8, zorder=0)
    ax.set_yticks(y, per.index)
    ax.set_xlim(-0.05, 1.05)
    ax.set_xlabel(f"Share of {cfg['reps']} runs that detected the planted flaw")
    ax.legend(loc="lower right", frameon=False)
    ax.set_title("Planted-flaw detection by design")
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "detection_by_design.png", dpi=200)
    print((RESULTS_DIR / "summary.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()

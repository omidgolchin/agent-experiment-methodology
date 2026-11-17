"""Shared helpers for the seeded-flaw evaluation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

EVAL_DIR = Path(__file__).resolve().parent
OUT_DIR = EVAL_DIR / "outputs"
RAW_PATH = OUT_DIR / "raw_runs.jsonl"
SCORING_DIR = EVAL_DIR / "scoring"
RESULTS_DIR = EVAL_DIR / "results"


def load_config() -> dict:
    with open(EVAL_DIR / "config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def design_ids() -> list[str]:
    return sorted(p.stem for p in (EVAL_DIR / "designs").glob("*.md"))


def read_design(design_id: str) -> str:
    return (EVAL_DIR / "designs" / f"{design_id}.md").read_text(encoding="utf-8")


def skill_text(cfg: dict) -> str:
    parts = []
    for rel in cfg["skill_files"]:
        path = (EVAL_DIR / rel).resolve()
        parts.append(f"===== FILE: {path.name} =====\n" + path.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def build_messages(cfg: dict, design_id: str, condition: str) -> list[dict]:
    """Both conditions get the same user message; only the system prompt differs."""
    user = (EVAL_DIR / "prompts" / "user_prompt.md").read_text(encoding="utf-8")
    user = user.replace("{design}", read_design(design_id))
    if condition == "baseline":
        system = (EVAL_DIR / "prompts" / "system_baseline.md").read_text(encoding="utf-8")
    elif condition == "skill":
        system = (EVAL_DIR / "prompts" / "system_skill.md").read_text(encoding="utf-8")
        system = system.replace("{skill}", skill_text(cfg))
    else:
        raise ValueError(f"unknown condition: {condition}")
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_raw() -> list[dict]:
    if not RAW_PATH.exists():
        return []
    with open(RAW_PATH, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

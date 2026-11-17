# Evaluation plan: does the skill help a model catch flaws in agent-experiment designs?

Settle every open item below, then run `python freeze.py` before the first real run. Changes after the freeze go in the amendment log at the end.

## Question

When a language model reviews a short design for an experiment on LLM agents that contains one serious flaw, does giving it this skill make it more likely to find that flaw?

## Conditions

Both conditions get the same user message, which asks for a review with BLOCKING / NON-BLOCKING labels and a final verdict line (`prompts/user_prompt.md`). Only the system prompt differs:

- **baseline:** a one-sentence methodologist role (`prompts/system_baseline.md`).
- **skill:** the same sentence, followed by the full skill text with its reference files (`prompts/system_skill.md`).

**What the contrast estimates.** The effect of adding the entire skill text to the system prompt. That bundles the skill's content with a much longer prompt and its vocabulary. The test does not isolate any single part of the skill.

## Stimuli

There are 12 short designs in `designs/`, written for this test before any run. All are experiments on or with LLM agents: single tool-using agents, multi-agent teams, simulated customers and game-playing agents.

- D01–D10 each contain one planted flaw, from a different category: a bundled contrast; post-treatment selection; pseudo-replication; an outcome-structural difference; differential exclusion; an unmasked, unvalidated model judge; pilot tuning to the effect; a time and version confound; a demand cue; multiplicity.
- C01–C02 are clean controls with no planted major flaw.

The flaws and the detection criteria are fixed in `answer_key.yaml`.

## Units and replication

The design is the replication unit. Each design is reviewed `reps` times per condition (default 3). Repeated runs sample the model's responses for that design and are not independent designs. Run order is randomized and interleaved across conditions (`master_seed`).

## Outcomes

- **Primary:** for each review of D01–D10, whether it names the planted flaw with the right reason (`detected`, 0/1), scored against `answer_key.yaml`.
- **Secondary:**
  - whether a detected flaw is labelled BLOCKING;
  - over-flagging on C01–C02 (a BLOCKING finding or a "not ready" verdict that the scorer judges not genuine);
  - the verdict distribution;
  - review length;
  - failed runs.

## Scoring

Scoring is done by hand from `scoring/sheet.csv`, which shows the design ID but not the condition. Blinding is imperfect, because reviews written with the skill may be recognizable by their style; report this. If possible, a second person scores a random 25% of reviews, and agreement on `detected` is reported (percentage agreement and Cohen's kappa).

## Exclusions and failures

No review is excluded. A run that fails after 3 identical attempts is scored as not detected.

## Analysis

`analyze.py` computes the following:

1. Per design, the share of runs that detected the flaw, in each condition.
2. The primary estimate: the mean over the 10 designs of (skill minus baseline), with a 95% bootstrap interval that resamples designs.
3. An exact sign test across designs.

## Interpretation rules (set before running)

- **The skill helped on these designs** if the primary estimate is positive and the bootstrap interval excludes zero.
- **The skill hurt** if the estimate is negative and the interval excludes zero.
- **Inconclusive** otherwise. With 10 designs, small effects cannot be distinguished from zero, and an inconclusive result is not evidence of no effect.
- Report over-flagging alongside detection either way: a skill that catches more flaws by flagging everything is not better.

## Limitations to report

- The designs were written by the skill's author, and the flaw categories overlap with what the skill teaches.
- There is one model, and the contrast is bundled (see Conditions).
- Blinding is imperfect, and there is a single scorer unless a second one is added.
- The results describe these 10 flaws, not agent-experiment designs in general.

## Amendment log

| Date | Change | Reason | Outputs seen? |
|---|---|---|---|
| 2026-11-10 | `run_eval.py`, `common.py`: dry-run placeholders now go to `outputs/dry_run.jsonl`, and the real run refuses to start if placeholders are in `raw_runs.jsonl`; re-frozen. | The first freeze's dry run wrote placeholders where the real run resumes from, so the real run skipped every call. | No — no real outputs existed. |
| 2026-11-10 | `analyze.py`: the verdict parser now accepts markdown around the label ("**VERDICT:** not ready"); re-frozen. | The first analysis classed 37 of 72 verdicts as "missing" although every review had a verdict line; the strict pattern missed bolded labels. Affects only the secondary verdict table; detection, labelling and over-flagging are unchanged. | Yes — the first analysis output had been seen. |

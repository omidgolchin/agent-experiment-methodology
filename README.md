# Agent Experiment Methodology

This is an agent skill for reviewing the design of an experiment on LLM agents before you build or run anything. It finds the choices your design leaves open, checks what each comparison actually tests, and keeps your decisions separate from the model's suggestions.

I built it while running my own experiments with LLM agents. In these studies a condition is not just "the treatment". It is a whole configuration: the model, the prompts, the tools, the memory, the other agents, the environment, the budgets and the harness. One extra sentence or one different step limit in one condition changes what the comparison measures, and that is easy to miss.

The skill is for anyone running controlled comparisons with agents, for example:

- **agents as subjects:** how agents behave in games, negotiations, debates or simulated societies under different personas, partners or rules;
- **agents as systems under test:** whether a prompt, a tool, a memory module, a planner, a team structure or a different model makes an agent better at a task.

The general checks also work for experiments that have no agents in them.

## What it checks

- **What a comparison really tests.** It builds a table of everything that differs between conditions, not only the intended manipulation: prompts, personas, tools, memory, turn order, how answers are combined, compute, the harness, the environment and who is measured. For example, "debate vs. a single agent" usually also compares more tokens and more samples.
- **Whether the outcome would differ anyway.** If the effect you expect did not exist at all, would the outcome still differ between conditions? For example, six agents produce more ideas than two even if no agent behaves any differently.
- **Timing.** Nothing that defines a comparison should depend on what agents did after treatment: no subgroups, exclusions or task classes built from behavior ("hard tasks are the ones the agents failed").
- **Replication.** Repeating runs with new seeds samples the model's randomness. It does not give you new tasks, new scenarios, new wordings or new models.
- **Hazards specific to agents.** Prompt sensitivity, order effects, nondeterminism, model and environment changes over time, state leaking between runs, contamination, limits and retries that hit one condition more than the other, checkers agents can game, LLM judges, agents' self-reports, simulated users and cues in the prompt. Each one comes with a check and a fix.
- **Measurement.** Whether a measure captures what you mean, whether judges are blind to condition, and whether model-coded outcomes are validated.
- **The analysis plan.** The exact quantity being estimated, clustering by task, multiple outcomes, power or precision, and how results will be read, all decided before the data come in.
- **Pilots and freezes.** What a pilot is allowed to change, and how changes after the freeze are recorded.

It works by a simple rule: the model proposes and the researcher decides. Advice, notes and AI output are treated as input, not decisions, and a source is cited only after it has been checked.

## Using it

The skill is a folder in the Agent Skills format: `skill/agent-experiment-methodology/`, with a `SKILL.md` file and six reference files.

- **Claude:** add the folder as a skill, then ask, for example, "audit this agent experiment", "what does my debate vs. single-agent comparison actually measure?" or "write the condition specification for these two configurations".
- **Other models:** paste `SKILL.md`, and any reference files you need, into the system prompt. `eval/prompts/system_skill.md` shows one way to do it.

## Does it help? A small test

I tested the skill with a small, pre-specified study in `eval/`:

1. **Designs.** I wrote ten short designs for agent experiments, each with one planted flaw from a different category, plus two clean designs with no planted flaw.
2. **Reviews.** A model reviewed each design three times with the skill and three times without it.
3. **Scoring.** Each review was scored by hand against a fixed answer key, without knowing which condition it came from.

`eval/PLAN.md` describes the protocol, the rules for reading the results, and the limitations.

```bash
cd eval
pip install -r ../requirements.txt
python freeze.py                 # hash the designs, answer key, prompts, skill and settings
python run_eval.py --dry-run     # test the pipeline without API calls
python run_eval.py               # real run; set the API key named in config.yaml
python make_scoring_sheet.py     # blinded reviews in scoring/
# score scoring/sheet.csv against answer_key.yaml, then:
python analyze.py                # results/summary.md and results/detection_by_design.png
```

**Results (v0.1, gpt-oss-120b, 3 reviews per design and condition).** Both conditions caught almost every planted flaw: 29 of 30 reviews without the skill and 30 of 30 with it. With the skill, every flaw that was caught was also marked blocking, so the review would not let the design go ahead with it (90% without the skill). Both conditions were too cautious on the two clean designs: every review raised a blocking problem there. The planted flaws turned out to be easy for this model, which left almost no room for a difference, and by the reading rules set before the run this test cannot separate the two conditions. The next test uses subtler flaws in more complex designs, where I expect the gap to be larger; that is a hypothesis to test, not a result. One change was made after I had seen the results, a fix to how verdicts are read, and it is recorded in `eval/PLAN.md`. The full summary is in `eval/results/summary.md`. The 72 reviews are in `eval/outputs/raw_runs.jsonl`, the hand scores in `eval/scoring/sheet.csv`, and the key that unblinds them in `eval/scoring/_key_DO_NOT_OPEN.csv`; `python analyze.py` reproduces the summary from these. Don't rerun `make_scoring_sheet.py` in this copy: it would overwrite the scores with a blank sheet.

## Repository layout

```
skill/agent-experiment-methodology/   the skill (SKILL.md + references/)
eval/designs/                         12 test designs (D01–D10 flawed, C01–C02 clean)
eval/answer_key.yaml                  planted flaws and detection criteria
eval/prompts/                         the shared user prompt and the two system prompts
eval/PLAN.md                          pre-specified evaluation protocol
eval/*.py                             freeze, run, blind scoring sheet, analysis
```

## Scope and status

This is a review aid. It does not analyze collected data, build your experiment harness, or replace a methodologist or an ethics review. This is version 0.1, and feedback and issues are welcome.

## License and citation

MIT License. If you use the skill or the evaluation, please cite it with `CITATION.cff`.

# Computational and model-based experiments

This covers how agent experiments run as software: runs, randomness, models, materials, logs, failures and the freeze. Read it whenever the experiment runs in software — every agent experiment does — or uses models as subjects or coders. It adds the checks that physical experiments don't need; the general audits in SKILL.md still apply, and `agent-hazards.md` lists the hazards these checks guard against.

Contents
1. Units and the population a claim is about
2. Randomness and run order
3. Model identity, access and fallback
4. Materials and prompt equivalence
5. Observability and exposure logging
6. Scripted null-behavior runs
7. Failures, retries, limits, exclusions
8. Raw records and derived data
9. Pilot use and the freeze manifest
10. What "reproducible" has to mean

---

## 1. Units and the population a claim is about

- **A run is one draw.** It samples one specific combination of model, task, wording, environment state and configuration. Repeating a configuration samples the model's response distribution *for that configuration*. It does not sample new tasks, new wordings or new models.
- **Match replication to the claim.** Name the population the claim is about, then replicate at that level:

  | The claim is about | Replication needed |
  |---|---|
  | This model on these tasks | Repeated runs |
  | This model on tasks like these | Distinct tasks |
  | Other wordings of the prompts | Paraphrases |
  | Agents built on other models | Several models or model families |
  | Other environments or counterparts | Several environments or counterpart types |

- **Interacting agents are not independent observations.** When agents interact within a run, the run (the team, conversation or simulated world) is the unit of assignment and of independence.
- **Model subjects are not human subjects.** A pattern found in model agents can motivate a claim about people or organizations, but cannot establish one. Any claim about human or organizational behavior needs explicit scope conditions.

## 2. Randomness and run order

Separate the sources of randomness and record each:

| Source | What to do |
|---|---|
| (a) Assignment: conditions, task allocation, option position and labels, speaking order, run order | Seed it and log it. |
| (b) Task, scenario and persona generation | Seed it and version the generator. |
| (c) Model sampling | Record the decoding and reasoning settings. Use provider seeds where supported, but assume residual nondeterminism even at temperature 0. |
| (d) Environment: simulated users, stochastic environments, live services | Seed what can be seeded; snapshot or log what cannot. |
| (e) Infrastructure: batching, timeouts, retries, rate limits | Record it. |

**Seeds.** Derive every per-run seed from one master seed, so any run's *inputs* can be regenerated. Do not claim exact replay of outputs where the provider doesn't guarantee it. Claim regenerable inputs and distributional reproducibility, and archive the actual outputs.

**Run order.** Randomize run order so conditions are interleaved in time; otherwise provider-side changes, rate limiting, live-environment changes or time-of-day effects can line up with condition. Prefer shuffling within blocks that each contain every condition (and task) combination: a study that stops early, or has to switch model at a block boundary, then stays balanced. Retries must not change the order or the realized allocation. Concurrency can matter too: if conditions run with different parallelism, rate limits and timeouts can hit them differently.

**Decoding and reasoning settings.** Temperature, reasoning effort and thinking budgets are part of the design: they decide which response distribution is studied. Justify them, use the same settings for every role and condition unless a setting is itself the manipulation, and keep them fixed. In multi-agent studies, temperature also sets how diverse the agents' outputs are, which matters for votes and debates. If sensitivity to them matters, vary them as a pre-specified robustness factor.

## 3. Model identity, access and fallback

Record for every call:

- the provider;
- the exact model snapshot requested — never a floating alias such as "latest" — and the model the response reports, because some clients and plans substitute a different model when a usage limit is reached;
- decoding and reasoning settings (temperature, reasoning effort or thinking budget, maximum tokens);
- system and developer prompts;
- tool definitions and structured-output settings;
- token counts;
- the timestamp.

Changing the model, its version or its settings is a protocol change.

**Access and fallback.** Access to a model can end partway through a study: usage limits, rate limits, outages, deprecation. An unplanned switch lines the model up with run order and time, so decide before the freeze what happens.

- Use one model and setting for each confirmatory comparison. If the primary model can't reliably cover the whole main study, run the whole study on the fallback instead.
- Pre-specify the fallback model and settings, what triggers a switch, and what happens to completed runs.
- If access is lost mid-study, prefer pausing until it returns. If a switch is unavoidable, make it at a block boundary of a blocked run order (§2), so every condition is balanced within each model's runs. Treat the model as a block factor and report the effect for each model separately: a pooled estimate weights the models by when access ran out.
- Call subject models through an interface that pins the exact snapshot, not a client or plan whose model can change with usage. Whatever the interface, check the served model in the logs.
- Never switch models, or choose between models' results, because of what the results show.

Expect deprecation: archive raw outputs and document the snapshot. Cross-model robustness is a separate, pre-specified analysis, not a substitute to switch to when the first model disappoints. A fallback from the same model family does not test robustness across families.

## 4. Materials and prompt equivalence

- **One source, one template.** Generate all condition materials from one data object through one template. Condition differences should enter only through named fields. Framework defaults (a library's built-in system prompt, its default tool descriptions or retry rule) count as materials: write them down.
- **Diff what each agent receives.** Render the full input every agent receives in each condition and diff the versions. Classify every difference as intended, entailed or accidental. A clean diff is an implementation invariant.
- **Treatment content written by agents.** If a participating agent writes the treatment content, its wording can carry part of the effect. Scripted content from one template, agent-written content within a constrained schema, and free agent-written content treated as part of the treatment trade control against naturalness; the choice is the researcher's (`agent-protocols.md` §8). Whichever is chosen, log the content actually delivered, so fidelity can be checked.
- **Don't cue the hypothesis.** Prompts and instructions should not signal what behavior is being studied beyond what the condition requires. Models follow instruction-like cues readily: how prominently a tool is described can change how often it is used. How to describe an offered tool is a design choice (`agent-protocols.md` §5).
- **Position, order and labels.** Models are sensitive to where options appear and what they are called. Unless position is itself the manipulation, the options are to randomize or counterbalance these, recording the assignment, or to hold them fixed, which keeps conditions identical but ties the result to that one arrangement. The choice is the researcher's.
- **Paraphrase robustness.** Pre-specify which materials will be paraphrased, how many variants there will be, how they are generated (before any run, by a rule that ignores the hypothesis), and how the results will be compared.
- **Probing agents.** A comprehension or manipulation check can run in a forked context (the same history, in a separate call) so the probe doesn't alter the main trajectory. This is one option among several, each with its own trade-off (`agent-protocols.md` §10).

## 5. Observability and exposure logging

- **Make actions recordable.** If the construct is an action, make it one the harness records — a tool call, a message routed through the controller, a structured field, an environment state change — rather than something inferred from free text. Then check coverage: can the behavior also happen through an unrecorded channel, such as free-text messages or a side effect in the environment?
- **Log exposure.** For every agent and every piece of information an outcome depends on, record when it became visible and from whom. Outcomes about whether an agent used information it received cannot be measured without exposure records.
- **Structured fields for judgments about inputs.** If an outcome concerns which inputs an answer draws on, consider requiring the agent to cite them (document or message identifiers) in a structured field, and check the citations by rule. The citations are behavior, not a window into the process, and the requirement can change what it measures; validate any model-based coding that remains against human coding.

## 6. Scripted null-behavior runs

Before piloting with real models, run the full pipeline with scripted agents whose behavior is fixed and ignores the manipulated factor. Typical scripts:

- always act; never act;
- act at random with a fixed probability;
- a constant answer;
- keep the first answer.

`agent-protocols.md` §10 lists scripts for multi-agent outcomes. This is the null-behavior check from SKILL.md (step 3), run at pipeline level. The question is whether the pipeline produces a systematic difference between conditions when behavior ignores the condition — not whether a finite sample shows exactly zero.

- **Deterministic scripts** (always act, never act, constant answer): outcomes should match across conditions exactly, unless the design deliberately makes them differ.
- **Stochastic scripts** (act at a fixed rate): give each scripted unit the same random stream in every condition (common random numbers), so scripted behavior is identical across conditions and any remaining difference is structural rather than sampling noise. Where that isn't possible, compare against the analytically expected value, or run enough scripted replications that a structural difference of practical size would stand out from noise.

A systematic difference means one of two things:

- a structural property of the design, which needs a design or outcome change; or
- a bug in the measurement code.

Passing shows only that this class of artifact is absent. Use the same runs to confirm that every outcome can be reconstructed from the logs, that state resets work, and that every invariant holds. Scripted runs are cheap: they cost no model calls.

## 7. Failures, retries, limits, exclusions

- **Technical failures** — network errors, rate limits, provider errors, harness crashes. Retry with identical inputs under a fixed rule. Log the chain of attempts, and specify whether a retry replaces the failed call or the whole run.
- **Behavioral outcomes** — refusals, off-role behavior, malformed but delivered output, invalid actions or tool calls. Keep and code them: they are data. Retrying them until the output is valid lets the treatment change how many attempts a run gets.
- **Limits.** Step limits, timeouts, output-token limits and context windows are design parameters. Set them so they rarely bind in any condition, and score runs that hit them the same way in every condition. If the researcher's pilot plan allows the pilot to adjust such limits, adjust them then; after the freeze, record each limit hit as its own failure category.
- **Report failure, limit-hit and exclusion rates by condition.** Rates that differ by condition may signal selection bias.
- **Exclusions.** Pre-specify the rules. Analyze all assigned runs wherever possible, scoring failed runs by a fixed rule, and present exclusions as a sensitivity analysis.

## 8. Raw records and derived data

- **Raw records** are append-only and never edited. They cover:
  - every input, output and tool call, with token counts;
  - routing events, memory reads and writes, environment resets and timestamps;
  - seeds;
  - configuration, harness and protocol versions.
- **Derived datasets** are produced from raw records by versioned code, so every analysis row traces back to events.
- **Coding** — whether human, scripted or by an LLM judge — is stored as a separate layer, with coder identity, version and time.

## 9. Pilot use and the freeze manifest

If the researcher decides that the pilot may tune feasibility parameters, it tunes them against criteria stated in advance (SKILL.md, step 9):

- parse rate;
- comprehension;
- manipulation-check success;
- limit-hit and failure rates;
- judge agreement with human labels;
- cost.

It must not tune anything against the hypothesized effect, and pilot data stay out of confirmatory analysis.

At the freeze, write a manifest recording the version or hash of each of these:

- prompts, personas, templates and tool definitions;
- configurations;
- task sets, generators and environment snapshots;
- the harness and other code;
- the model snapshot, decoding and reasoning settings, and the fallback rule;
- judge prompts, coding rules and checkers;
- retry, limit and exclusion rules;
- the analysis plan.

Every main run records the manifest ID.

## 10. What "reproducible" has to mean

"Save the code and the seed" is not reproducibility. A computational experiment is reproducible when someone else can do all four of these:

- regenerate every input exactly, including the environment's starting state;
- re-run it under the same declared conditions;
- trace every reported number to raw events through versioned transformations;
- see every decision — and its origin — that shaped the materials, the sample and the analysis.

# Identification: what a design can and cannot show

Works named in this file are pointers to standard sources, not checked quotations: read a source before relying on a specific claim from it.

Contents
1. Difference tables
2. Bundling patterns to look for
3. The null-behavior check
4. Options when a contrast is bundled
5. Timing traps (including exclusions and missing outcomes)
6. Mechanism claims
7. Assignment, timing, delivery, units and replication

---

## 1. Difference tables

A difference table makes every difference between conditions visible, so the causal claim can be matched to what is actually varied. Its rows list the experimental *system*, not just the manipulation. Start from these rows and add any the study needs; `agent-protocols.md` §9 has the finer agent rows.

| Row | What to record |
|---|---|
| Actors | Who takes part — model agents, scripted agents, simulated users, humans; their roles, personas and stated expertise. |
| Models and settings | Snapshot, provider, temperature, reasoning effort, output limits, per seat. |
| Actions | What each actor may do — message, call tools, write shared state, end the episode, submit or aggregate the output; budgets and limits. |
| Information | What each actor knows, from which source, and when; what is visible to whom; what memory carries. |
| Interaction structure | Who sends to whom; the order; the number of messages, rounds or turns; who speaks first or last; who aggregates. |
| Materials | Prompt wording, length, examples, format, tone, salience and framing; tool descriptions; cues that signal what behavior is expected. |
| Compute | Tokens, samples, steps, tool calls, time and cost per run. |
| Harness | Parsers, retry rules, error messages, step and context limits. |
| Environment | Tasks and their versions; sandbox state and resets; simulated users; external services. |
| Awareness | Who knows which condition is which, and what is being tested: the agents (through their prompts), the people building materials, judges and coders. |
| Treatment delivery | Whether content is scripted or templated, or produced by an agent; channel (system prompt, user turn, message, tool result); timing. |
| Incentives and stakes | What the prompt or environment says is rewarded or penalized; payoffs in games. |
| Measurement | Which units contribute observations to each outcome; how many opportunities the outcome has; scorer; timing. |
| Outcome-determining actor | Whose output is scored, and what that actor was exposed to — directly or only through others. |

Give each condition its own column, and give every comparison arm (including control or baseline arms) its own column too. Then classify every difference:

| Class | Meaning | Consequence |
|---|---|---|
| **Intended** | The theoretical manipulation itself. | — |
| **Entailed** | Unavoidable given the intended difference. For example, a persona manipulation has to add text to the prompt. | It is part of the treatment. Either the claim includes it or the design changes. |
| **Accidental** | Not required. | Remove it, or equate it across conditions. |
| **Outcome-structural** | Changes who is measured, how many opportunities the outcome has, or who determines it. | Can produce a difference with no behavioral effect at all. |

Write down the **estimand as manipulated**:

> "A vs. B estimates the effect of [intended + entailed + any remaining accidental differences] on [the outcome, measured on which units], with [constants] held fixed."

If this sentence differs from the hypothesis, there are two legitimate responses: change the design, or narrow the claim. Keeping the hypothesis's wording while the design tests something else is not legitimate.

## 2. Bundling patterns to look for

Use these as prompts for filling in the difference table. They are not conclusions about any particular study.

| Intended manipulation | Frequently bundled with |
|---|---|
| Persona or role text | added instructions, prompt length, implied goals, partners' replies, output format |
| Number of agents | total compute and samples, message volume, context length, opportunities for the outcome, the aggregation rule |
| Debate, discussion or reflection rounds | compute, context length, the stopping rule, who gives the final answer |
| Tool access | prompt length, the tool description's cues, steps used, time and cost, output format |
| Memory | context length, information carried across tasks, retrieval failures |
| Model or model family | context window, tokenizer, default verbosity and refusals, format compliance, provider infrastructure, cost |
| Prompting technique (examples, reasoning instructions) | output length and token limits, extra instructions, format |
| Communication structure (hierarchical vs. flat, centralized vs. decentralized) | message volume, path length, who aggregates, who speaks last |
| Transparency, explanation, disclosure | added information content, length |
| Framing | information equivalence (frames often leak information) |
| Choice-set composition | set size, option position, labels, which options can be chosen |
| Incentive statements | attention to the incentivized dimension, demand |
| Dose or intensity | exposure duration, repetition, salience |

## 3. The null-behavior check

1. Write down a behavioral model in which the hypothesized effect is exactly zero: every agent acts on its own role and inputs, unaffected by the manipulated factor. If more than one such model is plausible — always act, never act, act at a fixed rate, keep the first answer — try two or three simple ones.
2. Ask whether the measured outcome would still differ systematically between conditions — in expectation, not just by chance.

Common reasons it would:

| Reason | What happens |
|---|---|
| **Different units are measured** | Different roles, or different kinds of agents, contribute the observations in each condition. |
| **Different opportunity** | The treatment changes how often the outcome can occur: more agents, rounds, steps, options or recipients, or longer exposure. |
| **Different input route** | The agent whose output is scored receives the treatment input directly in one condition and only as relayed by other agents in another — for example, an orchestrator that sees tool results itself against one that sees only a worker's summary. |
| **Different denominator** | The outcome is computed relative to quantities that differ by condition. For example, errors per step taken, when one condition takes more steps. |
| **Different aggregation** | A vote or selection over more outputs differs from a single output even when every agent behaves the same. |

**Reading the result.** A failure means the contrast is not isolated under the current design and outcome definition: part of any observed difference is produced by structure, not behavior. More runs cannot remove it. The options are:

- change the design;
- change the outcome definition;
- model the structural component explicitly and state that assumption.

A pass rules out only this class of artifact. It does not show that the contrast is unconfounded.

**Two levels of the check.**

- *Design level:* a thought experiment, or a small simulation.
- *Pipeline level:* push scripted agents through the real pipeline (`agent-protocols.md` §10). A systematic difference between conditions then exposes either a design property or a bug in the measurement code. For stochastic scripts, give each scripted unit the same random stream in every condition, so sampling noise can't pass for an effect.

## 4. Options when a contrast is bundled

| Option | How it works | Cost or limit |
|---|---|---|
| **Equate** | Make accidental differences identical: same wording, length, limits, timing and channel. | Only handles accidental differences. |
| **Focal-unit measurement** | Measure the outcome on agents whose position is the same in every condition — same role, inputs and opportunities. | Fewer observations per run. |
| **Cross factorially** | Vary the bundled elements independently (e.g., number of agents × total sample budget). | More cells, but each effect can be attributed. |
| **Matched control arm** | Add an arm that carries the bundle minus the intended element: a compute-matched arm (one agent sampled as often as the team, with the same aggregation), a length-matched prompt, a placebo tool. | Another arm to run. |
| **Fix the structure, vary the cue** | Hold positions, actions and information flows constant; vary only a persona label or description. | Tests a weaker version of the construct if the construct is inherently structural. |
| **Narrow the claim** | Keep the design and rename the treatment honestly ("debate with three times the samples"). | Claims less. |

Choose in two steps:

1. Decide which version of the claim the research question needs. This belongs to the researcher, because it defines the claim.
2. Pick the cheapest design that identifies that version.

## 5. Timing traps

Lay out the timeline: design time → assignment → treatment delivery → post-treatment behavior → outcome → analysis. Then check for each trap below.

### Circular classification

A condition, task class or moderator is defined by the very behavior the hypothesis is about. Example: "hard tasks are the ones the agents failed", used as a moderator of a prompting technique's effect.

Fix: define such variables structurally, at design time, from the task itself or from data outside the study. Use behavior only to check them. A class defined by a reference model's performance is a property of that model; never take it from the main study's own runs.

### Post-treatment moderators

Subgroups formed after treatment begins are shaped by the treatment. Example: "runs that lasted more than ten turns", or "runs in which the agent used the tool", used to split a component's effect.

Comparisons within such subgroups do not inherit the randomization. Prefer moderators fixed before treatment, such as task properties. If a post-treatment moderator is analyzed anyway, state its causal interpretation and the assumptions it needs.

### Classification under later manipulations

A manipulation may change the inputs of an earlier classification — adding a distractor document can change a task's difficulty class. Compute the class once, at design time, from the state the construct refers to; recompute it under the manipulation as a check; if it moves, decide explicitly which state the class describes, and, where factors are meant to be crossed, regenerate the task or bound the manipulation before the main study. Never reclassify a unit after it has acted.

### Exclusions and missing outcomes

Anything that removes units or periods from a comparison after assignment can leave groups that differ by condition. Deliberate exclusions and unplanned missingness act the same way:

| Source | Examples |
|---|---|
| Exclusion rules | "invalid run" or minimum-length rules; checks placed after treatment |
| Technical failure | crashes, timeouts, context overflows, logging gaps |
| Parse failure | outputs the parser cannot read; malformed tool calls |
| Behavioral non-response | refusals, off-task answers, empty submissions |
| Attrition | agents or simulated users leaving a multi-episode study; humans dropping out |

For each source, ask whether the chance of an observed outcome could differ by condition or depend on treatment-affected behavior. Then:

- prefer a primary outcome defined for every assigned unit — a failed or unparseable run scored as a failure, for example;
- reduce missingness by design: robust parsers, sensible limits, one output schema for all conditions;
- pre-specify the rules, and record the reason for every missing or excluded observation;
- report missingness and exclusion rates by condition;
- analyze all assigned units where possible, with exclusions as a sensitivity analysis;
- treat outcomes with low or possibly treatment-dependent coverage as secondary or exploratory, and specify the missing-data approach in the analysis plan (SKILL.md, step 7).

Dropping units that didn't use the treatment is covered under delivery and use (§7).

### Selecting stimuli on outcomes

Keeping the tasks, scenarios or prompts that "worked" builds the hypothesis into the sample. Pilot-based selection is defensible only when the researcher has decided, before the pilot, that it may inform selection; only on criteria unrelated to the hypothesized effect — comprehension, parseability, manipulation-check success, a feasible difficulty range in every condition; and with the selection frozen before main data collection (SKILL.md, step 9). Even then, the construct becomes "tasks that pass the check"; say so.

### Baseline leakage

An outcome is defined against a "correct" answer or control result computed from the treated data itself, or against a baseline whose own randomness is ignored.

### Exposure defined by behavior

"Unexposed" or "naive" agents should be defined by routing and design. They should not be defined by whether an agent appears to know something.

### Manipulation checks

A manipulation check may come after treatment; it tests whether the treatment was delivered or registered. It does not reassign units. A check-based exclusion must be pre-specified and reported as a sensitivity analysis next to the full sample. An analysis restricted to units that "passed" is not a randomized comparison.

## 6. Mechanism claims

A link X → M → Y is identified experimentally only where its cause is manipulated. When M is measured rather than manipulated, the M → Y relation is observational. Anything that drives both M and Y confounds it: task features, model dispositions, run length. Features of an agent's stated reasoning, how often it called a tool, or how long it deliberated are measured variables.

Ways to handle a measured mechanism:

- **Bound the claim.** Report that X affects M and X affects Y, and that the M–Y association is consistent with the mechanism.
- **Manipulate M in its own arm** (an experimental causal-chain design). Force or block the mechanism behavior — require or disable the tool call, insert or remove the intermediate step — and observe Y.
- **Moderation of process.** Pre-specify conditions that should block or amplify the mechanism, and test whether X's effect on Y changes accordingly.
- **Formal mediation analysis.** This requires sequential-ignorability assumptions that randomizing X does not provide. State them if you use it.

Standard sources when a mechanism claim is central:

- Spencer, Zanna & Fong (2005, *JPSP*) on causal-chain designs.
- Bullock, Green & Ha (2010, *JPSP*) on the limits of mediation analysis.
- Imai, Keele, Tingley & Yamamoto (2011, *APSR*) on identifying causal mechanisms.

## 7. Assignment, timing, delivery, units and replication

### Assignment integrity

| Question | What to look for |
|---|---|
| What is assigned, and at what level? | Run, task, task sequence, simulated world, agent seat, time block; for human participants, the person or group. |
| How is assignment generated? | Every task in every condition (paired), simple randomization, blocked or stratified, counterbalanced (orders, positions, labels, speaking order), or deterministic. Block or stratify on strong pre-treatment predictors of the outcome, such as task difficulty or category, when they exist. Deterministic assignment needs a justification and a check that it can't align with outcome-relevant factors. |
| What are the allocation probabilities? | Unequal probabilities must be known and recorded, because the analysis needs them. Check that the implementation preserves the planned ratio. |
| Can assignment be predicted or influenced? | Choosing which tasks get which condition by hand, running "interesting" tasks first, or (with people) sign-up order and self-selection. Any of these lets assignment track outcome-relevant characteristics. If randomization isn't feasible, state the weaker claim the design supports. |
| Is order itself a treatment? | Position, sequence and carryover — including memory or environment state that carries from one task to the next. Counterbalance or randomize order, and check order effects. |
| Does time line up with condition? | Running conditions in separate batches or weeks confounds them with drift in models, providers, live environments and the harness. Interleave conditions in time. Retries or replacements must not change the order. |
| Can the treatment leak? | Shared files, caches, memory stores, vector indexes or simulated worlds; the same agent instance serving several conditions; cached materials. |
| Is the realized assignment logged? | The plan, the seed or procedure, and the realized allocation must be recorded and checked against each other. |

### Treatment timing

When units start treatment at different times — a component rolled out across a deployed agent's users, or teams that adopt a tool in turn — check what sets the dates.

| Question | What to look for |
|---|---|
| Who or what sets each start date? | Readiness, sign-up or capacity make start dates track unit characteristics. Schedule starts in advance; where they vary across units, randomize or balance their order. |
| Is there a concurrent comparison in every period? | Comparing treated periods with untreated periods from other times confounds treatment with time. Observe untreated units in the same periods. |
| Do predictable shocks coincide with the rollout? | Model updates, product launches, seasons, policy changes. Start before them, balance starts around them, or define outcome windows that separate them. |
| Do exposure durations differ? | Later starters are treated for less time. Fix the exposure duration and outcome window in advance, and record actual start and stop dates. |
| Can units anticipate the treatment? | Behavior can change after an announcement but before the official start. Decide when treatment counts as begun. |
| Can treatment status switch? | Pauses, rollbacks, comparison units adopting the treatment. Record status by period, and decide in advance how switches are handled. |

If start dates vary, flag it for the analysis plan: pooling units treated at different times needs an estimator built for staggered adoption.

### Delivery and use

Assignment is what the design controls; what agents actually receive can differ.

assignment → delivery (what the agent actually received) → use (whether it engaged with it) → outcome

- Define what counts as delivered and as used. A tool that failed to load, a prompt truncated by the context window, or a memory store that returned nothing was assigned but not delivered. Log delivery and use by condition.
- Check for one-sided failures (assigned runs not receiving the treatment) and for contamination (comparison runs receiving it, through shared state or a misrouted configuration).
- Decide which effect the claim concerns. Randomization identifies the effect of assignment. The effect of actual use needs further design features (forcing use in an arm, for example) or explicit assumptions; state that estimand in the analysis plan.
- Comparing only runs that used the treatment with all comparison runs is a post-treatment comparison and doesn't inherit the randomization. The same holds for dropping runs that didn't use it.
- Classify each post-assignment event as delivery, use or outcome. When the hypothesized behavior is the use of something offered, such as calling a tool or consulting memory, that use is the outcome, not non-compliance.

### Units and dependence

Write one line per hypothesis:

| Column | What it records |
|---|---|
| Outcome | The outcome the hypothesis concerns. |
| Observation unit | What each observation is recorded on (a run, an agent within a run, a turn, a tool call). |
| Assignment unit | What receives the condition. |
| Clusters | What observations share (a task, a scenario, a run, a simulated world). |
| Crossing | Which factors vary within which units or tasks. |
| Replication unit of each factor | The level at which independent replication of that factor happens. |

Then check:

- **Assignment above observation.** When conditions are assigned to runs, teams or worlds, that level is the independent unit for the treatment effect. Rows below it — agents, turns, messages, tool calls — are repeated measures.
- **Interference.** Agents that interact affect each other's outcomes: agents in one conversation, units sharing memory, tools or an environment. Define the unit at the level where interference stops, keep conditions from sharing an environment, or measure the spillover.
- **Task-level factors.** If a factor is a property of the task or scenario (difficulty, domain, scenario type) and the claim generalizes beyond the specific tasks, the factor is replicated by distinct tasks, not by runs or seeds. Treat tasks as a sampled factor (Wells & Windschitl, 1999; Judd, Westfall & Kenny, 2012). If the claim is only about the tasks used, say so — repeated runs then suffice, and the claim is narrower.
- **Pseudo-replication.** Many runs of one task or configuration inflate n without adding independent information about the population the claim concerns (Hurlbert, 1984).
- **Composition.** If the units contributing to an outcome differ in kind across conditions, the contrast confounds treatment with unit type.
- **Within-unit designs and carryover.** Some treatments cannot be "unlearned" within a unit that carries state: memory, a shared environment, a revealed answer. Counterbalancing then leaves asymmetric carryover. Reset state, use between-unit assignment, or analyze only the first period.

### Replication screen

These are flags, not power calculations:

- A factor has very few replication units per level — a handful of tasks, scenarios or models — while the claim generalizes beyond them.
- The planned n counts observations below the assignment unit, or repeated runs of the same tasks.
- No primary outcome is designated, or several outcomes are tested with no stated handling of multiplicity.
- No precision target is stated, and no rationale is given for the planned sample.

The analysis, power and precision plan is SKILL.md, step 7, with details in `analysis-planning.md`.

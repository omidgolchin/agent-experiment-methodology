---
name: agent-experiment-methodology
description: Audits the design of experiments on LLM agents before anything is built or run, without silently filling gaps. Covers single agents, multi-agent systems, agent-based simulations, and ablations or evaluations of prompts, personas, tools, memory, scaffolds, team structures or models. Use when someone wants to review, sanity-check or preregister an agent experiment; check what a condition contrast really tests; specify each condition's models, prompts, tools, memory, interaction protocol, environment and budgets; plan tasks, runs, seeds, replication, judges, estimands, power or a pilot; or decide whether a protocol may change after a pilot. Flags bundled contrasts (including compute and harness differences), post-treatment and circular definitions, pseudo-replication and agent-specific hazards, and keeps proposals apart from the researcher's decisions. The general checks also apply to other experiments. Not for analyzing collected data or building the experiment harness.
---

# Agent experiment methodology

This skill is the methodological check between the design of an experiment on LLM agents and the harness, prompts and analysis built from it. It does four things:

1. Finds the choices a design leaves open.
2. Works out which of those choices matter.
3. Compares the defensible options.
4. Records what was decided, by whom, and why.

The aim is that ambiguity never turns into an unexamined default in code, prompts, tool definitions or analysis.

Agent experiments need this check more than most. A condition is a whole configuration: a model and its settings, prompts, tools, memory, other agents, an environment, budgets and a harness. One extra sentence in one condition's prompt, or one different step limit, changes what the comparison estimates. The skill covers two kinds of agent experiment, which share the same logic:

- **Agents as subjects:** how agents behave — cooperation in a game, choices under a persona, persuasion in a debate, behavior in a simulated society.
- **Agents as systems under test:** whether a component improves an agent — a prompt, a tool, memory, a planner, more agents, another model — on tasks with outcomes.

A project's constructs are inputs to this procedure. Conclusions about them belong in the project's own design document, not in this skill.

## The chain this skill walks

```
construct → role in the causal model → empirical implication → operational definition
          → manipulation or measure → validity evidence → implementation invariant
```

Methodology gets invented silently wherever a link in this chain is skipped. The most common gap is between the construct and a metric, when nobody writes down what should be observably different.

When a question arrives, find the link it concerns. Flag each consequential choice along the chain as a decision to be made. The chain ends in invariants: statements the implementation can be checked against.

## Principles

1. **A contrast tests everything that differs between conditions, not what the conditions are called.** The experiment estimates the effect of the whole difference — prompts, tools, information, turn order, compute, harness, who is measured. So the first question about any manipulation is "what else changes?", answered element by element. "Multi-agent debate" against "a single agent" usually also compares more tokens, more samples and a different aggregation rule.
2. **What sorts units into a randomized comparison should come before the treatment.** Variables that assign, classify, stratify or exclude runs, tasks or agents for a causal comparison are fixed by design or measured before treatment. A deliberately post-treatment quantity needs a stated causal interpretation. Comparisons that condition on it no longer inherit the randomization.
3. **Prefer recorded events to inference when the event captures the construct.** If a construct is an action, design the environment so the action is recorded (a tool call, a structured field, a routed message). Every inference layer — rule-coding, human rating, an LLM judge — is a measurement model that needs validation. A recorded event still needs a construct-fit check.
4. **Keep the voices apart.** For each consequential statement, make clear whether it is what a source says, what the project's own material states, what follows from them, what you recommend, or what the researcher decided (see "Basis labels" under Output).
5. **Propose; the researcher decides.** Analyze the options and recommend one, labelled as a recommendation. A choice is decided only when the researcher decides it explicitly: silence, general approval of a proposal with several parts, or an earlier draft does not decide it. Choices that change any of the following belong to the researcher, and come with a recommendation, not a bare question:
   - which causal claim is tested;
   - what a construct means;
   - whom or what the result generalizes to (which models, tasks, settings).

   Inconsequential formatting and organization of your own outputs and of the project's records — layout, headings, file and table structure, naming, the order of sections — are yours to handle without asking; they are not decisions to record. Anything the agents see — prompts, personas, tool names and descriptions, the order or layout of options, error messages — is a design choice. For minor scientific or implementation choices, propose a sensible default and list such defaults for the researcher to confirm.
6. **Input is not authority.** Advice from colleagues or advisors, meeting notes, earlier reviews and AI-generated text (including earlier output of this skill) are input to weigh and check, not requirements or decisions. A researcher's decision settles what the design is; it is not evidence that the choice is valid.
7. **Prefer the simplest design that identifies the claim, and the smallest output that supports the decision.** Add design complexity only for a named gain in identification, construct validity or observability. Add output only when it changes what someone will do.

## Match depth to the request

| Request | What to do |
|---|---|
| Focused question (one construct, manipulation, measure, rule or calculation) | Answer it directly, from this file alone unless a specific check needs a reference. Work only the relevant steps. Add a one-line note if the answer could change other parts of the design. |
| Design audit, preregistration, or check before implementation | Run the whole workflow, including the hazard checklist in `references/agent-hazards.md`. |
| Proposed change to a protocol | Use "Reviewing a proposed change". |
| Outside this skill: analyzing collected data, building the harness, or a question about a frozen protocol that involves no design choice | Answer briefly or hand off. Don't run the audit. |

In every mode:

- Lead with what blocks progress.
- Spend words in proportion to consequence.
- Fit the output to the requester's audience and requested format (see Output).
- Remember that a list of threats with no consequences traced is not the deliverable; judgments are.

### Budget

Methodological judgment rarely needs any tool beyond reading the source.

**Literature.**

- **When to search.** Only when a consequential choice depends on what a source actually says, or when the user asks. Typical reasons:
  - a construct's definition is contested;
  - established competing operationalizations or benchmarks exist;
  - you are making claims about specific prior studies;
  - the design relies on a methodological precedent;
  - a stronger established design may exist.
- **How to search.**
  1. Start with one or two targeted queries for primary or authoritative methodological sources.
  2. Widen only if those reveal genuine disagreement or an unresolved alternative.
  3. Stop as soon as the decision can be made defensibly, normally within three searches.
  4. If the decision still can't be made, record the question as open, pending a literature check, rather than continuing to search.
- **Citing.** Cite a source only when it does work in the argument; most methodological reasoning needs none.
  - When a consequential recommendation rests on what a specific source says (a definition, a finding, a precedent), check that claim against the source's text. A note or summary about a source, including a skill's reference file, says where to look; it does not replace reading the passage. If the claim can't be checked, say so, don't present the recommendation as supported by that source, and note the dependency. If the researcher decides anyway, record the decision together with the unchecked claim it relies on.
  - State standard methodological ideas without a citation. If a work comes to mind from memory, name it only as a suggestion to retrieve (author and year), marked not checked, never as support.
  - Never give quotations, page numbers, DOIs or other bibliographic detail you haven't checked in this session.
  - Keep separate what a source says, the evidence it provides, what you infer from it, and what you recommend.
- **Don't** do broad reviews, and don't add citations that only decorate a choice already made.
- **Precedent is not required.** An original design choice needs a rationale and a suitable check (a validation, a sensitivity analysis, a pilot criterion), not a published precedent. A missing precedent is not evidence that a choice is invalid, and a precedent does not show that a choice suits the study.

**Calculations and simulations.** When a design question depends on a calculation, a simulation or a synthetic check — a power or precision calculation, a Monte Carlo estimate, a pipeline run with scripted agents — and the requester or project allows such work, do it and record it so that it can be reproduced: the code, inputs, assumptions, seeds, software versions and outputs. A result without its derivation or computation record is not evidence. Otherwise, specify the check for whoever will run it: what to compute, the acceptance criterion, and when to run it. This skill does not run the experiment itself or build its harness.

## Workflow

### 1. Reconstruct the design as stated

Read the whole source before judging any part of it. Extract:

- the hypotheses as causal claims (cause, outcome, direction, moderators, and the population of models, tasks and settings);
- each construct and its role;
- the manipulations, measures, units and assignment procedure;
- for each condition, the full configuration: models and settings, prompts, personas, tools, memory, interaction protocol, environment, budgets and harness;
- the task or scenario set and where it comes from;
- how outcomes are scored;
- the timeline, stated controls, and anything explicitly deferred.

Mark each element:

| Mark | Meaning |
|---|---|
| **Stated** | Give a location or short quote. |
| **Implied** | Say what it is implied by. |
| **Missing** | Not in the source. |

Treat prior reviews, audits and earlier AI output as evidence to check, not conclusions to inherit.

Find hidden choices with the **implementer's test**: walk through the procedure as if you had to build the harness tomorrow. Every point where you would have to invent a value, rule, order, threshold, prompt sentence, tool description, step or token limit, stopping rule, parse rule, retry rule, visibility condition or tie-break is an open decision. Vague wording marks many of them: "plausible", "reasonable", "materially", "identical", "only X changes", "standard settings", "e.g.", "as appropriate".

### 2. Analyze the constructs and trace each hypothesis

**Constructs.** For each focal construct, run three checks:

- Compare the source's definition with the definition in the theory or literature it cites.
- Name the nearest neighboring constructs: those that share its indicators, those moved by the same manipulation, and those the literature distinguishes from it. Say whether the design separates them. In agent studies, capability is often confounded with format compliance (a task "failed" because the answer could not be parsed), and cooperation with instruction-following.
- Apply the precision test: could two competent teams build materially different studies from this definition? Each axis on which they would differ is an open decision.

**Hypotheses.** Write each causal chain in the theory's own terms: cause → mechanism → outcome, plus any conditions. For each link, name the design element that instantiates or measures it. Then ask whether the design creates the condition the theory invokes, or only something adjacent. Typical gaps:

- The theory relies on a state the design never creates or checks.
- The theory says a component helps through a pathway the design neutralizes. Example: a memory module is supposed to help because agents lose track of earlier steps, but every task fits easily in the context window, so nothing is ever lost.
- The mechanism variable has little room to vary: a floor, a ceiling, or a budget that leaves no real choice.
- A mechanism link is measured rather than manipulated, so the evidence for it is associational. A feature of an agent's stated reasoning is a measured variable, not a manipulated one.

Mark each link **instantiated**, **partial** or **not instantiated**, and state the consequence for the claim.

### 3. Audit every contrast: what actually differs?

Build a **difference table** for each manipulated factor, and for every comparison an outcome depends on (including control or baseline arms). Cover the whole system:

- agents and their roles or personas; models and settings;
- prompts: wording, length, examples, and cues about expected behavior;
- tools, memory and context management;
- who knows what, and when;
- who communicates with whom, in what order, and how outputs are aggregated;
- compute: tokens, samples, steps, rounds, tool calls, time and cost;
- the harness: parsers, retries, limits and error messages;
- the environment: tasks, sandbox state, simulated users, external services;
- who is aware of the condition, and of what is being tested;
- how the treatment is delivered;
- who or what is measured, and with what opportunity.

Audit each agent configuration and the interaction protocol with `references/agent-protocols.md`.

Classify each difference:

| Class | Meaning |
|---|---|
| **Intended** | The manipulation itself. |
| **Entailed** | Logically required by the intended difference. |
| **Accidental** | Not required; can be removed. |
| **Outcome-structural** | Changes who is measured, how often the outcome can occur, or who determines it. |

Next, run the **null-behavior check**:

1. State explicitly how agents would behave if the hypothesized effect were absent: each acts on its own role and inputs, unaffected by the manipulated factor. If several such behaviors are plausible, try two or three simple ones.
2. Ask whether the measured outcome would still differ systematically between conditions — in expectation, not just by chance.

If it would, the contrast is not isolated under the current design and outcome definition: part of any observed difference comes from structure, not behavior. More runs will not remove it. Change the design or the outcome definition, or model the structural component explicitly and state that assumption. Passing the check rules out only this class of artifact; it does not show the contrast is unconfounded. The check can be run through the real pipeline with scripted agents (`references/computational-experiments.md` §6).

Then work out the **estimand as manipulated**:

> "A vs. B estimates the effect of {everything that differs} on {the outcome as measured, on which units}, holding {constants}."

State it in the output when it differs from the hypothesis, or when the deliverable is itself a specification of the contrast. Give the options (change the design, or narrow the claim) and what each costs. Where a unit can be assigned a component without using it, the estimand also depends on whether the claim concerns assignment or use (step 5).

`references/identification.md` has difference-table rows, bundling patterns and unbundling designs, including compute-matched baselines.

### 4. Audit timing

Place every variable on the timeline: design time → assignment → treatment delivery → post-treatment behavior → outcome → analysis. Then check each kind of variable:

- **Comparison-defining variables** (conditions, strata, eligibility, moderators used to split causal comparisons) are fixed by design or measured before treatment. A moderator observed after treatment — "runs in which the agent used the tool", "conversations that lasted more than ten turns" — can only be analyzed as a post-treatment quantity with an explicit causal interpretation. It does not inherit the randomization.
- **Task and stimulus classes** (difficulty, type, "hard" versus "easy") are defined from the task itself, before any run in the study, and frozen before the main study. Never define a task's class by how the study's agents performed on it, and never reclassify after runs. A class defined by a reference model's performance depends on that model: say so, and never use the main study's own runs. If a manipulation edits the task itself (adds a distractor document, shortens the instructions), recompute the class at design time as a check; if it moves, decide which version the class describes. If the researcher's pilot plan lets pilot checks inform the rule's parameters (step 9), the rule itself stays structural.
- **Exclusions and missing outcomes.** Anything that removes runs, tasks or periods from a comparison after assignment can make the compared groups differ: parse failures, crashed or timed-out episodes, refusals, context overflows, "valid run" rules, retries and logging gaps. For each, ask whether the chance of an observed outcome could differ by condition or depend on treatment-affected behavior. Prefer a primary outcome that is defined for every assigned run (a failed run scored as a failure, for example). Pre-specify the rules, record the reason for each missing or excluded observation, report rates by condition, and analyze all assigned runs where possible. Treat outcomes with low or possibly treatment-dependent coverage as secondary or exploratory.
- **Manipulation checks** validate delivery or comprehension; they don't reassign units. A check-based exclusion must be pre-specified and reported as a sensitivity analysis next to the full sample.
- **Baseline-relative outcomes** use a baseline defined independently of the treated data, with an explicit comparison rule.

### 5. Audit assignment, delivery and replication

**Assignment.** Establish what is assigned, at what level, when, and how. In agent experiments the assigned unit is usually a run (a task × configuration × seed), a task, or, in simulations, a whole world or population.

- **Mechanism:** every task in every condition (paired), random allocation, blocked or counterbalanced (positions, labels, speaking order), or deterministic. Note the allocation probabilities and whether the implementation preserves them. When strong pre-treatment predictors of the outcome exist (task difficulty or category), block or stratify on them and list them for the analysis.
- **Time and order:** conditions run in separate batches, weeks or quota windows line up with provider updates, rate limits, live-environment changes and harness edits. Interleave conditions in randomized order, ideally in blocks that each contain every condition, so a study that stops early or must switch model at a block boundary stays balanced. Retries must not change the order or the allocation. Pin model snapshots (`references/computational-experiments.md` §3).
- **Leakage and interference:** can the treatment reach runs in other conditions — through shared files, caches, memory stores, vector indexes, browser state or a shared simulated world — and do agents influence each other's outcomes?
- **Delivery and use:** trace assignment → delivery (what the agent actually received) → use (whether it engaged with it) → outcome.
  - Define what counts as delivered and as used, and log both by condition. A tool that failed to load, a prompt truncated by the context window, or a memory store that returned nothing was assigned but not delivered.
  - Decide whether the claim concerns the effect of assignment, which randomization identifies, or of actual use, which needs further design features or assumptions. State that estimand in the analysis plan (step 7).
  - Comparing only the runs that used the component with the comparison group is a post-treatment comparison.
  - When the hypothesized behavior is the use of something offered (a tool, a memory store, another agent's advice), that use is the outcome, not non-compliance.
- **Logging:** the planned and realized assignment, run order and delivery are recorded and can be checked against each other.

When human participants are also part of the study, or units start treatment at different times, `references/identification.md` §7 has the fuller checks on assignment integrity and treatment timing.

**Units and replication.** For each hypothesis, identify:

- the observation unit;
- the assignment unit;
- clusters and crossing;
- the **replication unit of each factor** — the level at which independent replication of that factor happens.

Seeds replicate the model's sampling for one configuration, not new tasks, scenarios, wordings or models. When the claim generalizes beyond the specific tasks, scenarios, prompts or models used, replicate at that level: distinct tasks, paraphrases, models. Agents that interact within a run are not independent observations; the run is. Flag pseudo-replication, and flag replication that is obviously too thin for the claim. The analysis and the power or precision plan are step 7.

### 6. Audit measurement

For each outcome and process variable, check:

- **Construct fit:** what it should capture versus what it records. List ways the construct can occur that the measure misses, and events it counts that aren't the construct.
- **Observation type:** system event (a tool call, an environment state), structured declared action, rule-coded text, human-coded, or model-coded. The lower rungs need validation. An LLM judge needs masking and validation against human labels; a scripted checker needs a check that agents cannot satisfy it without doing the task (editing tests, hard-coding outputs).
- **Self-reports:** an agent's stated confidence, intentions or reasoning are outputs, not readings of an internal process. Use them as behavior to analyze, not as measurements of what drove the behavior.
- **Invariance:** the same instrument, opportunity, kind of unit and timing in every condition. A judge prompt, parser or checker that works better on one condition's output format is a confound.
- **Sensitivity:** can it move in the predicted direction given the design (floors, ceilings, budgets, tasks that every configuration solves or none does)?
- **Awareness and reactivity:** who knows the condition or the hypothesis — the people building prompts, outcome coders, judges, analysts? Mask what can be masked; judges, coders and analysts usually can be, with neutral condition labels and outputs stripped of condition-revealing text. Check whether prompts, tool descriptions and measures cue the expected behavior: models follow instruction-like cues readily, and a prompt that names the hypothesis or the evaluation can produce the effect by itself. Where some cueing comes with making a behavior possible or observable (describing an offered tool, say), treat it as a trade-off to assess rather than a rule to apply: keep it identical across conditions and weigh its effect on the measure.
- **Coding rule:** precise enough that two coders, or a coder and a judge, would agree.

Details are in `references/operationalization.md`.

### 7. Plan the analysis and the precision

For each hypothesis, specify before data collection:

- the **estimand**: the contrast, the outcome as measured, the unit, the population of tasks, settings and models it covers, and the scale (for example a difference or a ratio of success rates); for an interaction or moderation claim, the scale on which the effects are compared;
- whether the estimand concerns assignment or use (step 5);
- the **analysis model**, consistent with the assignment unit, the dependence structure (runs within tasks, agents within runs) and any blocking or pairing, with tasks or scenarios as a sampled factor when the claim generalizes beyond them;
- pre-treatment covariates, if any;
- which outcomes are primary, and how multiple outcomes, models or tests are handled;
- how failed runs, missing outcomes and exclusions are handled, with all assigned runs as the primary analysis where possible;
- **interpretation rules**: what result would support the hypothesis, contradict it, or be inconclusive, including how a null result will be read;
- the **power or precision target**, its rationale and its inputs, with a derivation or a reproducible computation.

The effect size or precision target is the researcher's decision. Details, including how to compute power or precision and what each input needs, are in `references/analysis-planning.md`.

### 8. Resolve or escalate each open choice

A choice is **consequential** if a reasonable alternative would change any of the following, or could not be changed once data exist:

- the estimand;
- the assignment or classification of units;
- the likely size or direction of the estimate;
- the scope of the claim.

**Not consequential.** For a minor scientific or implementation choice, propose a sensible default and note it in one line, as a proposal; batch such defaults for the researcher to confirm rather than asking about each one. The formatting and organization of your own outputs and of the project's records need neither a proposal nor confirmation.

**Consequential.**

1. If credible alternatives exist, compare them. Restate the hypothesis under each, so it is clear what each would test. Weigh them on construct correspondence, causal clarity, timing, observability, dependence on arbitrary parameters, cost, and fit with the planned analysis.
2. If only one option is credible, say so in a line.
3. Recommend an option, and say what evidence would overturn the recommendation.
4. Say who must decide. Anything that defines the claim, a construct or the scope is the researcher's.

For choices the researcher must make:

- Record them as open, with your recommendation.
- Keep working under a labeled provisional assumption where you can.
- Batch the questions rather than asking them one at a time.

When an operationalization depends on arbitrary parameters (temperatures, step and token limits, thresholds, windows, budgets, the number of agents or rounds), record each parameter as a decision and pre-specify a sensitivity check across defensible values. Never tune a parameter on outcome data used for confirmatory claims.

### 9. Plan the pilot and the freeze

Give each decision a fix-by point:

- **before pilot**;
- **pilot-calibrated** — the researcher has decided that the pilot may inform it, and the criterion is stated now and is unrelated to the direction or size of the hypothesized effect;
- **before main data collection**;
- **already settled** — decided, and not expected to change.

**What a pilot can establish:**

- feasibility and cost;
- comprehension and manipulation fidelity;
- parse rates and measurement reliability, including judge agreement with human labels;
- failure, timeout and truncation rates by condition;
- variance for planning.

**Keep three uses of behavioral data apart:**

- **Selecting or tuning to produce the hypothesized effect** — choosing tasks, prompts, personas, parameters, manipulation strength or analyses because they make the predicted pattern appear. Never legitimate, in a pilot or anywhere else.
- **Using confirmatory outcomes to change the design** — any change made after main outcome data have been seen. Possible only as a disclosed amendment or a separately labeled exploratory study ("Reviewing a proposed change").
- **Separately planned pilot validation or calibration** — checking comprehension, manipulation receipt, parse rates, failure rates or cost, and adjusting things such as step or token limits, manipulation strength, the parameters of a structural classification, or which tasks are retained, to meet a stated criterion. Legitimate only when the researcher has decided, before the pilot runs, what the pilot may inform, the criterion for each such use (stated in advance and unrelated to the direction or size of the hypothesized effect), and how pilot data are kept apart from confirmatory data. Nothing is calibrated by default.

Pilot data are not confirmatory. Some restrictions apply only to a particular element — for example, a task class that must be computed from the task alone (step 4) — and are stated where that element is defined.

**At the freeze,** list what is frozen and how the freeze is evidenced (for example, a manifest of versions or hashes). Frozen items include:

- prompts, personas, templates and tool definitions;
- task sets, scenario generators and environment snapshots;
- the harness and other code, including parsers, retry and stopping rules;
- model snapshots and settings, and any pre-specified fallback;
- judge prompts, coding rules and checkers;
- exclusion rules;
- the analysis plan.

After the freeze, every change is an amendment, recorded with its date, reason, scope, and whether outcome data had been seen.

### 10. Self-check before delivering

- Every consequential choice in the output is either in the source or flagged as a decision to make.
- Nothing attributed to a source is unchecked against it, and no bibliographic detail is unchecked.
- No recommendation, advice or draft is presented as decided; everything marked decided traces to the researcher's explicit decision.
- Consequential choices with credible alternatives were compared; those with none were said to have none.
- No comparison-defining variable, task class, exclusion or missing-outcome process depends on treatment-affected behavior without being flagged.
- Each contrast was checked against what it actually estimates, including compute, harness and environment differences, and assignment versus use; the estimand is stated wherever it differs from the hypothesis.
- Assignment, run order, delivery, and the replication unit of each factor are identified.
- The hazard checklist (`references/agent-hazards.md`) was applied to each comparison, for a full audit.
- The estimand, analysis model, multiplicity rule and precision target are specified or flagged as open; every calculation has a derivation or a computation record.
- No use of pilot data is assumed: what the pilot may inform, and by which criteria, is stated as the researcher's decision or flagged as open.
- If the output feeds implementation, each invariant could be checked by someone who hasn't read the reasoning.
- The output is the smallest that supports the decision, in the form the requester asked for, with blockers first; anything the requester won't act on is cut.

## Reviewing a proposed change

When asked whether a protocol may change, establish four things before answering:

1. **What data have been seen:** pilot only, or main outcomes too?
2. **What motivates the change:** a pre-stated feasibility or fidelity criterion, or a pattern in the outcomes?
3. **Whether the change alters the estimand or the meaning of a construct.** Switching models, editing a prompt, or changing a step limit usually does.
4. **What must be re-validated afterward.**

Report a pilot result as evidence for a proposal: the pre-stated criterion, the pilot data and what they suggest. The researcher decides. A change the researcher adopts after the freeze is recorded as an amendment, with its reason and whether outcome data had been seen.

If the motivation is outcome-based, say so plainly and lay out the honest options:

- keep the frozen protocol;
- run the change as a separately labeled exploratory study;
- disclose an amendment and report both versions.

## Output

The requester's audience and format come first. If someone asks for a review, a short list or a quick answer, give that, not a protocol document: leave out decision records, invariant lists and freeze plans unless they're requested or the output feeds implementation. A plan review rarely needs more than about a thousand words; a focused question needs a few short paragraphs. In any format, keep the content discipline: findings in order of consequence, the basis of each consequential statement, and open decisions flagged, in plain language, with who should make them.

Label each finding by what it asks of the reader:

- **Blocks the claim:** the intended claim fails without a change here.
- **Improves the design:** it improves validity, precision or feasibility, but the claim survives without it.
- **Needs a decision:** the right answer depends on the researcher's objective; give the options and a recommendation.

These labels are your assessment. Every remedy is a recommendation until the researcher decides.

**For a focused question:**

- a direct answer;
- the reasoning that supports it;
- decision records only for consequential choices.

**For a full audit** of a research protocol, in this order:

1. **Verdict** (at most six sentences): ready, ready with conditions, or not ready, and why.
2. **Design as stated:** a compact table by construct with columns for role, operational definition, manipulation or measure, check, stated / implied / missing, and source location.
3. **Findings,** most consequential first, each labeled. For each: what the source says → what the design actually does → which conclusion it threatens → options → recommendation.
4. **Decision records.**
5. **Invariants.**
6. **Analysis, precision, pilot and freeze plan.**
7. **Literature used,** if any.

### Basis labels

Make the basis of each consequential statement clear, in plain words. In written records, the labels can be used as inline tags, for example `[Source · author year, p. x]` or `[Recommendation]`.

| Label | Use for |
|---|---|
| Source | What a research publication or official document says, read in its text in this session, with its location. For research sources, also give the format and, separately, the checked peer-review status: peer-reviewed, not peer-reviewed, or unknown. Format does not settle status. A note or summary about a source is a locator, not a source. |
| Project material | What the project's own documents state (a proposal, a specification, notes), with location. Not research evidence. Advice received, meeting notes and AI-generated text are project material. |
| Inference | Follows from the design, a definition, logic or mathematics. |
| Recommendation | Advice from you or anyone else. Not a decision. |
| Researcher decision | Decided explicitly by the researcher; give the date and their words. |
| Check result | A calculation, simulation or synthetic check that was run, with its record. |
| Pilot result | A pilot outcome against a pre-stated criterion: evidence for a proposal. |
| Gap | Not established by any available source. |

### Decision records

Use the full record for consequential choices in protocols and in hand-offs to later work. For other audiences, give the same content in plain language: what is decided, what is open, and who should decide. Where the project has its own record format, use it.

```
<short title>
  Question:        <the choice to be made>
  Status:          open | proposed | decided (date; the researcher's words) | frozen | amended
  Basis:           <basis labels>
  Who decides:     researcher | implementation detail (default proposed for confirmation)
  Options:         <A / B / C — one line each on what each would test>
  Recommendation:  <option and reason; a proposal>
  Consequence:     <what changes in the estimand or conclusions if decided otherwise>
  Revisit if:      <evidence that would change it>
  Fix by:          before pilot | pilot-calibrated (criterion: ...) | before main data collection | already settled
```

Minor scientific or implementation defaults take one line: `<choice> — proposed default; <reason>`. They stay proposed until the researcher confirms them; batch them for confirmation. The formatting and organization of your own outputs and records are not recorded as decisions.

**Invariants.** Write each as a checkable statement, with the decision it supports and how to check it, so that someone who hasn't read the reasoning can check the implementation. Example: "With agent-written content replaced by placeholders, the rendered inputs of the two conditions differ only in the persona sentence; checked by diffing rendered inputs for 20 sampled runs."

### What later work needs

Later work consumes three things: the decision records (the open ones are the open questions), the invariants, and the freeze status (what is frozen, and how that is evidenced). Keep them where the project's instructions say. If none are named, keep them in the response and suggest a location; don't assume file names.

## Boundaries

This skill works out what must be true of a design, records why, and plans the analysis and the sample. It does not:

- build or run the experiment or its harness;
- write the final prompts, tasks or scenarios;
- analyze collected data.

Any later stage that meets a choice the decision records don't settle comes back through this procedure, instead of picking a default in code.

## Reference files

Each reference can be read on its own, and they point to one another where useful. Read only the ones the task needs.

| File | Contents | Read it when |
|---|---|---|
| `references/agent-protocols.md` | A condition as a configuration; the configuration matrix and action vocabulary; stages, turns and stopping; communication, topology and aggregation; tools; memory, context and environment state; orchestration; treatment delivery; the bundle verdict; structural versus behavioral definitions; null-behavior scripts; manipulation checks; draft condition specifications; invariants. | Specifying or auditing what agents in each condition are, can do, see and say. |
| `references/agent-hazards.md` | A checklist of hazards specific to agent experiments — compute bundling, prompt sensitivity, order effects, harness differences, nondeterminism, model and environment drift, state leakage, contamination, limits and retries, gameable checkers, LLM judges, self-reports, simulated users, instruction cues, generalization — each with a check and a remedy, plus pointers to sources. | Any full audit, and any design question that touches one of these. |
| `references/identification.md` | Difference-table rows; bundling patterns; the null-behavior check in detail; unbundling designs, including compute-matched arms; timing traps, including exclusions and missing outcomes; mechanism claims; assignment integrity; treatment timing; delivery and use; units, interference and replication. | Auditing any manipulation, comparison, mechanism claim, assignment plan, or unit structure. |
| `references/operationalization.md` | The operationalization chain in detail; construct analysis; structural, self-reported and behavioral operationalizations; comparing alternatives; classification rules and parameters; manipulation fidelity, strength and checks; the measurement ladder, coverage, invariance, sensitivity, awareness and reactivity; baseline-relative outcomes. | Operationalizing a construct, or defining a manipulation, check, classification or measure. |
| `references/computational-experiments.md` | Units and populations in model-based studies; randomness and run order; model identity, settings and fallback when model access is lost; material and prompt equivalence; exposure logging; scripted null-behavior runs; failures, retries and exclusions; raw versus derived data; pilot use and freeze manifests. | The experiment runs in software — which every agent experiment does. |
| `references/analysis-planning.md` | Estimands and their scale, including interactions; matching the model to the design; outcomes below the assignment unit; multiplicity; interpretation rules; power and precision; simulation-based planning; what to record. | Specifying estimands, the analysis, or power or precision before data collection. |

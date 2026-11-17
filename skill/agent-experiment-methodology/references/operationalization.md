# Operationalization and measurement

Contents
1. The operationalization chain
2. Construct analysis
3. Structural, self-reported and behavioral operationalizations
4. Comparing alternative operationalizations
5. Classification rules and their parameters
6. Manipulation design and checks
7. Measurement
8. Outcomes defined against a baseline

---

## 1. The operationalization chain

| Link | What it answers |
|---|---|
| Construct | What is the theoretical definition? |
| Role in the causal model | Is it a cause, moderator, mechanism, outcome or control? |
| Empirical implication | What would be observably different if the construct were high rather than low? |
| Operational definition | What rule could anyone apply? |
| Manipulation or measure | How is it varied or recorded? |
| Validity evidence | What check, validation or reliability estimate supports it? |
| Implementation invariant | What must the materials or code guarantee? |

A design **jumps** when it goes straight from a construct's name to a metric and skips the empirical implication. The metric can then be precise yet measure something else. Write the missing link out; this often reveals that the metric actually captures a neighboring construct. "Collaboration" measured as the number of messages exchanged, or "planning ability" measured as the length of a written plan, are typical jumps.

## 2. Construct analysis

For each focal construct, work through five points.

1. **Definition.** Record the definition the source uses and the definition from the theory or literature it cites, and check that they match. Note any disagreement in the literature that matters for this study.
2. **Neighbors.** Find the constructs it could be confused with:
   - constructs that share its observable indicators;
   - constructs the same manipulation would also move;
   - constructs the literature explicitly distinguishes from it.

   For each neighbor, state what distinguishes the two and whether the design separates them. Common pairs in agent studies:
   - capability vs. format compliance (a correct answer the parser could not read);
   - cooperation vs. instruction-following (cooperating because the prompt implies it is wanted);
   - persuasion vs. agreeableness (changing an answer because of an argument, or because someone disagreed);
   - reasoning quality vs. output length;
   - tool competence vs. tool availability or salience;
   - memory vs. retrieval (the information was stored but not retrieved);
   - consensus vs. convergence on the first or last speaker.
3. **Role.** The role constrains timing and design:
   - A moderator used to split causal comparisons should be fixed by design or measured before treatment. A post-treatment moderator needs an explicit causal interpretation and does not inherit the randomization.
   - A mechanism sits between treatment and outcome.
   - Causes are manipulated; the others are usually measured.
4. **Predictions.** List the observable patterns the theory implies, including any the design does not measure. An unmeasured implication can be a cheap extra test, or a warning.
5. **Precision test.** Ask whether two competent teams, given this definition, could build materially different studies. Each axis on which they would differ is an open decision.

## 3. Structural, self-reported and behavioral operationalizations

| Level | What it is | Typical use |
|---|---|---|
| **Structural** | A property of the task, environment or configuration, set by design and fixed before any agent acts. Examples: a payoff matrix, the communication graph, the tools available, the information each agent holds, a task's difficulty class from data outside the study. | Manipulations and moderators |
| **Self-reported** | What agents (or people) say about themselves. Examples: stated confidence, a stated persona, a stated plan or reason. For model agents these are outputs, not access to an internal state. | Manipulation and comprehension checks; secondary measures |
| **Behavioral** | What agents do. Examples: choices, actions, tool calls, messages, submitted answers, timings. | Outcomes and process measures |

Circularity enters when levels are mixed:

- a structural construct defined by behavior ("hard tasks are those the agents failed");
- a behavioral outcome inferred from a self-report ("the agent was cautious because it said it was unsure").

When the theory's construct is a state (an agent "believing" its partner is human, say), a structural manipulation supports claims about the *structure* only. A claim about the state needs a check showing that the structure moves it — and for model agents, any such check is itself a behavioral or self-reported measure, with the limits that brings.

## 4. Comparing alternative operationalizations

When more than one operationalization is credible:

1. **Restate the hypothesis under each alternative.** This shows what each one actually tests; the restatements often differ more than the metric names suggest.
2. **Compare them on:**
   - correspondence to the theoretical definition;
   - causal clarity — what else each one changes;
   - timing;
   - observability and reliability;
   - dependence on arbitrary parameters;
   - feasibility and cost;
   - fit with the planned analysis.
3. **Ask whether they would plausibly lead to different conclusions.**
   - If not, pick the simpler one and record that in one line.
   - If so, the choice is consequential:
     - recommend one;
     - say what evidence would overturn the recommendation;
     - decide whether a pre-specified robustness analysis using the runner-up is warranted.

When only one operationalization is credible, say so in a line instead of inventing rivals. Convenience, familiarity, a popular benchmark's default metric and mathematical elegance are not reasons on their own.

## 5. Classification rules and their parameters

Any high/low or categorical condition built from a continuous property — task difficulty, scenario conflict, context length — needs all of the following written down:

- **Metric:** what is computed.
- **Inputs and sampling:** what it is computed from — task features, human solve rates, a reference model's pass rate over a stated number of runs.
- **Thresholds:** where the categories are cut.
- **Boundary cases:** what happens near a threshold — an exclusion band, regeneration, or a fixed rule.
- **Ties:** how they are broken.
- **State:** which version of the task or unit is classified (usually the untreated one).
- **Timing:** computed at design time and frozen before the main study runs any unit.

Prefer a clear gap between categories. Record the continuous value for every unit, so analyses can also use it.

**Parameters.** Parameters that look technical often encode substantive assumptions: defining difficulty by a reference model's pass rate makes "difficult" mean "difficult for that model", and a threshold chosen on the subject model's own pilot results ties the classes to that model's behavior. Treat each such parameter as a decision:

- justify it;
- pre-specify a sensitivity check across defensible alternatives;
- never tune it to produce the hypothesized effect, or on outcome data used for confirmatory claims; tuning it against pilot checks is possible only under a pilot plan the researcher has decided (SKILL.md, step 9).

**Later manipulations.** A later manipulation may touch a classification's inputs, for example by adding a distractor to the task. Handle this at design time, before the main study runs any unit, and again after any pilot-informed change to the classification or the manipulation:

1. Recompute the classification under the manipulated inputs. This is a check, not a reclassification.
2. If the value moves, decide explicitly which version the class describes.
3. When factors are meant to be crossed, keep each unit's level on the earlier factor fixed. Regenerate or reject the task, or bound the manipulation.

Never reclassify a unit after it has acted.

## 6. Manipulation design and checks

- **Fidelity.** Confirm that the treatment was delivered as specified to every unit, and log what was actually delivered and whether agents used it. Scripted or templated delivery guarantees identical content; content produced by an agent can be more natural, but it varies, and its wording becomes part of the treatment. Which the claim needs is the researcher's decision.
- **Strength and realism.** A manipulation must be strong enough to register and realistic enough to engage the construct. These pull against each other; say which way the design leans. A persona stated in one clause may not register; one stated in a paragraph adds instructions. Calibrating strength against a manipulation check can be legitimate, but only as a separately planned pilot step the researcher has decided on (SKILL.md, step 9). Calibrating it against the hypothesized effect is not.
- **Cues.** Materials should not signal which behavior is expected or what is being tested, beyond what the condition itself requires. Model agents tend to follow instruction-like cues, so a sentence that names the hypothesis, or describes the study's interest, can produce the predicted behavior by itself (`agent-hazards.md` §4.1).
- **Equivalence of everything else.** Build a difference table (SKILL.md, step 3), and diff the rendered inputs.
- **Checks.** Two kinds:
  - *Comprehension:* did agents register the manipulated attribute (their persona, who their partner is, which tools they hold)?
  - *State:* did it change the intended state, as far as behavior or reports can show?

  Where to place a check is a trade-off for the researcher. A check before the outcome can alter later behavior; a check after the outcome cannot, but its answers can be shaped by what happened; a separate probe in a forked context avoids feedback into the run but measures what is reported outside it (`agent-protocols.md` §10). Checks validate a manipulation; they do not define conditions or reassign units. A check-based exclusion must be pre-specified and reported as a sensitivity analysis next to the full sample.

## 7. Measurement

### Observability ladder

When the construct is an action, prefer higher rungs — provided the recorded event actually captures the construct.

1. A system event recorded by the environment: a tool call, a state change in the environment, a routed message, a timestamp.
2. A structured declared action: the agent selects from a fixed action set in a schema.
3. Rule-coded text: deterministic rules applied to free text.
4. Human-coded judgment: a codebook, coders blind to condition, reliability reported.
5. Model-coded judgment (an LLM judge): a fixed model, version and prompt; validated against human coding on a sample; blind to condition; position-balanced where outputs are compared; reliability reported.

Every rung below 1 adds a measurement model that must be specified and validated. Some constructs are judgments by nature, such as whether an answer is grounded in the documents provided, or whether a message is persuasive. For those, either:

- redesign so the judgment becomes observable (for example, require answers to cite document identifiers, and check the citations by rule — noting that citing is itself a behavior the requirement can change); or
- keep a coded measure and validate it.

Scripted checkers (unit tests, answer matchers, environment-state checks) sit high on the ladder but can be satisfied without doing the task. Check what the agent can see and change of the checker (`agent-hazards.md` §3.1).

### Coverage and false positives

- **Coverage:** list ways the construct can appear that the measure misses. For example, counting calls to a search tool misses information the agent got from another agent's message; a plan can be written and not followed.
- **False positives:** list events the measure counts that are not the construct, such as a reflexive tool call made on every turn regardless of need.

Then decide whether to funnel the construct through the measured channel or to widen the measure.

### Invariance

Every condition must have the same instrument, the same opportunity, the same kind of unit and the same timing. A measure that is easier to trigger in one condition — a parser tuned to one output style, a judge that prefers longer answers when one condition writes longer — is a confound.

### Sensitivity

A measure that cannot vary cannot detect an effect. Check that it can move in the predicted direction given the design. Common obstacles:

- floors or ceilings — tasks every configuration solves, or none does;
- budgets or limits that leave no real choice;
- too few opportunities per unit.

### Awareness and reactivity

- **Who knows what.** List who knows each unit's condition and the hypothesis: the agents (through anything in their prompts), the people writing materials, judges, coders and analysts. Mask what can be masked; judges, coders and analysts usually can be, with neutral condition labels and condition-revealing content removed. When the treatment necessarily reveals itself in the output (a persona's style, a tool's citations), say which biases in scoring remain possible.
- **Reactivity.** Check whether the act of measuring, or the materials, change the behavior being measured. Examples: an output field that announces what matters, or a prominently described tool that invites its own use.

### Coding rules

A coding rule must be operational enough that two coders, or a coder and a judge, agree. Define:

- the coding unit;
- the decision rule;
- how ambiguous cases are handled;
- what happens when the item to be coded is missing.

## 8. Outcomes defined against a baseline

When an outcome is "different from control" or "differs from the correct answer", define four things:

- **Comparison distribution:** a single modal answer, or the full distribution.
- **Baseline estimation:** how a stochastic baseline is estimated — how many baseline runs per task.
- **Pairing:** matched task, or matched seed.
- **Decision rule:** what counts as "different".

If the baseline is itself uncertain, a binary "differs from the modal answer" mixes treatment effects with baseline noise. Prefer distributional estimands, such as the shift in answer probabilities between paired baseline and treated runs.

# Analysis and precision planning

Read this when specifying estimands, the analysis model, multiplicity handling, interpretation rules, or power or precision before data collection (SKILL.md, step 7). It covers planning only, not the analysis of collected data. The effect sizes, precision targets and error rates it asks for are the researcher's decisions; the procedure says what each needs.

Contents
1. Start from the estimand
2. Match the model to the design
3. Outcomes measured below the assignment unit
4. Multiple outcomes and tests
5. Interpretation rules
6. Power and precision
7. Simulation-based planning
8. What to record

---

## 1. Start from the estimand

For each hypothesis, write the target quantity before choosing a model:

| Element | What to state |
|---|---|
| Contrast | which conditions are compared, and at which levels of any other factor |
| Outcome | as measured, with its scoring rule and observation window |
| Unit | the level at which the effect is defined and averaged (for example the run, the task, or an agent within a multi-agent run), and how it relates to the assignment unit. If it is below the assignment unit, say whether runs or agents are weighted equally: the two differ when the number or kind of measured agents differs by condition |
| Population | the tasks, settings and models the claim covers; if it generalizes beyond the tasks used, tasks are a sampled factor |
| Summary and scale | a difference in means or success rates, a ratio, an odds ratio; the scale is part of the claim |
| Assignment or use | randomization identifies the effect of assignment; the effect of actual use needs more (`identification.md` §7) |

Start from the estimand as manipulated (SKILL.md, step 3). If it differs from the hypothesis, change the design or narrow the claim before planning the analysis.

**Interactions and moderation.** A claim that an effect is larger under one condition than another — a technique helps more on hard tasks, or more for smaller models — depends on the scale. With a binary outcome, an interaction can be present on the probability scale and absent on the log-odds scale, or the reverse, and a model without a product term on one scale generally implies an interaction on the other. Choose the scale that matches the claim — the probability scale when the claim concerns how many more tasks are solved — and state the interaction contrast on it (in a 2 × 2 design, the difference between the two simple effects). Report the other scale as a check. Base rates near a floor or ceiling can create or hide an interaction on either scale; check the expected base rates in each cell.

## 2. Match the model to the design

- **Unit of analysis.** Analyze at the assignment unit, or model the dependence among observations within it. Rows below the assignment unit (agents, turns, messages, tool calls) are repeated measures, not independent replications.
- **Paired designs.** When every task runs in every condition, analyze the paired differences by task, or include task effects; this usually gains much precision.
- **Dependence.** Choose an approach that matches the structure: summaries at the assignment unit; cluster-robust standard errors (clustered by task when tasks are repeated); generalized estimating equations, which estimate population-averaged effects; or multilevel models, which estimate unit-specific effects. With nonlinear links such as the logit, population-averaged and unit-specific effects differ; say which one the claim needs. With few clusters, cluster-robust standard errors are unreliable without a small-sample correction.
- **Tasks as a sampled factor.** When the claim generalizes over tasks or scenarios, model task variation (for example, random effects for tasks), not only task labels; with several models, decide whether models are fixed levels or a sampled factor.
- **Blocking and stratification.** Include the blocking or stratification variables in the analysis.
- **Covariates.** Use only pre-treatment covariates, chosen in advance, such as task features. They can improve precision, but they must not change the estimand. With a logit link, adjusting for covariates changes the conditional odds ratio even under randomization, because odds ratios are non-collapsible; if the estimand is a marginal effect, report a standardized (marginal) estimate. If the estimand is a conditional odds ratio, the covariate set is part of its definition.
- **Specification.** Write the model precisely enough that someone else could run it: the formula, link, covariates, cluster structure, estimation method, software and version, the exact contrast reported, and what is done if the model fails to converge.

## 3. Outcomes measured below the assignment unit

- An outcome recorded per agent, turn or message is clustered within the run. Either summarize it at the run (a rate, any or none, a count) or model the clustering.
- Restricting an analysis to a subset defined after treatment — for example "among runs in which the agent called the tool" — is a post-treatment comparison and does not inherit the randomization (`identification.md` §5).
- When different kinds of agents, or different numbers of opportunities, contribute observations in different conditions, the contrast mixes treatment with composition. Fix it in the design or the outcome definition (`identification.md` §3).
- A count bounded by the number of opportunities (for example, how many of a run's agents reached the correct answer) needs a model or summary that respects the bound.

## 4. Multiple outcomes and tests

- Designate the primary outcomes and hypotheses; label the rest secondary or exploratory. Agent studies tend to collect many outcomes cheaply (success, cost, steps, tool calls, judge scores); collecting them is fine, testing them all as primary is not.
- Pre-specify how multiplicity is handled: a fixed testing order (hierarchical or gatekeeping), a family-wise or false-discovery-rate correction, or an explicit decision to report unadjusted estimates as exploratory. Several models, task subsets or judge rubrics multiply tests the same way.
- A mechanism argued from a sequence of tests (the treatment moves the mechanism; the mechanism predicts the outcome) mixes experimental and observational links. Only links whose cause is manipulated are experimental (`identification.md` §6).

## 5. Interpretation rules

- For each hypothesis, state in advance which results count as support, as contradiction, and as inconclusive.
- If a null result may be read as "no meaningful effect", plan for it: define the smallest effect that would matter, and use an equivalence test or a confidence interval that excludes it, rather than reading non-significance as absence.
- For a directional hypothesis, say how a reversed effect will be reported.
- For robustness checks (another model, paraphrased prompts, another task set), state in advance which pattern counts as the result holding and which would narrow its scope.
- When cost or compute differs between conditions, say in advance how a gain that comes with higher cost will be described.

## 6. Power and precision

**Choose the target.** Either power to detect a specified effect, or a target precision, such as the width of a confidence interval for the primary estimand. The effect or precision used is the researcher's decision, with a rationale: the smallest effect that would matter for the claim, decision relevance, prior evidence, feasibility. A published or pilot estimate of the effect is not a sound target on its own: estimates from small samples are imprecise, and estimates selected for being notable are inflated.

**Count the right units.** Power for a factor depends on its independent replications: distinct tasks for a task-level factor, assignment units for a unit-level factor. When the claim generalizes over tasks, many runs of a few tasks add little power. With clustering, the effective sample size falls as the within-cluster correlation rises; for clusters of equal size m and intraclass correlation ρ, the variance is inflated by the design effect 1 + (m − 1)ρ. Repeated runs of the same task are such a cluster.

**Interactions need more data.** In a factorial design, the interaction contrast is estimated with more error than a main effect at the same sample size; in a 2 × 2 design with equal cell sizes and variances, the standard error of the difference between the two simple effects is twice that of a main effect (the difference between the two marginal means). A hypothesis that an effect shrinks, rather than reverses, is harder still to detect. Compute power for the interaction directly; never infer it from the main effects.

**Inputs and their sources.** Give each input's source (a prior study; the pilot, if the researcher's pilot plan includes this use (SKILL.md, step 9); an assumption) and its uncertainty: base rates per cell, variance components, intraclass correlations, the correlation between paired conditions, opportunities per unit, and expected failure and exclusion rates. Pilot estimates of variability are planning inputs, not facts; reflect their uncertainty, for example by planning across a range.

**Sensitivity.** Report the required sample, or the achievable precision, across a grid of defensible input values, not at a single point.

**Analytic or simulated.** Use an analytic formula when its assumptions match the design and the planned analysis, and show the derivation or cite its source. Otherwise simulate (§7).

**Sequential and adaptive plans.** Stopping early, or adding runs after looking at the results, changes error rates unless the rule and its error control are specified in advance. Running "a few more tasks" because a result is close to significance is such a change.

## 7. Simulation-based planning

1. Write the data-generating model: the design (conditions, tasks, runs, agents, rounds), the outcome model, and its parameters under the effect of interest and under the null of each tested contrast.
2. Generate data as the design would, including dependence, failures and exclusions.
3. Analyze each simulated dataset with the planned analysis, exactly as specified.
4. Estimate power as the share of simulated datasets that meet the planned criterion. Its Monte Carlo standard error is √(p(1 − p)/S) for S datasets; choose S so that this error is small relative to the decision.
5. Simulate under the null of each tested contrast, on the claim's scale, with the other effects at plausible values. Check that the false-positive rate is within Monte Carlo error of the nominal level. If it is not, the analysis does not test the claimed contrast on that scale, or the simulation is wrong.
6. Repeat across the sensitivity grid.
7. Record the code, the parameter values and their sources, the seeds, the software and versions, and the outputs.

## 8. What to record

For each primary hypothesis: the estimand; the analysis model; the multiplicity rule; the interpretation rules; the power or precision target with its rationale; the inputs with their sources; the derivation or computation record; and the sensitivity results. Mark each element as decided by the researcher or proposed.

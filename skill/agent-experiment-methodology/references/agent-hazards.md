# Hazards specific to agent experiments

Read this for any full audit of an agent experiment, and whenever a design question touches one of the hazards below. Each entry says what goes wrong, how to check for it, and the usual remedies. The remedies are options; which one fits is the researcher's decision when it changes the claim. The general audits in SKILL.md still apply; this file adds what agent experiments make likely.

The pointers at the end name sources on several of these hazards. They were checked for authors, title, year and venue on 2026-11-10; no passage from them is quoted or summarized here. Read the source before relying on a specific claim from it.

Contents
1. Comparisons
2. Runs, models and environments
3. Measurement
4. Cues, counterparts and generalization
5. Quick screen
6. Pointers

---

## 1. Comparisons

**1.1 Compute travels with the treatment.** More agents, more debate or reflection rounds, more samples, a larger step limit or a longer output limit all add tokens and attempts. A gain may come from the extra compute rather than from the structure or the technique.
- *Check:* tokens, model calls, samples, steps and cost per run, by condition, in the difference table (`agent-protocols.md` §9).
- *Remedies:* add a compute-matched arm (the single agent sampled as many times as the team, with the same aggregation rule; the same token budget spent differently); report outcomes against cost; or name the compute in the claim ("debate with its added compute").

**1.2 One prompt is one draw.** Wording, formatting, separators, example choice and option labels can move results by themselves. A comparison made with one wording per condition tells you about those two wordings.
- *Check:* whether the claim is about a technique in general or about these exact prompts.
- *Remedies:* treat paraphrases or format variants as a sampled factor (several per condition, generated before any run by a rule that ignores the hypothesis); or narrow the claim to the prompts used. Keep everything except the treatment fields identical (`computational-experiments.md` §4).

**1.3 Order and position.** Models respond to where things appear: options in a list, documents in the context, agents in the speaking order, conversations shown to a judge.
- *Check:* every ordered element that agents or judges see, and whether its order is fixed, randomized or tied to the condition.
- *Remedies:* randomize or counterbalance with recorded seeds, or hold the order fixed and say the result is tied to it. For pairwise judging, present each pair in both orders.

**1.4 The harness differs between conditions.** Different frameworks, parsers, retry rules, error messages or default prompts in each condition are part of the contrast. Comparing two published agent frameworks compares everything in them.
- *Check:* rendered inputs, parser code and retry rules per condition; framework defaults that were never written down.
- *Remedies:* one harness with the treatment as a named setting; or declare the comparison as one between whole systems.

**1.5 Model comparisons bundle the model.** "Model A against model B" also compares context windows, tokenizers, default verbosity, refusal and format-compliance rates, provider infrastructure and cost.
- *Check:* parse and refusal rates by model in the pilot; whether one prompt was tuned on one model.
- *Remedies:* report these rates by model; score failures the same way for all; avoid prompts developed on only one of the compared models, or disclose it.

## 2. Runs, models and environments

**2.1 Nondeterminism.** Outputs vary between identical calls, even at temperature 0, because of batching and infrastructure. A single run per configuration is one sample.
- *Check:* the number of runs per configuration, and whether variation between runs is estimated.
- *Remedies:* repeat runs, and analyze them as repeated measures within tasks; claim distributional, not exact, reproducibility (`computational-experiments.md` §§2, 10).

**2.2 Model drift and substitution.** A model name can point to different snapshots over time, and some clients serve a different model when a limit is reached.
- *Check:* whether an exact snapshot is requested and the served model is logged on every call.
- *Remedies:* pin snapshots; log the served model; interleave conditions in time; pre-specify a fallback (`computational-experiments.md` §3).

**2.3 Environment drift.** Live websites, search results and APIs change. Runs at different times see different environments.
- *Check:* every external service the agent can reach.
- *Remedies:* use a snapshot or a cache, or record every return; interleave conditions so drift cannot line up with them.

**2.4 State leaks between runs.** Files, databases, browser profiles, caches, memory stores, vector indexes and simulated worlds can carry information from one run to the next, or from one condition to another.
- *Check:* what persists after a run ends, and who can read it.
- *Remedies:* reset to a recorded snapshot before every run and log the reset; separate stores per condition; if tasks are meant to run in sequence, make the sequence the unit (`agent-protocols.md` §6).

**2.5 Contamination and shortcuts.** Public tasks and their solutions may be in the model's training data, and an agent with web or file access may find the answer instead of working it out.
- *Check:* whether the tasks are public; whether tools can reach solutions, test files or answer keys.
- *Remedies:* block access to solutions and evaluation files; log tool calls and screen them for shortcuts; where possible, use tasks created after the model's training data or held out from publication. Contamination that affects both conditions equally still limits what the absolute numbers mean.

**2.6 Limits that bind unequally.** Step limits, timeouts, maximum output tokens and context windows can cut off one condition's runs more often, especially when the treatment makes runs longer.
- *Check:* the share of runs ending at each limit, by condition, in the pilot.
- *Remedies:* set limits so they rarely bind in any condition; score runs that hit a limit the same way in every condition; report the rates. If the limit is itself the manipulation, say so (`computational-experiments.md` §7).

**2.7 Retries that resample the outcome.** Retrying until the output parses, or until the agent "succeeds", lets the treatment affect how many attempts each run gets.
- *Check:* the retry rule and what triggers it.
- *Remedies:* retry only transport errors, with identical inputs; count everything else as data; log every attempt.

## 3. Measurement

**3.1 Checkers can be gamed.** An agent can satisfy a scripted checker without doing the task: editing or deleting tests, special-casing the checked inputs, writing to the file the checker reads.
- *Check:* what the agent can see and change of the checker and its inputs; a manual read of a sample of successful runs.
- *Remedies:* hidden tests outside the agent's reach; checks that the tests and protected files are unchanged; pre-specified rules for what counts as gaming and how it is scored.

**3.2 LLM judges are instruments.** A model that scores outputs can respond to the condition label, to position, to length or style, and to outputs that resemble its own.
- *Check:* what the judge is told; whether outputs reveal the condition; whether the judge has been compared with human labels on this kind of output.
- *Remedies:* strip condition-revealing content and use neutral labels; randomize or swap positions; validate against human labels on a sample before the main study, and report agreement; fix the judge's model, version and prompt at the freeze (`operationalization.md` §7).

**3.3 Self-reports and stated reasoning.** What an agent says about its confidence, intentions or reasons is output. It need not reflect what produced its behavior.
- *Check:* whether any outcome or mechanism claim rests on an agent's stated reasons.
- *Remedies:* measure behavior where possible; treat stated reasoning as a measured variable, not evidence of the mechanism; manipulate the mechanism when the claim depends on it (`identification.md` §6).

**3.4 Outcome definitions that favor one format.** A parser or judge that handles one condition's output style better produces a difference in scores, not in behavior.
- *Check:* parse rates and judge behavior by condition on pilot outputs.
- *Remedies:* one output schema for every condition; parse failures scored identically; a parser tested on each condition's outputs.

## 4. Cues, counterparts and generalization

**4.1 Instruction cues and agreeableness.** Models tend to do what a prompt implies is wanted. A prompt that names the hypothesis, describes the evaluation, or praises one option can produce the predicted behavior by itself; a user or partner who states an opinion can pull the agent toward it.
- *Check:* every sentence agents see, in every condition, for what it signals about expected behavior.
- *Remedies:* keep the hypothesis and the evaluation out of agent-visible text; keep any necessary cue identical across conditions; when the treatment necessarily carries a cue, name it in the claim (`operationalization.md` §6).

**4.2 Signs of being tested.** Agents may behave differently when a setup looks artificial or evaluative.
- *Check:* whether the materials look like a test (placeholder names, labels such as "Condition B", meta-instructions).
- *Remedies:* realistic, neutral materials; identical framing across conditions; say how far the claim reaches beyond the study setting.

**4.3 Simulated counterparts.** A simulated user, customer or opponent is part of the environment, and its model can interact with the treatment.
- *Check:* the counterpart's model, prompt and seed, per condition.
- *Remedies:* hold them fixed across conditions; consider several counterpart types as a factor; say which kind of counterpart the claim covers (`agent-protocols.md` §6).

**4.4 Generalization across models and tasks.** One model is one draw from the models a claim might cover; one task set is one draw from the tasks.
- *Check:* the population named in the claim.
- *Remedies:* several models or families, and distinct tasks, when the claim is general; otherwise narrow the claim (`computational-experiments.md` §1).

**4.5 Model agents are not people.** Agents simulating people can motivate claims about human behavior but cannot establish them.
- *Check:* whether any conclusion is stated about humans or organizations.
- *Remedies:* explicit scope conditions; human data for human claims.

## 5. Quick screen

For a short review, ask these per comparison:

1. Is compute matched, or named in the claim?
2. Are tasks, prompts and models replicated at the level the claim needs?
3. Is every ordered element randomized, counterbalanced or declared fixed?
4. Are models pinned, the environment frozen or logged, and state reset between runs?
5. Can agents reach solutions, tests or the checker?
6. Do limits, retries or parse failures differ by condition, and how are they scored?
7. Is any judge masked, position-balanced and validated?
8. Does any agent-visible text cue the hypothesis?

## 6. Pointers

| Hazard | Source | Format and status |
|---|---|---|
| 1.1 | Kapoor, S., Stroebl, B., Siegel, Z., Nadgir, N., & Narayanan, A. (2025). AI agents that matter. *Transactions on Machine Learning Research*. arXiv:2407.01502. | Journal article; peer-reviewed |
| 1.1 | Li, J., Zhang, Q., Yu, Y., Fu, Q., & Ye, D. (2024). More agents is all you need. *Transactions on Machine Learning Research*. arXiv:2402.05120. | Journal article; peer-reviewed |
| 1.2 | Sclar, M., Choi, Y., Tsvetkov, Y., & Suhr, A. (2024). Quantifying language models' sensitivity to spurious features in prompt design, or: How I learned to start worrying about prompt formatting. *ICLR 2024*. arXiv:2310.11324. | Conference paper; peer-reviewed |
| 1.3 | Pezeshkpour, P., & Hruschka, E. (2024). Large language models sensitivity to the order of options in multiple-choice questions. *Findings of NAACL 2024*. arXiv:2308.11483. | Conference paper; peer-reviewed |
| 1.3, 3.2 | Zheng, L., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *NeurIPS 2023, Datasets and Benchmarks Track*. arXiv:2306.05685. | Conference paper; peer-reviewed |
| 2.1, 2.2 | Biderman, S., et al. (2024). Lessons from the trenches on reproducible evaluation of language models. arXiv:2405.14782. | Preprint; peer-review status not checked |
| 2.2 | Chen, L., Zaharia, M., & Zou, J. (2024). How is ChatGPT's behavior changing over time? *Harvard Data Science Review*. arXiv:2307.09009. | Journal article; peer-reviewed |
| 3.1 | Zhong, Z., Raghunathan, A., & Carlini, N. (2025). ImpossibleBench: Measuring LLMs' propensity of exploiting test cases. arXiv:2510.20270. | Preprint; peer-review status not checked |
| 3.3 | Turpin, M., Michael, J., Perez, E., & Bowman, S. R. (2023). Language models don't always say what they think: Unfaithful explanations in chain-of-thought prompting. *NeurIPS 2023*. | Conference paper; peer-reviewed |
| 4.1 | Sharma, M., et al. (2024). Towards understanding sycophancy in language models. *ICLR 2024*. arXiv:2310.13548. | Conference paper; peer-reviewed |
| 4.5 | Aher, G., Arriaga, R. I., & Kalai, A. T. (2023). Using large language models to simulate multiple humans and replicate human subject studies. *ICML 2023*. arXiv:2208.10264. | Conference paper; peer-reviewed |
| Analysis | Miller, E. (2024). Adding error bars to evals: A statistical approach to language model evaluations. arXiv:2411.00640. | Preprint; peer-review status not checked |

The hazards, checks and remedies above are design logic and recommendation; a pointer marks where a topic is studied, not support for a specific claim in this file.

# Agent configurations and interaction protocols

Read this when agents — model-based or scripted — act in a study, alone or with other agents, simulated users or people. A condition in such a study is a configuration, and with several agents it is a small organization. Its protocol fixes which agents take part and, for each one, what it is, what it can know, do and say, and when. This file supplies the agent-specific rows of the difference table and the checks that go with them. The difference classes (intended, entailed, accidental, outcome-structural) and the null-behavior logic are those of SKILL.md, step 3, and `identification.md`.

The aim is that no configuration property reaches code as an unexamined default — a framework's default prompt, a library's default retry rule, a provider's default temperature — and that no contrast is described as "only X" while something else also differs. Write every value the design does not settle as `UNSPECIFIED: <question>` and carry it to the open decisions. Never fill it silently: leave it `UNSPECIFIED`, or write a labelled proposed default and list it for the researcher to confirm.

Contents
1. A condition is a configuration
2. The configuration matrix and the action vocabulary
3. Stages, turns, stopping and outputs
4. Communication, topology and aggregation
5. Tools
6. Memory, context and environment state
7. Orchestration and control
8. Treatment delivery
9. Comparing conditions
10. Structural versus behavioral; null-behavior scripts; manipulation checks
11. Draft condition specifications
12. Invariants and reproducibility
13. Reporting a protocol audit

---

## 1. A condition is a configuration

Name a condition by its idea ("debate", "with memory", "expert persona", "planner–executor") and most of what defines it stays hidden. Record each component, for every agent, in every condition:

| Component | Question it answers |
|---|---|
| Model and settings | Which model snapshot, provider and settings (temperature, reasoning effort, maximum tokens)? |
| Instructions | What system prompt, role or persona text, task text and examples does it receive, and from which template? |
| Tools | Which tools can it call, with which descriptions, budgets and return formats? |
| Memory and context | What does it remember within and across episodes; how is its context truncated or summarized? |
| Information | What does it hold at the start, and what reaches it later, from whom, when? |
| Actions | What can it do: message, call tools, write shared state, end the episode, submit, aggregate others' outputs? |
| Output role | Does its output count toward the scored outcome, directly or through aggregation? |
| Budgets | Tokens, steps, tool calls, rounds, wall-clock time, money; enforced by the harness or only stated? |
| Environment | The task, the sandbox and its state, simulated users, external services, other agents. |
| Harness | Parsers, retry rules, error messages shown to the agent, step and context limits. |

Three rules follow.

1. **A role or persona is a bundle until shown otherwise.** A persona label in a prompt usually travels with extra instructions, prompt length, implied goals, and sometimes different tools, turn order or output duties. When a label differs, audit every other component of that agent and every consequence for the agents it interacts with. If nothing else changes, report "label only"; otherwise report the actual bundle ("persona bundle: label + ...").
2. **Stated, enforced and exercised are different.** A capability or limit can exist only as a sentence ("you may search at most five times"), be enforced by the harness, or both; and an available action may never be used in a run. Record, for each, where the agent learns of it, whether the harness enforces it, and whether it is exercised. A limit that is only stated is a cue; a limit that is enforced but never stated (a hidden step limit, silent context truncation) changes the structure without the agent knowing. Which a study needs is a design decision.
3. **Changes are relational.** Changing one agent changes others' inputs and opportunities. A more verbose agent fills its partners' context windows; an agent that may end the episode limits everyone's remaining turns; an aggregator decides whose output counts. Record the consequence on every affected agent.

## 2. The configuration matrix and the action vocabulary

Inventory every actor: model-based agents, scripted agents (fixed policies), simulated users, humans, the controller or orchestrator, tools, the environment, and sinks such as the scored output. A seat is a position; its occupant can differ by condition (a model agent in one, a scripted policy in another; one model in one condition, another model in the next). Record the seat-assignment rule: fixed, random or counterbalanced, and how it is logged.

One row per actor per condition. Every cell holds a value, "none", or `UNSPECIFIED`.

| Column | Record |
|---|---|
| Seat and occupant | the position; model agent, scripted policy, simulated user or human |
| Label or persona | the name and description others see; who is told it |
| Model and settings | model reference; settings |
| Instructions | template identifier; examples; length |
| Tools | tools, budgets, descriptions |
| Memory and context | memory type; context limit and truncation rule |
| Initial information | what is in its context before any flow |
| Information received | from which flows, at which stage |
| Actions | each action in the vocabulary below |
| Output role | whether and how its output enters the scored outcome |

**Action vocabulary.** Write each action explicitly as available or not; an omitted action is a silent default.

| Action | Meaning | Record also |
|---|---|---|
| message | may post | channels; stages; messages or tokens per stage; may initiate |
| call tool | may call a tool | which tool; budget; stages |
| read shared state | sees a shared board, file system, memory store or others' work | which; when |
| write shared state | may change shared files, boards or memory | which; whether others see the change, and when |
| revise own output | may revise its earlier messages or answers | stages |
| edit others' output | may change or replace another agent's output | whose; when |
| aggregate | votes, selects, merges or summarizes others' outputs | the rule; tie-breaks |
| end or extend | may end the episode, or request more turns | conditions under which it takes effect |
| submit | produces the output that is scored | alone or with others; when |

For every available action, also record where it is conferred (instructions, tool definition, harness), what enforces it (the harness, or nothing), and whether it is exercised in a run. When X can edit, replace or select Y's output, write the matching entry on Y: "output may be replaced by X", "output counts only if selected by X".

## 3. Stages, turns, stopping and outputs

- **Stages.** For each stage: who acts; what enters each agent's context, and whether it accumulates; the allowed actions; the outputs and who sees them; when outputs are released (as produced, or together at the stage end); the display order (fixed, or a seeded permutation).
- **Turn order and synchrony.** Who speaks first and last is a design property: last speakers see more, first speakers anchor. With asynchronous turns, arrival order depends on latency and response length, which can differ by condition. Specify the ordering rule, and treat latency-driven order as a possible confound.
- **Initiation.** Who may start an exchange, and through which channels (direct messages, mentions, forwarding).
- **Repetition.** The number of rounds or episodes, and what carries over between them.
- **Stopping.** A fixed number of stages is structural. A rule that depends on behavior (consensus, a "done" token, a submitted answer, a budget running out, a step limit) makes the number of opportunities an outcome. Record the maximum structurally, treat the realized length as behavior, and check whether one condition lets a different agent, or an easier event, end the run.
- **Structured outputs.** The fields per stage and their visibility (public, private, recorded only). Public fields are content flows. No field may name the hypothesis. A field that invites the behavior being measured (a field asking for a confidence rating before acting, when confidence or caution is an outcome) is a reactivity trade-off: it may be needed to make the behavior observable. Flag it, keep it identical across conditions, and consider its effect on the measure (`operationalization.md` §7).

## 4. Communication, topology and aggregation

- **Flows.** For each flow, record: its type (content, control, tool result, feedback from the environment); its real origin and its attributed sender (masking); its recipients after channels are expanded and exclusions removed; its stages; whether it is scripted or agent-written; when it becomes visible and to whom; its position and order; any length limit; any repetition.
- **Content and control.** A content flow changes what the recipient knows without forcing an action. A control flow changes what happens next: a turn token, a selection, a vote, an end signal, a task assignment. Write control flows as flows, not only as actions, so a change in who controls what shows up as a changed edge.
- **Topology.** Is it fixed before the run? Can agents create, drop or re-route links? Classify endogenous links as forbidden, allowed (the realized network is then measured behavior) or studied (link formation is then the treatment). Close off-protocol channels the design does not intend, such as shared files, or identifiers that let agents address each other.
- **Aggregation.** How the system's output is formed: one agent's final answer, a majority vote, a judge agent's selection, the last speaker's answer, a consensus rule, a merge. Record tie-breaks and how invalid or missing answers enter the rule. Aggregation over more outputs uses more samples, which is compute (§9).

**Topology questions, for any contrast in which an edge, channel, route or team size differs:**

| # | Question | How to answer |
|---|---|---|
| 1 | Does node degree change? | count each agent's distinct partners per condition |
| 2 | Does the number of senders per agent change? | in-degree per stage |
| 3 | Does the number of recipients per message change? | out-degree; channel sizes |
| 4 | Does message volume change? | messages and tokens per agent and per run |
| 5 | Does context load change? | tokens each agent receives; whether truncation or summarization starts earlier |
| 6 | Does redundancy change? | how many independent routes deliver the same information |
| 7 | Does path length change? | relays between an information source and the agent whose output is scored |
| 8 | Does source composition change? | which roles each agent hears from |
| 9 | Does timing change? | the stage at which information first reaches each agent; whether a fixed number of rounds lets it reach everyone |
| 10 | Does role composition change? | whether one position also aggregates, relays or speaks last |
| 11 | Does the opportunity to act change? | turns, tool calls and steps left to each agent after it receives the information |

Mark each topology feature **intended** (the manipulated property, named in the treatment definition), **held constant** (equal across conditions by design, shown by the table rather than asserted) or **endogenous** (created by agents during the run; measured as behavior, never part of the condition).

## 5. Tools

| Item | Record |
|---|---|
| Callers | which agents may call the tool, in which conditions |
| Availability | the stages at which it can be called |
| Budget | the number of calls; per agent or a shared pool; enforced by the harness or only stated |
| What consumes budget | an attempt, a success, an error, a timeout |
| Returns | what comes back; whether it depends on the condition (if so, that is treatment content) |
| External state | whether returns depend on a live service (the web, an API) that changes over time; snapshot, cache or log every return |
| Result visibility | caller only, a channel, everyone; immediately or at the stage end |
| Use visibility | whether others see that a call happened, by whom, on what; budget counters |
| Persistence | whether results enter shared memory, notes or later contexts |
| Description | the tool's name, description and argument schema; identical across conditions unless the description is itself manipulated; how prominently it is presented (below) |
| Failure and timeout | what the agent sees; whether budget is kept; whether a call is retried with identical inputs |

**How to present a tool.** The description shapes use as well as understanding, so its prominence is a design choice for the researcher. The risks to weigh: a description that stresses the tool's importance can raise use in every condition, pushing the measure toward a ceiling where differences between conditions are hard to detect, and can signal what is being studied; a bare description can leave agents unsure what the tool does or when it helps, pushing use toward a floor. Options include a neutral functional description (what the tool does and returns); a description matched in length and emphasis to the other tools; or deliberate emphasis, when the claim concerns settings in which the tool is salient. A pilot comprehension check, if the researcher's pilot plan includes one, can show whether the description is understood.

**Comparable tool opportunity.** When tool use is an outcome or a mechanism, every agent whose behavior is measured needs the same tool, budget and budget scope, the same availability relative to when the relevant information arrives, and the same result and use visibility. Common hidden differences:

- results posted to a shared space in one condition, so one call informs everyone and per-agent outcomes depend on the others;
- a pooled budget against per-agent budgets: "the same total" is not the same per-agent opportunity;
- visible tool use, so who called what becomes a social signal;
- a failure rule that consumes budget in one condition only;
- information that arrives later in one condition, leaving fewer steps in which to use the tool.

**Protocol or implementation.** A rule is protocol, and so a decision, when it changes what an agent sees, how much opportunity it keeps, or when it acts. Retrying a transport error with identical inputs, logging and storage are implementation.

## 6. Memory, context and environment state

- **Memory.** Record the type (none; a scratchpad within the episode; a store that persists across episodes; a store shared between agents), what is written, by whom and when, how retrieval works (recency, similarity search, a summary) and what is retrieved. Memory is a leakage path: notes written during task 3 can contain the answer to task 7, and a store filled during one condition's runs must never be read in another condition's runs. Decide whether memory starts empty for every run, for every task sequence, or never resets, and log its contents at each retrieval.
- **Context management.** Record the context limit, the truncation or summarization rule and, where a model summarizes, which model and prompt. Conditions that produce longer transcripts — more agents, more rounds, more verbose personas, tool outputs — reach truncation sooner, so what is forgotten can differ by condition.
- **Environment state.** Reset sandboxes, file systems, databases, browser profiles and caches before every run, and log the reset. No state passes between runs or conditions unless the design says so. Where tasks run in sequence, say whether each sequence is the unit.
- **Simulated users and counterparts.** A simulated user, opponent or customer is part of the environment: fix its model, prompt and seed, and hold them identical across conditions. Its responses depend on the agent's behavior, so it can amplify or dampen a treatment effect; say which claim needs which kind of counterpart (scripted, model-based, human).

## 7. Orchestration and control

When the design assigns subtasks, sets a hierarchy or routes work through a controller, answer for each relation:

| Question | Record |
|---|---|
| Who assigns work? | the orchestrator, or a fixed script; whether it is told it is assigning |
| What is assigned? | a subtask, a tool call, the whole task; with what instructions |
| What does the worker receive? | the full context, or a brief written by the orchestrator |
| What comes back? | the full output, a summary, a status; who writes the summary |
| What does the orchestrator see directly? | tool results, the environment, or only workers' reports |
| What control is kept? | review, rejection, re-assignment, override; when each can be exercised |
| Who can stop the run? | which agent, under which rule |
| Who produces the scored output? | one agent, an aggregation rule, the orchestrator |
| Can the direction reverse? | escalation back, re-assignment to another worker |
| Stated, enforced, exercised? | for every control action that moves |

Then check the classes that commonly move with a change in orchestration (§9): compute, information access, the output owner, control of stopping, and instruction text. The design must say which of them belong to the treatment.

## 8. Treatment delivery

Use this whenever a treatment reaches agents in a message, a prompt, an environment event or through another agent.

| Dimension | Compare across conditions | Typical problem |
|---|---|---|
| Scripted or agent-written | who produces the wording | an agent in a different role frames the same content differently, so wording carries part of the effect |
| Source identity | real origin and attributed sender; masking | the attributed sender changes more than the intended attribute (another model, another role, a human-versus-AI label) |
| Content | everything except the named treatment fields | extra words, a stated reason, a recommendation |
| Timing | stage and position | one condition delivers earlier, or first |
| Length | characters or tokens | a longer message is more salient and uses more context |
| Recipient set | who receives it | different agents exposed, so different agents measured |
| Channel | system prompt, user turn, broadcast, direct message, tool result | the same text in the system prompt and in a user turn is treated differently by many models |
| Repetition | how often it is delivered or restated | a source that remains in the conversation restates its message |
| Visibility | who sees that it was delivered, and to whom | others know who received it |
| Opportunity to respond | can recipients answer the source; can the source answer back | a scripted source cannot respond to objections |
| Opportunity to act | the same tools, budget and remaining steps for every recipient | late delivery in a fixed-length run leaves less time to act on it |

**Scripted or agent-written delivery.** When a property of a message or its sender is the treatment (a partner's style, a negotiator's strategy), who writes the message is a consequential choice for the researcher. Scripted delivery from one template, in which only the named fields differ, holds the content constant, but the message may not read as the sender's own. Agent-written delivery can be more natural, but the wording then varies with the role and can carry part of the effect; a schema or length limit narrows that variation without removing it. Whichever is chosen, log what was actually delivered. If agents write the treatment, the realized wording is part of the treatment as delivered: say so, and define the conditions by the assignment, not by the wording produced.

## 9. Comparing conditions

For each pair of compared conditions, control arms included, build the difference table with one column per condition and these rows:

| Class | Compare | Derived consequence to add |
|---|---|---|
| Agents | presence; kind (model, scripted, simulated user, human); who occupies each seat | team composition; who can respond to whom |
| Labels and personas | label and description per seat; who is told | label only, or a persona bundle |
| Models and settings | snapshot; provider; temperature; reasoning effort; maximum tokens | — |
| Instructions | wording; length; examples; cues | — |
| Tools | tools; descriptions; budgets; returns | — |
| Memory and context | memory type and contents; context limit; truncation | what each agent can still see late in a run |
| Information access | initial information; what reaches whom and when | — |
| Actions | every action, on both sides of each relation; conferred, enforced, exercised | whose output counts |
| Content edges | origin; attributed sender; recipients; stages; visibility | recipients, in-degree, context load |
| Control edges | turn tokens, assignments, selections, votes, end signals | who determines the outcome |
| Compute | tokens, samples, steps, rounds, tool calls, wall-clock time, cost per run | whether the contrast is compute-matched |
| Harness | parsers, retries, error messages, limits | which failures are possible, and how they are scored |
| Environment | tasks; sandbox state; simulated users; external services | — |
| Timing and order | stage of delivery; order within a stage; synchrony; release | first-exposure stage |
| Feedback and iteration | rounds; stopping rule; revision opportunities | number of opportunities |
| Measurement | what is scored; on which agents; how many opportunities; the scorer | outcome-structural rows |

**Bundle verdict.**

1. List every class with a difference.
2. Mark one as intended: the manipulation as the design names it.
3. For every other class:
   - **entailed** only if the treatment's own definition requires it. Cite that definition; if none exists, write "needs a decision: is X part of the treatment?";
   - **accidental** if it can be removed; propose how (equate it, match it, or move it into both conditions);
   - **outcome-structural** if it changes who is measured, how often the outcome can occur, or who determines it. These go to the identification audit (`identification.md` §3).
4. Verdict: "single-class" only when nothing but the intended class differs. Otherwise "bundled: <intended> + <list>". With only entailed differences, write "the treatment is <intended> together with <entailed list>; the claim must name them."
5. State the estimand as manipulated: the contrast estimates the effect of everything that differs on the outcome, measured on which units.

Never describe a contrast as pure, or as "only X", while another class differs. Run the topology audit (§4) whenever any edge, channel, route or team size differs; the delivery audit (§8) whenever a treatment travels in a message or through an agent; and the persona audit (§1, rule 1) whenever a label differs.

**Patterns to look for in agent experiments.** These are prompts for the table, not conclusions about any study.

| Nominal manipulation | Often travels with |
|---|---|
| A persona or role sentence | added instructions; prompt length; implied goals; how partners reply; output format |
| More agents | more samples and tokens (compute); message volume and context load; more chances for the outcome to occur; an aggregation rule |
| Debate, discussion or reflection rounds | compute; context length; a stopping rule; who gives the final answer; the last speaker's advantage |
| Adding a tool | prompt length; the tool description's cues; more steps used; time and cost; a different output format and parser |
| Memory | context length; information carried across tasks; retrieval failures |
| One model against another | context window; tokenizer; default verbosity, refusals and format compliance; provider infrastructure; cost |
| A prompting technique (examples, a reasoning instruction) | output length and token limits; extra instructions; format |
| A planner, orchestrator or hierarchy | compute; what each agent sees directly; who can stop; who owns the output |
| Communication structure | degree; message volume; path length; timing within a fixed number of rounds; a hub that also aggregates |
| Visibility of others' work | one agent's result informing everyone; social signals of who did what |
| Sampling settings | output diversity, and so the number of distinct answers available to a vote |

## 10. Structural versus behavioral; null-behavior scripts; manipulation checks

| Structural: an opportunity the protocol defines | Behavioral: a realized action, an outcome or process measure |
|---|---|
| holds the tool and budget at that stage | called the tool; what it called it on |
| receives the message | used its content |
| may message X | messaged X |
| a memory store is available | retrieved from it; what it retrieved |
| may end the episode | ended early |
| is in the aggregation set | its answer was selected |
| a route exists from the source | information arrived through that route |
| may open links | opened links; the realized network |

- Conditions, strata, exposure classes and "treated" groups are defined from the left column only.
- "Exposed" means routed by the design and recorded by the harness, not "appears to know".
- A behavior-dependent stop makes the number of opportunities an outcome.
- An endogenous change in the network never silently becomes part of a supposedly fixed treatment.

**Null-behavior scripts.** For a pipeline run, give agents fixed policies that ignore the condition, and state which outcomes must then be equal across conditions:

| Script | Use |
|---|---|
| a constant answer; a random valid action from the action set | task outcomes, scoring and aggregation |
| always call the tool; never call it; call it at a fixed rate | tool-use outcomes |
| keep the initial answer; adopt the majority | consensus, conformity and final-answer outcomes |
| send a fixed-length message every turn; send nothing | volume, context-load and spread outcomes |
| always end at the first opportunity; never end early | behavior-dependent stopping |

A stochastic script uses the same random stream in every condition. A difference that remains is structural, or a bug (`computational-experiments.md` §6). An expected inequality is an outcome-structural row: for example, when every agent keeps an independently drawn initial answer that is right with probability p > 0.5, a majority vote over six agents (ties broken at random) is right more often than one over two agents, with no interaction at all.

**Manipulation and comprehension checks.** Whether the study needs evidence that agents registered the manipulation — which persona they hold, who they are talking to, which tools they have — is a design decision for the researcher. The risk to assess is reactivity: asking about the manipulation can make it more salient and change later behavior, while not asking leaves receipt unchecked beyond the delivery logs. The options trade these off:

- **structural evidence only:** the harness logs show the treatment was delivered as specified; this shows delivery, not comprehension;
- **a forked probe:** the same history, asked in a separate call whose answer never enters the run; it avoids feedback into the run, but measures what the agent reports outside it, not what drove its behavior;
- **a probe after the outcome, within the run:** it cannot affect the measured outcome, but its answers can be shaped by what happened during the run;
- **a structured field in the agents' outputs** (for example, naming the partner's role): observed at the moment it matters, but reactive, and part of the protocol in every condition;
- **checks on a subset of runs, or in the pilot only:** less reactivity and cost in the main study, and less evidence about it.

Whatever is chosen, use the same procedure in every condition, state the failure criterion in advance, and treat the results as validation of receipt or comprehension: they never reassign units or redefine exposure, and an analysis restricted to units that passed is a pre-specified sensitivity analysis, not the primary comparison (`identification.md` §5).

**After a failed check.** The response depends on when the check fails and why, and it is the researcher's decision. In a pilot, within the researcher's pilot plan (SKILL.md, step 9), the options include revising the materials or the delivery, revising the check itself if it was unclear, or keeping the manipulation and narrowing the claim to the manipulation as delivered. A revision applied to every condition keeps the conditions comparable; a revision to one condition changes the contrast and goes into the difference table (§9). In the main study, any change is an amendment (SKILL.md, "Reviewing a proposed change").

## 11. Draft condition specifications

A condition specification describes one comparison: a shared system description, plus, per condition, the values that change. If the researcher uses an existing configuration format (a framework's configuration file, a schema of their own), use its vocabulary, and give any property it lacks a field that a comparison of specifications can see. Until then, these neutral blocks are enough for drafts. Either way, never keep a configuration property only in prose or only in framework defaults.

| Block | Holds |
|---|---|
| Metadata | identifier, title, status (draft, decided, frozen, rejected), the decisions it depends on, provisional assumptions, sources with their basis |
| `models` | per model reference: provider, exact snapshot, settings, fallback |
| `stages` | per stage: who acts; turn order; synchronous or not; release rule; display order; tools available |
| `agents` | per seat: kind (model, scripted, simulated user, human, controller); label and persona; model reference; seat assignment; instructions (the wording, or the template that holds it); tools; memory; initial information; actions (§2); output role |
| `channels` | members; release rule; order |
| `flows` | type; real origin; attributed sender; recipients; exclusions; stages; content carried; scripted or agent-written; when and to whom visible; position; length limit |
| `tools` | per tool: description; returns; external state; result visibility; use visibility; budget scope; what consumes budget; persistence; failure and timeout rules |
| `memory` | per store: type; writers; readers; retrieval rule; reset rule |
| `environment` | task set and version; sandbox and reset rule; simulated users (model, prompt, seed); external services and their snapshot |
| `budgets` | tokens, steps, tool calls, rounds, time and cost limits; enforced or stated |
| `harness` | parser; retry rule; error messages shown to agents; context limit and truncation |
| `aggregation` | how the scored output is formed; tie-breaks; invalid answers |
| `stopping` | fixed stages, or the behavior-dependent rule with its maximum |
| `outputs` | per stage: fields and their visibility |
| `topology` | fixed before the run or not; endogenous links (forbidden, allowed, studied); the independent realization (usually the run) |
| `outcomes` | identifier; measured on which agents; stage; scorer; pointer to its definition |
| `checks` | null-behavior scripts; any manipulation or comprehension checks |
| `conditions` | per condition: the values set or removed |
| `declared_differences` | the element; its class (intended, entailed, accidental, outcome-structural); a note |
| `unspecified` | the element; the open question; who settles it |

A specification for open options stays a draft, and every provisional assumption in it is listed as such: an assumption needed to write a draft is not a decision. Exact prompts, persona texts and message wording can be written into the specification or kept in templates that accompany it; either way, they must be available to the design audit, because wording can differ between conditions in ways a field-level comparison does not show (§12). Drafting and comparing wording is design work; a wording is decided only when the researcher decides it. Name the fields that vary between conditions, the fields that must be identical, and where each wording is kept.

## 12. Invariants and reproducibility

State the invariants the implementation must satisfy, each as a checkable statement with the decision it supports and how to check it. Typical ones follow; each applies where the design has made the corresponding choice.

| Area | Invariant |
|---|---|
| Rendered inputs | with agent-written content, tool results and environment observations replaced by placeholders, each agent's rendered input differs between conditions only in the named treatment fields |
| Pre-treatment stages | inputs before delivery are identical across conditions |
| Delivery | for scripted delivery, the treatment comes from one template, with its position and timing fixed; for agent-written delivery, the schema, length limits and logging rules hold |
| Visibility | each flow reaches exactly its specified recipients; private fields never reach others |
| Budgets and compute | limits enforced by the harness as specified for each condition; every call logged with tokens and the budget before and after |
| Release and order | synchronous release where specified; display and speaking order from a recorded seeded permutation |
| Isolation | fresh contexts per run; memory and environment state reset as specified; no state shared across runs or conditions; agents receive only what the specified flows route to them (for example, not each other's hidden reasoning unless a flow carries it) |
| Models | every call requests the pinned snapshot and settings; the served model is logged and matches |
| Labels | no condition, hypothesis or ground-truth label in agent-visible content, unless the design deliberately discloses it |
| Seats | assignment follows the recorded rule |
| Versioning | every run records the specification version, template identifiers and harness version |

A field-level comparison of specifications does not check wording held in templates; compare the rendered inputs as well. The implementation must also log what the outcomes need: every rendered input (or its hash), exposure per agent and stage, tool calls with arguments, results and budget, message routing, release order, memory reads and writes, and the stopping event. Any rule that changes what an agent sees or how much opportunity it keeps is a protocol decision, not something the implementation settles.

**Reproducibility.** Record enough to regenerate every agent's input: the specification version, template identifiers, scripted policies, the environment snapshot, the master seed and how seat assignment, display order and any sampling derive from it, and the model configuration. The claim is distributional reproducibility of outputs, not exact replay (`computational-experiments.md` §§2, 10).

## 13. Reporting a protocol audit

A quick question about one protocol element gets a short prose answer: the direct answer, the one or two consequences that matter, and at most one question back.

For a full protocol audit, report in this order, omitting sections that do not apply:

1. verdict and blockers (at most six sentences);
2. the difference table per comparison, with the bundle verdict;
3. the configuration matrix by condition, where a reader needs it;
4. the stage and turn timeline;
5. flows, visibility, topology and aggregation;
6. tools, memory, context and environment state;
7. orchestration and control, if relevant;
8. the delivery and confound audit;
9. structural versus behavioral notes, null-behavior scripts and any manipulation checks;
10. invariants and reproducibility;
11. open decisions for the researcher, each with its options, which classes each option would change, a recommendation, and when it must be settled.

Name agents, classes and actions in words (Planner agent, accidental, may end the episode), not invented codes. No sentence or table cell states as fact a property the design leaves open: write `UNSPECIFIED`, or label it as a provisional assumption.

Everything in this file is design logic or recommendation. How agents respond to personas, tools, topologies or memory in a given study is an empirical question for that study, not an input to its protocol. For documented hazards and pointers to sources, see `agent-hazards.md`.

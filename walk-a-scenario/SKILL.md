---
name: walk-a-scenario
description: Read before judging whether a surface actually works. Runs an analytic walkthrough of one scenario from docs/scenarios.md against the real code — traces the path, costs it in decisions and navigations, scores six dimensions, and returns ranked fixes. Use this whenever a scenario is named (S1–S48), whenever the question is whether something is clunky, confusing, slow, expensive or missing, whenever a surface is being evaluated without usage data, and whenever a change needs checking against a scenario. The scenario set tests only whether an answer *exists*; this is what tests what the answer *costs*.
---

# Walking a scenario

`docs/scenarios.md` is a floor, not a gradient. Every one of S1–S48 can have an
answer while the app is exhausting to use, because "has an answer" and "costs
what it should" are different questions and only the first is written down.

This is the second question. It is analytic — no users, no logging, no
instrumentation — because there is one user, he is building the tool, and by the
time enough usage has accumulated to measure, he has adapted to the friction and
can no longer see it. Analytic inspection is the method that does not depend on
that adaptation not having happened yet.

Two bodies of prior art, each contributing one half. **Cognitive Walkthrough**
(Polson, Lewis, Rieman & Wharton, 1992) supplies the step discipline. **KLM /
GOMS** (Card, Moran & Newell, 1983) supplies the costing. Take only the step
discipline from CW: its four questions are about *learnability by a novice* —
will they notice the control, will they associate it with their goal — and the
sole user of this system is its author. Those two questions pass trivially here
and tell you nothing. KLM is the half that fits, because it models expert
performance with no learning at all.

Four steps, then the exits. Do them in order; the trace has to exist before
anything can be scored against it.

**The verdicts have to be reproducible.** Two people walking the same scenario
against the same code should reach the same six verdicts; where they cannot, the
dimension is underdefined and that is a defect in this file rather than a matter
of taste. The definitions below are written tightly for that reason, and the
first time a walkthrough has to *choose* a reading, the reading it chose belongs
in the report so the next one can be consistent with it.

## 1. Fix the scenario and its budget

Run `scripts/scenario.py Sn` to pull the scenario block, its *Must work* and
*Guards* clauses, and every surface the coverage table assigns to it. Read what
it prints rather than working from memory of the scenario.

The **budget** is the constraint the scenario states in its own first line —
"phone, eight seconds", "one hand, kitchen", "one minute, half attention",
"Sunday, twenty unfiled things". That is the pass line for cost, and it is why
this method needs no usage data: the scenario already declared what the path is
allowed to cost.

Not every scenario has one. Sections A, B and F state budgets; E and I largely
do not. **A missing budget is a finding about the scenario, not a reason to
invent a default.** Record Cost as `unscoreable`, keep walking, and emit a
scenario amendment (exit 2). Inventing a budget makes the dimension look scored
when nothing was measured, which is worse than the gap.

## 2. Trace the real path

Read the code. Docstrings in this repo *argue* — they are worth reading and they
are claims about intent, not evidence of behaviour, and `domain.md` and
`scenarios.md` both say plainly that a claim there may be unmet. So the trace
comes from components and routers, and a doc that disagrees with them is itself
a finding.

Where to start, in the order that usually works:

| looking for | start at |
|---|---|
| which objects the scenario touches | `web/src/services/api/registry.ts` |
| the surface you land on | `web/src/pages/`, `web/src/router/routes.tsx` |
| the fields and actions on a record | `web/src/entities/<obj>/Detail.tsx` |
| what an action actually writes | `api/src/wild_life/routers/<obj>.py` |
| what the shape permits | `api/src/wild_life/models/<obj>.py` |
| whether a failure ever surfaces | `api/src/wild_life/routers/reviews.py` |

That last row earns its place. Most scenarios in sections D, E and I have a
*must work* clause about something becoming **visible** — staleness, neglect, a
scope unexamined, a job that stopped. Visibility is almost always the review
dashboard, and a surface can execute its whole happy path correctly while the
condition the scenario cares about is detected nowhere. Check it explicitly; it
is the failure this method finds most often and the one no amount of reading the
front end will reveal.

**Step 0 is a question, not a section.** Ask whether the path begins with a
choice the scenario does not decide — two mechanisms that both plausibly serve
it. When there is one it is usually the most expensive decision in the trace and
the most important finding. When there is not, say nothing and start at step 1.
Most scenarios have no step-0 fork, and the first draft of this skill produced
one in three walkthroughs out of three, which is the rate to be suspicious of. A
finding that is not a fork — a wrong count, a dead link — is an ordinary step or
a score, and filing it under Step 0 because the heading is there costs the
heading its meaning.

Write the trace as numbered steps. Each step records four things:

1. what you intend at that moment
2. the gesture
3. what the system does
4. **what you must decide** — the currency, see step 3

Per step, three questions. They come from guards this repo has already written,
which is why they find its failures where Nielsen's ten heuristics would not:

- **Is the next action available where you already are**, or does it require
  navigating first? (S26 guards a logging path that requires finding the
  schedule first.)
- **Does the system ask for anything the gesture already carried?**
  (`web/docs/ui-architecture.md` → *Creation is capture*, rule 1; S32.)
- **Is the result visible where you are**, without a tick or a navigation? (S3
  guards the lag that made writing feel unrecorded; S10 guards orphans created
  by a modal that navigated away.)

**When two surfaces answer the same question differently, that is a finding, not
a tie to break.** It usually means one concept has grown two implementations,
which lands in exit 3.

## 3. Cost the path

Count **decisions and navigations**, not keystrokes. In KLM the mental operator
M (~1.35s) dominates a path of this granularity, and the keystrokes of typed
content are the payload rather than overhead — a scenario that asks you to write
a paragraph is not expensive because the paragraph is long.

| operator | ~cost | count it when |
|---|---|---|
| **M** — mental preparation | 1.35s | a decision the user cannot have made in advance |
| **P** — point | 1.1s | a targeted click or tap |
| **K** — keystroke | 0.2s | chrome only, never the content being written |
| **H** — home | 0.4s | hand moves between input devices |
| **N** — navigation | ~1s + R | a route change, which is an M and a wait together |
| **R** — response | measure | anything the user waits on |

**Report one headline figure with its arithmetic**, so the number can be argued
with and re-derived later:

```
Cost: 2 decisions, 1 navigation, 1 point ≈ 2×1.35 + 1.0 + 1.1 = 4.8 s
      Budget: "Kitchen, kids, phone in one hand" → over on device, not on count
```

A step-0 decision counts as an M before the first gesture. **Produce the figure
even when the scenario states no budget** — the count is still a fact worth
having and comparable across walkthroughs; it is only the *verdict* that is
unscoreable, not the measurement. A walk that reports no number has not run this
step, and replacing "feels heavy" with a number is the whole reason the method
exists.

Where a path has more than one route — the ordinary case and the deviation, say
— cost each separately. An average across them describes a path nobody walks.

## 4. Score the six dimensions

Four are Green & Petre's **Cognitive Dimensions of Notations**, which is the
framework built to evaluate a notation without users. Two are ours, because the
frontier claims this system makes — more signal than a planning app, more agency
than a wiki — are not in anyone's standard rubric and fail in ways the standard
dimensions cannot see.

| dimension | the question | fails when |
|---|---|---|
| **Cost** | decisions + navigations vs. the stated budget | over budget |
| **Premature commitment** | is a choice demanded before the information to make it exists? | any required input the moment cannot answer. A **choice of mechanism** counts *only when the fact that decides it is not yet available* — two paths recording different things, forked before you can know which you need. If you do know and simply cannot revise the choice afterwards, that is **viscosity**, and filing it here inflates this dimension while hiding the real defect |
| **Viscosity** | what does changing or undoing something already recorded cost? | revision costs more than re-entry, undo is unavailable or lossy, or an edit rewrites history |
| **Hidden dependency** | from the act, what it affected; from the affected thing, what caused it | either direction is dead |
| **Legibility under accretion** | read the surface at 100× today's row count | works only while sparse |
| **Attribution** | when a second actor writes, does its work say so? | a machine's write is indistinguishable from yours |

Two of these were one dimension in the first draft and were split because two
walkthroughs of S26 scored the weld differently — one read it as attribution
(`fails`), the other as reversibility with no machine actor present
(`not exercised`), and both readings were fair. **Undo cost is viscosity**:
resistance to change is Green & Petre's own definition, so it belongs there
rather than beside a dimension that only applies when something else is writing.
Attribution stands alone and is `not exercised` on most scenarios, which is a
real verdict and not a gap.

**The boundary between `degrades` and `fails` is the same one the whole method
turns on: can the person do the thing, or not.**

- `fails` — under this dimension, the thing cannot be done. No route exists, or
  the only route is one the scenario forbids.
- `degrades` — it can be done, worse than it should be.
- `holds` — it can be done at the cost it should cost.

Two runs of S26 split on exactly this and produced `fails` and `degrades` from
identical facts, twice. Worked: *can a recorded dose's amount be corrected?*
Nowhere, on any surface → `fails`, not `degrades`. *Can you get from the dose
moment to its amount?* No → the direction is dead, and an unrelated route
reaching the same medication does not revive it, because the dependency the act
created is the one that has to be traversable **from the artifact the act
produced**.

`not exercised` is about the **surface**, not about who happened to walk it: use
it when the scenario names no second actor *and* the surface could carry one;
use `fails` when the surface could not carry one at all. A walkthrough found this
gap and resolved it this way, and it is right — a dimension that reports "not
applicable" for a surface that structurally cannot answer it hides the finding.

Verdicts are `holds` / `degrades` / `fails` / `not exercised` / `unscoreable`.
Three live values rather than pass-fail, mirroring S18's three answers, because
the honest outcome is often "worse than it should be" or "can't tell without the
row count" and collapsing those into a failure produces a rubric nobody trusts.
`not exercised` is a real verdict — most scenarios have no machine actor.

Two dimensions carry the frontier claims and deserve deliberate attention rather
than a glance:

**Legibility under accretion** is the only line that catches a surface which
works today and fails at a row count that does not exist yet. Grouping, sorting
and empty states are where it bites. Ask what this screen looks like with fifty
rows, not five.

**Viscosity** is where a life-management system rots specifically. A journal is
append-only and never gets viscous; this system holds standing objects that
change — a protocol's dose, an intention's window, two people who turn out to be
one. S29's guard, "a schedule edit that retroactively alters history", is a
viscosity failure written before the word was available.

## Separate what is impossible from what is expensive

The finding worth most is a **cannot** — something a person cannot do at all on
this path today — and it is easily lost, because the six dimensions are all
scales and a scale absorbs an absolute. Say it in its own line, before the
scores.

The first draft of this skill lost one exactly this way. S26's only control for
recording a dose different from the prescribed one is `opacity-0
group-hover:opacity-100`, and the scenario names a phone. There is no hover on a
phone, so the walkthrough scored it **Cost · degrades** when the honest finding
is that on the stated device the thing cannot be done by sight at all. A cost
score reads as "make this nicer"; a cannot reads as "this does not work", and
they rank nowhere near each other.

The test is not whether an affordance exists in the DOM but whether a person
under the scenario's stated constraints can reach it. Hover on touch, a control
behind a route the scenario forbids, an endpoint with no caller, a field editable
from nowhere — all of these are absences wearing the costume of a cost.

**A `degrades` or `fails` verdict that is really a cannot must say so**, and the
cannot outranks everything else in the fix list, because making a surface cheaper
where it does not work is not an improvement.

## The exits

A walkthrough that ends in prose is a walkthrough nobody rereads, and
`AGENTS.md` is explicit that a failing check beats a written instruction. Every
finding leaves through exactly one of three doors.

| exit | when | lands as |
|---|---|---|
| **1 · a counted check** | the path works but costs too much, or a condition is undetected | a test asserting the count or the detection — for an undetected condition the check *is* the feature. **Name the assertion in one sentence.** A fix with no assertion is an ordinary bug ticket wearing an exit tag, and it will be forgotten in the same way the prose it replaced was |
| **2 · a scenario amendment** | walking it showed the scenario underspecified — most often a missing budget | an edit to `docs/scenarios.md`, written before the fix |
| **3 · a concept defect** | the friction traces to two concepts serving one purpose, or one serving two | a `model-the-domain` question, not a UI fix |

Exit 3 is the one to watch for and the one most easily misfiled as three
unrelated UI problems. The vocabulary is Daniel Jackson's *The Essence of
Software* (2021): **redundancy** is two concepts sharing one purpose,
**overloading** is one concept serving two, and both present as interface
friction while being untouchable from the interface. `api/docs/domain.md` →
*What the domain has not decided* already diagnoses several without the words for
them. Three awkward steps in three scenarios all touching cadence are not three
findings; they are `tasks.recurrence` and `rules`.

**The report itself does not land anywhere.** It is a claim about the code at one
moment and it starts rotting immediately, which is the failure mode `domain.md`
was rebuilt to escape. Only the three exits are durable. Do not create a
`docs/walkthroughs/` directory.

## Ranking the fixes

Order them by what would be wasted work if done in the wrong order:

0. **A cannot** — something that cannot be done at all under the scenario's
   stated constraints. This is the only class where the fix changes what the app
   *can* do rather than what it costs, and it is the measure the whole method is
   ultimately judged by: a walkthrough earns its keep when it finds a place the
   app is unusable and the fix makes it usable.
1. **`fails` on a *must work* clause** — the scenario is not answered, which is
   the one thing the scenario set exists to assert.
2. **Concept defects (exit 3)** — before any interface fix they would invalidate.
   Polishing one of two redundant surfaces is work undone by deciding which
   survives. Row counts matter here: a defect no data uses yet is the cheapest it
   will ever be, and `domain.md` already makes this argument about
   `TaskStatus`'s unused `delegated`/`delivered`.
3. **`fails` on a dimension** without a *must work* clause behind it.
4. **`degrades`** — record, act only if cheap or adjacent to something above.

Give each fix its exit, its dimension, and an honest size. A fix whose size you
cannot estimate without more tracing should say so rather than guess.

## Counts that change a ranking

Row counts from the live database are the strongest evidence available here —
"4 rows use this" and "1,278 rows use this" rank the same defect differently. So
when a count decides an ordering, **give the query beside it**, because a number
nobody can re-run ages into a claim nobody can check. Counts that merely colour a
description need no such ceremony.

## Output format

```markdown
# Sn · <title> — walkthrough

**Budget:** <the scenario's stated constraint, or "none stated">
**Cost:** <the headline figure and its arithmetic; report it even when unscoreable>
**Traced:** <files read, so the reader can check the claim>

## Step 0
<only when the path opens on a fork the scenario does not decide; omit otherwise>

## The trace
<numbered steps; per step: intend / gesture / system / decide>

## Scores
| dimension | verdict | basis |

## Must work
<each clause of the scenario's *must work*, answered yes or no, with the evidence>

## Recommended fixes
| # | fix | exit | dimension | size |

## What this walkthrough did not cover
```

The *Must work* section is not optional and is not the same as the scores. The
scenario states its own acceptance criteria; a walkthrough that scores six
dimensions and never answers them has evaluated something other than what was
asked.

## What this method is blind to

It finds structural friction — a step that should not exist, a question already
answered, a dependency with no route back. It does not find felt friction: the
path that is defensible on paper and grating in the hand, usually a rhythm or a
latency problem rather than a step-count one. That is a limit of analytic
inspection generally, not of this rubric. Say so in the report rather than
letting the silence read as coverage.

## A worked example

`references/s21-walkthrough.md` is a complete run against S21 (delegation that
stalls, then declines) from 2026-08-16. Read it when the shape of a step-0
finding or the depth expected in a trace is unclear. It is also the case where
all three exits appeared at once, which is the normal outcome rather than a
remarkable one.

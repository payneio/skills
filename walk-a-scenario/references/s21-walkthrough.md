# S21 · Delegation that stalls, then declines — walkthrough

Run on 2026-08-16. Kept as the worked example because all three exits appeared at
once, which is the normal outcome rather than a remarkable one, and because the
finding that mattered was at step 0 — before any gesture.

Read it for the shape, not the verdicts. The code will have moved.

**Budget:** none stated — section E scenarios carry no constraints, so the Cost
*verdict* is unscoreable here (exit 2 below).
**Cost:** route A 3 decisions, 3 navigations ≈ 3×1.35 + 3×1.0 = 7.1 s to reach and
offer the task; route B 2 decisions, 1 navigation. Measured, not scored.
**Traced:** `web/src/components/AssignmentBar.tsx`,
`web/src/components/OutcomeTasks.tsx`, `web/src/entities/outcome/Detail.tsx`,
`api/src/wild_life/routers/tasks.py`, `api/src/wild_life/routers/reviews.py`,
`api/src/wild_life/models/tasks.py`.

**Superseded 2026-08-20.** The delegation tables this walkthrough read are gone;
what is owed between parties is a docket entry now. The finding still stands and
the paths no longer do.

## Step 0

The walkthrough does not survive its first step. Before any gesture the scenario
requires a choice it has no way to make, because there are two complete and
unconnected implementations of handing work to someone:

| | Task assignment | Delegation |
|---|---|---|
| surface | `AssignmentBar` on the task detail | `/delegations` list + `DelegationDetail` |
| moves | four buttons — offer / accept / decline / withdraw | one 12-value `status` select |
| API | `POST /tasks/{id}/assignment` | `PATCH /delegations/{id}` |
| history | an `exchange` moment per move | none; `status` overwrites |
| what it moves | `responsible_id` only, explicitly never Accountable | `responsible_id` and `accountable_owner_id`, no invariant |
| link to the commitment | it *is* the task | soft `entity_type`/`entity_id` |

Plus a third fragment: `TaskStatus` still carries `delegated`/`delivered`
(`models/tasks.py:35`).

The two surfaces give **opposite answers to the same question, and both wrote
down their reasoning**. `AssignmentBar`'s docstring: *"The four moves are
deliberately not a status dropdown… A control that offered 'declined' among a
task's statuses would say the opposite."* `DelegationDetail` renders exactly that
dropdown, with `declined` in it. Two surfaces disagreeing is a finding, not a tie
to break — see exit 3.

## The trace

### Route A — task assignment

1. **Reach the draft task.** From the outcome, `OutcomeTasks` lists what serves it
   and links through, so S15's both-directions holds for *reading*. Writing is
   one-way: the empty state says "Tasks name what they are for from their own
   page", so creating the task and pointing it at the outcome means leaving the
   outcome, creating in `/tasks`, opening it, setting the objective, returning.
   *3 navigations, 2 decisions.*
2. **Offer it.** `AssignmentBar` → Offer → combobox → person.
   *1 decision (who), 3 gestures.* Cheap, and asks nothing the gesture already
   carried.
3. **Three weeks pass.** Nothing surfaces it. The only detector that would catch
   a task going quiet is `untouched_tasks`, whose test is
   `Task.updated_at == Task.created_at` (`routers/reviews.py:164`) — "literally
   nothing has happened to the row". Offering sets `responsible_id`, which bumps
   `updated_at`. **Offering a task removes it from the only staleness detector
   that could have surfaced it.** Nothing keys on responsible-set-plus-silence;
   the `exchange` moments are written and nothing reads their age.
4. **They decline.** `AssignmentBar` → Declined → `responsible_id = None`, an
   `exchange` moment on the task's Log, commitment untouched, the bar reading
   "yours, unoffered". *1 gesture.* The axiom holds.

### Route B — delegation record

1. **Create.** QuickCreate takes outcome text plus a person and opens the row,
   matching the declared rule in `ui-architecture.md` (Delegation → open).
2. **Every subsequent move** is the 12-value status select.
3. **Three weeks pass.** `delegation_followups` fires on
   `follow_up_date <= today`, so silence is visible only if you remembered to set
   a date. Staleness here is **declared, not detected**. `last_contact_date` is
   stored and displayed and nothing computes from it — while `stale_projects`
   twenty lines away does the detected version
   (`last_activity_date < stale_before`). The pattern exists in the file;
   delegations do not use it.
4. **Reaching the commitment.** `entity_type`/`entity_id` are writable —
   `<F.Root />`, filed under a section titled **"Progress"**, between "Latest
   update" and "Completion evidence" — but the outcome's page renders only
   `OutcomeTasks`. From "the paper is published", who is drafting it is invisible.

## Scores

| dimension | verdict | basis |
|---|---|---|
| **Cost** | unscoreable | S21 states no budget |
| **Premature commitment** | fails | the route is chosen at capture, before acceptance or deliverable-review is known; route B then demands 1 of 12 statuses when only "offered" is true |
| **Viscosity** | fails | nothing converts between the two mechanisms; choosing wrong means re-entry, and the exchange history does not follow. Undo of a wrong route is re-entry, not reversal |
| **Hidden dependency** | degrades | task↔outcome both live; outcome→delegation dead; delegation→root writable but unrendered on the root and filed under "Progress" |
| **Legibility under accretion** | degrades | eight open-status groups to scan; fine at today's counts |
| **Attribution** | not exercised | S21 names no second actor, **and** the surface could carry one — `exchange` moments are written through a path that sets `actor_token_id`. Had the surface been unable to carry an actor at all, this would be `fails` |

## Must work

| clause | answer |
|---|---|
| offer, accept, decline, withdraw as moves on the *assignment* | **yes** on route A — four moves, own endpoint, own history. **No** on route B — a status dropdown |
| the commitment stays yours throughout | **yes**, both routes, by different means |
| three weeks of nothing visible as staleness | **no**, both routes — route A erases the signal, route B never looks for it |
| "they said no" never reads as "it is over" | **yes** on route A. On route B the value sits in a vocabulary that also holds `cancelled` |

## Recommended fixes

| # | fix | exit | dimension | size |
|---|---|---|---|---|
| 1 | Detect assignment silence: a dashboard row for a task with `responsible_id` set and no `exchange` moment in N days. The check *is* the feature — no such row exists | 1 | must work | small |
| 2 | Detect delegation silence from `last_contact_date`, as `stale_projects` already does, rather than waiting on a declared `follow_up_date`. Assert: an open delegation whose `last_contact_date` is older than the stale window appears in the dashboard even with no `follow_up_date` set | 1 | must work | small |
| 3 | Decide whether delegation and task-assignment are one concept. Jackson redundancy; `domain.md` already files this as *What is a request, and is it one concept or several?* and names S21 as its test. **Before 4 and 5**, which either surface's polish would waste | 3 | premature commitment, viscosity | a decision, then a migration |
| 4 | Give section E scenarios budgets, so Cost is scoreable across S21–S25 | 2 | cost | writing |
| 5 | Render the delegation on its root's page, and move `<F.Root />` out of "Progress". Assert: a delegation whose root is an outcome is reachable from that outcome's detail | 1 | hidden dependency | small |

Note on ordering: 3 outranks 5 even though 5 is a quarter of the work, because
polishing one of two redundant surfaces is undone by deciding which survives.
`TaskStatus`'s `delegated`/`delivered` have no rows using them, which is the
cheapest that defect will ever be.

## What this walkthrough did not cover

Route A was traced from an outcome that already had its task. Creating the
commitment itself, and S22's other direction — being asked — were out of scope.
No felt friction: everything here is structural, read from code rather than from
use.

Aside, found in passing: `_TASK_OPEN = ("completed", "cancelled")`
(`reviews.py:70`) holds the *closed* set. All four uses are `notin_`, so the
logic is right and the name is inverted.

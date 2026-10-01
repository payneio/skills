---
name: pitch-deck
description: >-
  Turn a product idea, vision doc, or rough notes into a compelling investor/exec pitch — both a
  structured pitch document and a self-contained HTML slide deck. Use this WHENEVER someone wants to
  pitch a product, build a pitch deck or slide deck, make an "Amazon one-pager" or press release,
  create a founder/startup/exec pitch, turn a vision or one-pager into slides, prepare a demo-day or
  board presentation, or get feedback that their existing deck "isn't landing." Trigger even when they
  don't say the word "deck" — e.g. "help me present this product to my VP," "make this idea
  investable," "I have a vision doc, now what," or "nobody likes our current pitch." Builds on a proven
  entrepreneurship pitch spine (problem, product, customer, reach, money, team, why-care, why-win) and
  produces a deck that reads as intentional, not templated.
---

# Pitch Deck Builder

Turn a product's *substance* into a persuasive pitch, using a battle-tested *structure*. The output is
two artifacts: a **pitch document** (the thinking-and-alignment tool) and a **self-contained HTML slide
deck** (the presentation). This method has produced decks that consistently draw "sign me up" reactions.

## The one idea that makes this work: two separate sources

A good pitch fuses two things that people usually tangle together:

- **Substance** — what the product actually is, drawn from the user's material (a vision doc, a
  one-pager, notes, or an interview). This is the *only* place facts come from.
- **Structure** — the order and beats a persuasive pitch needs, drawn from `references/pitch-spine.md`.
  This is a fixed checklist, independent of any product.

Keep them separate in your head. Structure tells you *what slots must be filled and in what order*;
substance fills the slots. When substance is missing for a slot, you say so (see **Source fidelity**),
you don't invent it. Most weak pitches fail because someone reached for a nice-sounding structure and
then wrote whatever words filled it — untethered from anything true about the product.

## Workflow

Follow these steps in order. Steps 1–2 are where quality is won or lost; don't rush to slides.

### 1. Gather the substance into one canonical source

You need one trustworthy account of the product. If the user handed you a vision doc, one-pager, PRFAQ,
or notes, that's it — read it fully. If they gave you several documents, or pointed at a codebase and a
transcript, **pick or synthesize a single source of truth** and tell the user which one you're treating
as authoritative. If they gave you almost nothing, interview them briefly — the minimum you need is:
what is it, who is it for, what painful problem does it kill, and why now. Don't start writing until you
can answer those four.

Watch for **context poisoning**: material written for a different audience, an older strategy, or a
lower altitude (implementation details) will drag the pitch down if you let it leak in. If two sources
disagree, surface the conflict to the user instead of silently averaging them.

### 2. Draft the pitch document

Read `references/pitch-spine.md` and write a markdown pitch doc that hits every beat, in order. This
document is not throwaway — it's the alignment tool the team argues over before anyone cares about
fonts. It's also where you do the real thinking; the deck is a compression of it.

Two disciplines govern this draft:

- **Source fidelity.** Every claim traces to the substance from step 1. Where the spine asks for
  something the source doesn't contain — market size, the founder's personal "why," revenue model,
  named team — write a visible **`[needs data]`** marker naming what's missing, rather than fabricating
  a plausible number or backstory. This is not laziness; it's the feature. A pitch that honestly flags
  its three unknowns is far more useful (and more credible) than one that papers over them, and it turns
  the doc into a to-do list for the humans. Fabricated specifics are the fastest way to lose a room.
- **Altitude.** Lead with the general, human-legible story — the problem and the stakes — not the
  machinery. Scope decisions ("we're doing the Azure version first"), sequencing, and implementation
  belong in a **roadmap** or **appendix**, not the vision. A pitch that opens on "a governance and
  deployment layer" has already lost; one that opens on "you built it, now you can't get it live" has
  the room. If you catch yourself explaining *how* it works up top, you're too low — move it down.

Preserve genuine **open questions and tensions** in their own section rather than resolving them
artificially. Decision-makers trust a pitch that knows what it hasn't settled.

### 3. Build the HTML slide deck

Once the doc is right, read `references/deck-craft.md` and compress it into slides. Start from
`assets/deck-template.html` — a self-contained scaffold with keyboard/click navigation, a progress bar,
and layout primitives already wired up. You fill in slides and choose the visual design.

The deck follows the same spine as the doc but is *ruthlessly* compressed: one idea per slide, a headline
that could stand alone, minimal words. It targets a ~7-minute spoken walkthrough. `[needs data]` markers
from the doc carry over as honest visible tags, not silent omissions.

**Design intentionally.** Do *not* reuse a single house style across products. Choose type, color, and
layout that fit *this* product's character, and make deliberate choices rather than accepting defaults —
a deck that looks templated reads as a product that is. `references/deck-craft.md` has the craft
details; if a `frontend-design` skill is available, consult it for aesthetic direction.

### 4. Hand off

Tell the user both artifact paths, and call out the `[needs data]` items explicitly — those are the
highest-leverage things for them to fill next. Offer to open the deck in a browser. If they want it
hosted or served, do that only when they ask (it's environment-specific).

## What "good" looks like

- The **first slide** makes a stranger care in one sentence — a problem or stakes, not a category.
- Every beat of the spine is present and in order; nothing load-bearing is skipped.
- Claims are traceable to the source; unknowns are flagged, not faked.
- The vision reads general and durable; scope/implementation is pushed to a roadmap.
- The deck is a single self-contained `.html` file that opens anywhere, navigates by arrow keys, and
  looks like it was designed for this product specifically.

## Files in this skill

- `references/pitch-spine.md` — the structural checklist: the beats, their order, and *why* each earns
  its place. Read before drafting the doc (step 2).
- `references/deck-craft.md` — turning the doc into slides: compression, slide types, navigation,
  design. Read before building the deck (step 3).
- `assets/deck-template.html` — the reusable, self-contained deck scaffold. Copy and fill.

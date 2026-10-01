# Deck Craft — turning the pitch doc into slides

The doc is the argument; the deck is its compression for a live room. Read this before building slides.
Start from `assets/deck-template.html` (self-contained; nav, progress, and layout primitives already wired).

## The compression rule
A slide is not a paragraph. For each beat of the doc, ask: *what is the single idea a viewer must leave
with?* Put that as a headline that could stand alone if screenshotted, and support it with the fewest
words or the one visual that proves it. If a slide has two ideas, split it. If it has none, cut it.

Target **~7 minutes spoken**, which is roughly 12–18 slides. Err toward fewer, bolder slides.

## Slide sequence (maps to the spine)
A reliable default order — adapt to the product:

1. **Title** — product name + the back-of-the-box promise (one line). Not a category description.
2. **Why listen** — the problem as a punch: the before/after or the stark statement.
3. **The gap / stakes** — make the problem vivid and specific.
4. **Why care** — the three failure modes, or who's hurt and how.
5. **Why now** — the inflection(s).
6. **What is it** — the back-of-the-box block, read aloud.
7. **The product** — the jobs, as cards. Benefits, not features.
8. **The novel mechanism** — the one genuinely new thing.
9. **The customer** — two buyers, what each gets.
10. **Beachhead + market** — where we start; rings outward. Flag if sizing is `[needs data]`.
11. **Reach** — the channel; where their head is.
12. **Money / the ask** — the horizon and the concrete ask.
13. **Why win** — three sources of advantage.
14. **Competition** — "it's been done," rebutted (a compact table).
15. **The emotional close** — why anyone cares.
16. **Aspiration** — the future, one bold line. Optional team slide before it.
17. **(Optional) 7-minute spine** — a speaker's cheat-sheet table of beats + lines.

## Slide types you'll reuse (all in the template's CSS)
- **Statement** — one big serif headline, optional lead line. For hooks, gaps, closes.
- **Two-pole** — "what you have → what you need," an arrow between. For framing the gap.
- **Card grid** — 2–4 cards. For jobs-to-be-done, failure modes, advantages.
- **Labeled rows** — a key column + description. For two-buyers, competition, why-now shifts.
- **Numbered list** — big numerals. For the three advantages.
- **Box / back-of-box** — a bordered callout with a headline and promise. For "what is it."
- **Rings** — stacked bands. For beachhead → expansion market.
- **Finale** — the aspiration/promise, large.

## Navigation & mechanics (already built in the template)
- Arrow keys / space / PageDn to advance; arrows / PageUp back; Home/End to jump; click (right two-thirds
  = next, left third = back).
- A top progress bar and a slide counter.
- The URL hash tracks the slide (`#7`) so a slide is deep-linkable and reload-safe.
- **Self-contained.** Everything inline in one `.html`. The only acceptable external dependency is a web
  font `<link>` — and always give a real system-font fallback so it degrades cleanly offline. No local
  JS/CSS files, no build step, no framework.

## Honest markers
Carry `[needs data]` items from the doc onto the relevant slides as a small, visibly-styled tag (the
template has a `.tag.data` style). Don't silently drop them — a visible gap on the market slide is more
credible than a fabricated number, and it tells the presenter exactly what to go get.

## Design intentionally — do not ship the template's default look
The scaffold ships with neutral placeholder styling so it *runs*, but a deck that looks like the template
reads as a product that phoned it in. For each pitch, make deliberate choices:

- **Character first.** Decide the product's personality in a word or two (e.g. *authoritative/editorial*,
  *warm/human*, *precise/technical*, *playful/bold*) and let type and color follow from it.
- **Type.** Choose a display face with actual character for headlines and a clean face for body. Pair
  them; don't run everything in one system font. Give real fallbacks.
- **Color.** A restrained palette — one confident accent, an ink, a paper — beats a rainbow. Ensure
  contrast is strong enough to read from the back of a room.
- **Layout.** Left-aligned editorial layouts often feel more intentional than everything-centered. Use
  generous whitespace; let big type carry.
- **One system.** Whatever you choose, apply it consistently so the deck reads as one designed object.

If a `frontend-design` skill is available in the session, consult it for aesthetic direction before
committing to type and color — it's built for exactly this judgment.

## Common failure modes to avoid
- **Paragraphs on slides.** If you're reading it verbatim, it's a doc, not a slide.
- **Category-first title.** "An X-and-Y platform" instead of a promise or a stake.
- **Feature lists.** Convert to jobs/benefits.
- **Templated sameness.** Default fonts, default colors, centered everything.
- **Fabricated specifics.** Invented market sizes, fake logos, made-up metrics. Flag instead.
- **Too low, too soon.** Implementation architecture in the first third. Push it to a roadmap slide or cut.

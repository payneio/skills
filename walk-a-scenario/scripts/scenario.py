#!/usr/bin/env python3
"""Pull one scenario out of docs/scenarios.md with everything a walkthrough needs.

Prints the scenario block verbatim, the surfaces the coverage table assigns to
it, and a reading of its budget — the constraint stated in its first line, which
is the pass line for the Cost dimension.

The budget is *reported, never inferred*. A scenario with no stated constraint
prints "none stated", which is a finding about the scenario (exit 2) rather than
an invitation to pick a default.

    scripts/scenario.py S21
    scripts/scenario.py 21 --file /path/to/scenarios.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Section headings carry no scenario, but a block ends at one.
BLOCK_START = re.compile(r"^\*\*(S\d+)\s*·\s*(.+?)\.\*\*(.*)$")
COVERAGE_ROW = re.compile(r"^\|\s*(.+?)\s*\|\s*(S\d.*?)\s*\|\s*$")
# En dash in "S10–S14"; hyphen accepted too, since both get typed.
RANGE = re.compile(r"S(\d+)\s*[–-]\s*S?(\d+)")
SINGLE = re.compile(r"S(\d+)")


def find_repo_default() -> Path:
    """docs/scenarios.md, searched upward from this script then from cwd."""
    for start in (Path(__file__).resolve(), Path.cwd().resolve() / "_"):
        for parent in start.parents:
            candidate = parent / "docs" / "scenarios.md"
            if candidate.is_file():
                return candidate
    raise SystemExit("could not find docs/scenarios.md — pass --file")


def scenario_block(lines: list[str], want: str) -> tuple[str, list[str]]:
    """The block for `want`, from its bold opener to the next scenario or heading."""
    out: list[str] = []
    title = ""
    collecting = False
    for line in lines:
        match = BLOCK_START.match(line)
        if match:
            if collecting:
                break
            if match.group(1) == want:
                collecting = True
                title = match.group(2)
        elif collecting and (line.startswith("## ") or line.startswith("---")):
            break
        if collecting:
            out.append(line.rstrip())
    if not collecting:
        raise SystemExit(f"{want} not found — scenarios run S1 upward")
    while out and not out[-1]:
        out.pop()
    return title, out


def covering_surfaces(lines: list[str], number: int) -> list[str]:
    """Coverage-table surfaces whose scenario list contains this number."""
    found: list[str] = []
    for line in lines:
        match = COVERAGE_ROW.match(line)
        if not match:
            continue
        surface, refs = match.group(1), match.group(2)
        numbers: set[int] = set()
        for lo, hi in RANGE.findall(refs):
            numbers.update(range(int(lo), int(hi) + 1))
        numbers.update(int(n) for n in SINGLE.findall(RANGE.sub("", refs)))
        if number in numbers:
            found.append(surface)
    return found


def read_budget(block: list[str]) -> str:
    """The constraint clause that opens the scenario, if it states one.

    Budgets have a consistent form across the file — a comma-separated list of
    constraints with no verb: "Mid-conversation, phone, eight seconds",
    "Kitchen, kids, phone in one hand", "One minute, half attention". Setup prose
    is a sentence: "You commit that a paper will be published…".

    The test is deliberately **conservative in one direction**. Reporting no
    budget when one exists costs a hand-check; reporting a budget that is really
    a fragment of setup invents a pass line and makes the Cost dimension look
    measured when nothing was. So a clause qualifies only as a list of at least
    two short verbless-looking parts, and anything else reads as none stated.
    Known false negative: S17 states its budget ("A Sunday hour") three sentences
    in, and this will miss it.
    """
    opener: list[str] = []
    for line in block:
        if line.lstrip().startswith("*Must work") or line.lstrip().startswith("*Guards"):
            break
        opener.append(line)
    match = BLOCK_START.match(opener[0]) if opener else None
    tail = " ".join([(match.group(3) if match else "")] + opener[1:]).strip()
    first = tail.split(".")[0].strip()

    parts = [p.strip() for p in first.split(",")]
    if len(parts) >= 2 and all(p and len(p.split()) <= 4 for p in parts):
        return first
    return "none stated"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("scenario", help="e.g. S21 or 21")
    ap.add_argument("--file", type=Path, default=None)
    args = ap.parse_args()

    number = int(re.sub(r"\D", "", args.scenario))
    want = f"S{number}"
    path = args.file or find_repo_default()
    lines = path.read_text(encoding="utf-8").splitlines()

    title, block = scenario_block(lines, want)
    surfaces = covering_surfaces(lines, number)
    budget = read_budget(block)

    print(f"# {want} · {title}")
    print(f"# source: {path}")
    print()
    print("\n".join(block))
    print()
    print(f"BUDGET: {budget}")
    if budget == "none stated":
        print(
            "  -> Cost is unscoreable. Record it as such and emit a scenario\n"
            "     amendment (exit 2). Do not invent a budget."
        )
    print()
    print("SURFACES (coverage table):")
    for surface in surfaces or ["  (none — a scenario with no surface is the backlog)"]:
        print(f"  - {surface}" if surfaces else surface)
    return 0


if __name__ == "__main__":
    sys.exit(main())

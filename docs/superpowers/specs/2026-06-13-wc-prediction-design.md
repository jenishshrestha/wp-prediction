# WC-Prediction — Design Spec

**Date:** 2026-06-13
**Goal:** A Claude Code–driven system that predicts the **exact scoreline** of a FIFA World Cup 2026 fixture, reasoning like a football expert and a scientist over curated data plus live research.

## Overview

There is **no application code**. The repository is a structured knowledge base plus a rigorous methodology that Claude Code executes on demand. When the user names two teams, Claude loads their base profiles, tops up with live web research, applies the methodology, and produces a scoreline prediction with explicit probabilities and reasoning.

**Primary success criterion:** correctly predict the scoreline of fixtures (winner direction is necessary but not sufficient — the exact/most-likely score is the target). Calibration is tracked over the tournament.

## Decisions (from brainstorming)

- **Engine:** LLM reasons over assembled context (no trained ML model).
- **Scope:** single match on demand (the core unit).
- **Data sourcing:** hybrid — curated base files for stable facts + live web research for volatile facts.
- **Interface:** structured prompt + Claude Code (no app, no API setup).
- **Team coverage:** lazy — build a team's base file the first time it appears in a prediction.

## Architecture & File Layout

```
wc-prediction/
├── CLAUDE.md                  # The prediction workflow any session follows
├── methodology.md             # Factor model, expected-goals → scoreline, calibration rules
├── data/
│   ├── teams/<team>.md        # Base profile per team (stable facts), built lazily
│   └── tournament.md          # WC2026 format, groups, venues, schedule
└── predictions/
    └── YYYY-MM-DD-teamA-vs-teamB.md   # Saved predictions → track record
```

### Components

**`CLAUDE.md` — the workflow.** Instructs any session how to run a prediction:
1. Identify the two teams and the fixture (stage, venue, date) from `data/tournament.md`.
2. Load both teams' base files from `data/teams/`. If a file is missing, scaffold it via web research first.
3. Live top-up via web research: injuries, suspensions, latest form/results, probable lineup, venue/weather, betting odds.
4. Apply `methodology.md`.
5. Write the prediction to `predictions/` in the standard output format.

**`methodology.md` — the expert + scientist core.** Defines a transparent factor model and, critically, how factors convert into an **expected-goals estimate per team** and then a **scoreline distribution**.

**`data/teams/<team>.md` — base profiles (stable facts):** key players, manager, tactical identity/formation, Elo + FIFA ranking, squad market value, qualification path, recent major-tournament history. Lightweight; built lazily via web research.

**`data/tournament.md` — tournament reference:** WC2026 format (48 teams, 12 groups), group assignments, venues (with altitude/climate notes), and schedule, so any fixture can be located in context.

**`predictions/` — track record:** each prediction saved with date and teams, enabling calibration review against actual results as the tournament progresses.

## Methodology Detail

The model produces, for each team, an **expected goals (xG-for) estimate** against this specific opponent, then derives a scoreline distribution.

**Step 1 — Factor assessment.** Evaluate seven factors:
1. **Baseline strength** — Elo + FIFA ranking + squad market value (the prior).
2. **Recent form** — last 8–10 matches, recency-weighted, adjusted for opponent quality.
3. **Squad availability** — injuries, suspensions, fatigue/rest days.
4. **Tactical matchup** — how the two styles interact (attack vs. defense, press vs. build-up), not just who is "better."
5. **Head-to-head** — historical record, weighted toward recent meetings.
6. **Match context** — venue, altitude/climate, travel, stage pressure, motivation/stakes.
7. **Market signal** — betting odds as a sanity-check prior against our own estimate.

**Step 2 — Expected goals.** Combine factors into an attacking expected-goals figure for each team (their attack vs. the opponent's defense, adjusted by form, availability, and context). Typical international range ~0.5–3.0.

**Step 3 — Scoreline distribution.** Treat each team's goals as approximately Poisson-distributed around its expected-goals figure; reason over the resulting grid of scorelines to identify the most likely exact score and its near alternatives. Derive Win/Draw/Win probabilities from the same grid (consistent with the scoreline, not estimated separately).

**Calibration discipline:**
- Stay calibrated — group-stage upsets and low-scoring knockout games are common; avoid overconfident scorelines.
- Always show the reasoning chain from factors → expected goals → scoreline.
- Flag the single biggest source of uncertainty.
- The most likely *exact* score is often a low number (1-0, 1-1, 2-1); reflect that reality rather than inflating.

## Output Format

Each prediction (saved to `predictions/YYYY-MM-DD-teamA-vs-teamB.md`):

- **Header** — teams, stage, venue, date.
- **Predicted scoreline** — the single most likely exact score (the headline answer).
- **Alternative scorelines** — 2–3 next-most-likely scores with rough probabilities.
- **Outcome probabilities** — Win / Draw / Win, derived from the scoreline grid.
- **Expected goals** — the xG-for figure used for each team.
- **Key factors** — ranked, driving the call.
- **Confidence + main uncertainty.**
- **Expert narrative** — one tight paragraph.

## Out of Scope (YAGNI)

- No trained statistical/ML model, no app/CLI/web UI, no direct API integration.
- No full-bracket simulation (single match is the unit; can compose later if wanted).
- No exhaustive pre-built profiles for all 48 teams (lazy build only).

## Open Questions

None blocking. Calibration review cadence can be decided once predictions accumulate.

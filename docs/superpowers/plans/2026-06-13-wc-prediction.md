# WC-Prediction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code–driven knowledge base + methodology that predicts the exact scoreline of any FIFA World Cup 2026 fixture.

**Architecture:** No application code. The repo holds (1) a tournament reference, (2) lazily-built per-team base profiles, (3) a rigorous methodology converting factors → expected goals → a Poisson scoreline distribution, and (4) a `CLAUDE.md` workflow Claude executes on demand, saving each prediction for calibration tracking.

**Tech Stack:** Markdown knowledge files only. Live data via Claude Code's web search/fetch at prediction time. No libraries, no API setup.

---

## File Structure

- Create: `data/tournament.md` — WC2026 format, groups, venues (altitude/climate), schedule.
- Create: `methodology.md` — factor model, expected-goals derivation, Poisson scoreline reasoning, calibration rules.
- Create: `CLAUDE.md` — the prediction workflow any session follows.
- Create: `data/teams/_TEMPLATE.md` — base-profile template for lazy team builds.
- Create: `predictions/_TEMPLATE.md` — prediction output template.
- Create (validation): one real team file + one real prediction to prove the workflow end-to-end.

Validation note: there are no unit tests. Each artifact's "test" is producing a concrete, sensible output by following it. The final task runs a full prediction end-to-end.

---

### Task 1: Tournament reference

**Files:**
- Create: `data/tournament.md`

- [ ] **Step 1: Research the WC2026 structure**

Use web search to confirm: 48 teams, 12 groups of 4, host nations (USA/Canada/Mexico), key venues with notable altitude/climate (e.g. Mexico City altitude, summer heat in southern US venues), and the current stage as of the prediction date.

- [ ] **Step 2: Write `data/tournament.md`**

Include these sections:
```markdown
# FIFA World Cup 2026 — Tournament Reference

## Format
48 teams, 12 groups of 4. Top 2 of each group + 8 best third-placed teams advance to a 32-team knockout round.

## Hosts & Venues
| Venue | City | Country | Altitude / Climate notes |
|-------|------|---------|--------------------------|
| ...   | ...  | ...     | ...                      |

## Groups
- Group A: <teams>
- ... (Groups A–L)

## Schedule / Current Stage
<group stage dates, knockout dates; note the current stage as of today>
```

Fill every row/group with researched values — no placeholders.

- [ ] **Step 3: Sanity-check**

Confirm 12 groups are listed, venues include altitude/climate notes, and the format description matches the 48-team structure.

- [ ] **Step 4: Commit**

```bash
git add data/tournament.md
git commit -m "Add WC2026 tournament reference"
```

---

### Task 2: Team base-profile template

**Files:**
- Create: `data/teams/_TEMPLATE.md`

- [ ] **Step 1: Write the template**

```markdown
# <Team> — Base Profile

_Last updated: <YYYY-MM-DD>_

## Identity
- FIFA ranking: <n>
- Elo rating: <n>
- Squad market value: <€n>
- Manager: <name>
- Tactical identity: <formation + style, e.g. 4-3-3 high press>

## Key Players
| Player | Position | Role / notes |
|--------|----------|--------------|
| ...    | ...      | ...          |

## Qualification Path
<how they qualified; notable results>

## Recent Major-Tournament History
<last 2-3 major tournaments: stage reached, style observations>

## Stable Tendencies
<goals-for / goals-against patterns, set-piece strength, defensive solidity>
```

- [ ] **Step 2: Commit**

```bash
git add data/teams/_TEMPLATE.md
git commit -m "Add team base-profile template"
```

---

### Task 3: Methodology — the expert + scientist core

**Files:**
- Create: `methodology.md`

- [ ] **Step 1: Write the factor model section**

```markdown
# Prediction Methodology

The goal is the most likely **exact scoreline**. We reason from factors to an
expected-goals figure per team, then to a scoreline distribution.

## Step 1 — Assess Seven Factors
For each team, assess and note direction + magnitude:
1. Baseline strength — Elo + FIFA ranking + squad market value (the prior).
2. Recent form — last 8–10 matches, recency-weighted, opponent-quality adjusted.
3. Squad availability — injuries, suspensions, fatigue/rest days.
4. Tactical matchup — how the two styles interact (this team's attack vs. that
   team's defense, and vice versa), not just who is "better."
5. Head-to-head — historical record, weighted toward recent meetings.
6. Match context — venue, altitude/climate, travel, stage pressure, motivation.
7. Market signal — betting odds as a sanity-check prior against our estimate.
```

- [ ] **Step 2: Write the expected-goals section**

```markdown
## Step 2 — Expected Goals (xG-for) per team
For each team, estimate goals they will score = (their attack quality) vs.
(opponent's defensive quality), then adjust up/down for form, availability,
tactical matchup, and context. Anchor to realistic international ranges
(~0.5–3.0 goals). State each team's final xG-for figure explicitly.
```

- [ ] **Step 3: Write the scoreline-distribution section**

```markdown
## Step 3 — Scoreline Distribution (Poisson reasoning)
Treat each team's goals as approximately Poisson-distributed around its xG-for.
For each plausible scoreline (0–4 goals per side), the probability ≈
P(home = a | xG_home) × P(away = b | xG_away), where
P(k | λ) = (λ^k · e^−λ) / k!.

Identify:
- The single most likely exact score (headline answer).
- The 2–3 next-most-likely scores.
- Win / Draw / Win probabilities = summed grid probabilities (home>away,
  equal, away>home), so outcomes are consistent with the scoreline grid.
```

- [ ] **Step 4: Write the calibration rules section**

```markdown
## Calibration Discipline
- Stay calibrated: group-stage upsets and low-scoring knockouts are common.
- The most likely exact score is usually low (1-0, 1-1, 2-1); don't inflate.
- Always show the reasoning chain: factors → xG → scoreline.
- Flag the single biggest source of uncertainty.
```

- [ ] **Step 5: Worked sanity-check**

Pick two well-known teams. Following the methodology by hand, derive xG figures
and confirm the Poisson grid yields a sensible low-scoring most-likely score and
Win/Draw/Win probabilities that sum to ~100%. If the math feels off, fix the
methodology wording. (Keep this scratch work out of the committed file.)

- [ ] **Step 6: Commit**

```bash
git add methodology.md
git commit -m "Add prediction methodology (factors to xG to scoreline)"
```

---

### Task 4: Prediction output template

**Files:**
- Create: `predictions/_TEMPLATE.md`

- [ ] **Step 1: Write the template**

```markdown
# <TeamA> vs <TeamB> — <Stage>

_Venue: <venue>, <city> · Date: <YYYY-MM-DD> · Predicted: <YYYY-MM-DD>_

## Predicted Scoreline
**<TeamA> X–Y <TeamB>**

## Alternative Scorelines
1. <score> (~<p>%)
2. <score> (~<p>%)
3. <score> (~<p>%)

## Outcome Probabilities
- <TeamA> win: <p>%  ·  Draw: <p>%  ·  <TeamB> win: <p>%

## Expected Goals
- <TeamA>: <xG>  ·  <TeamB>: <xG>

## Key Factors (ranked)
1. ...
2. ...

## Confidence & Main Uncertainty
<level + the one thing most likely to change the result>

## Expert Narrative
<one tight paragraph>
```

- [ ] **Step 2: Commit**

```bash
git add predictions/_TEMPLATE.md
git commit -m "Add prediction output template"
```

---

### Task 5: The workflow (CLAUDE.md)

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Write the workflow**

```markdown
# WC-Prediction — How to Run a Prediction

When the user names two teams (or a fixture), produce an exact-scoreline prediction.

## Workflow
1. **Locate the fixture.** Use `data/tournament.md` for stage, venue (note
   altitude/climate), and date. If not yet scheduled, ask the user for the stage.
2. **Load base profiles.** Read `data/teams/<team>.md` for both teams. If a file
   is missing, build it from `data/teams/_TEMPLATE.md` via web research, then commit it.
3. **Live top-up (web research).** Gather volatile facts as of today: injuries,
   suspensions, last 8–10 results / form, probable lineup, venue weather,
   current betting odds.
4. **Apply `methodology.md`.** Assess the seven factors → xG-for per team →
   Poisson scoreline grid → most likely score + alternatives + W/D/W.
5. **Write the prediction.** Use `predictions/_TEMPLATE.md`; save to
   `predictions/YYYY-MM-DD-<teamA>-vs-<teamB>.md`. Commit it.

## Rules
- Always show the reasoning chain (factors → xG → scoreline).
- Stay calibrated; favor realistic low scores; flag the biggest uncertainty.
- Cite live sources used for the top-up.
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "Add prediction workflow (CLAUDE.md)"
```

---

### Task 6: End-to-end validation — one real prediction

**Files:**
- Create: `data/teams/<teamA>.md`, `data/teams/<teamB>.md` (built during the run)
- Create: `predictions/YYYY-MM-DD-<teamA>-vs-<teamB>.md`

- [ ] **Step 1: Pick a real upcoming WC2026 fixture**

Use `data/tournament.md` (and web search for the current schedule) to choose an actual upcoming fixture as of today.

- [ ] **Step 2: Run the full `CLAUDE.md` workflow**

Build both teams' base files via research, do the live top-up, apply the methodology, and write the prediction file. This exercises every artifact end-to-end.

- [ ] **Step 3: Verify the output**

Confirm the prediction file has: a single headline exact score, 2–3 alternatives, W/D/W probabilities that sum to ~100%, explicit xG per team, ranked factors, a stated uncertainty, and a narrative. Confirm the reasoning chain (factors → xG → scoreline) is visible.

- [ ] **Step 4: Commit**

```bash
git add data/teams/ predictions/
git commit -m "Add first end-to-end prediction (validation)"
```

---

## Self-Review Notes

- **Spec coverage:** tournament.md (Task 1), team profiles + lazy build (Tasks 2, 5, 6), methodology with xG→scoreline (Task 3), output format (Task 4), workflow (Task 5), saved predictions/track record (Tasks 4, 6). All spec sections covered.
- **Naming consistency:** `xG-for` used throughout; file paths `data/teams/<team>.md`, `predictions/YYYY-MM-DD-<teamA>-vs-<teamB>.md` consistent across tasks.
- **No placeholders:** every artifact step shows the actual content/structure to write.

# WC-Prediction — From-Scratch Data Rebuild (SoFIFA-grounded, 32 R32 teams)

_Design spec · 2026-06-28_

## Context & goal

The repo predicts exact WC2026 scorelines from per-team profiles. The existing
`data/teams/*.md` profiles carry **fabricated unit ratings** that don't match real
SoFIFA (e.g. `argentina.md` says "OVR 86 / ATT 87 / MID 85 / DEF 85"; the real
SoFIFA FC26 scrape is **83 / 86 / 82 / 79**). This session produced verified, real
data — SoFIFA ratings, FIFA ranks, and live squad news — for the full Round-of-32
field while building the Matchday-3 and R32 dossiers.

**Goal:** rebuild the project's data layer from scratch on that verified data, and
codify the proven prediction pipeline, so future predictions are accurate and
repeatable without re-scraping.

## Decisions (from brainstorm)

- **Scope:** full from-scratch reset of the data layer.
- **Teams:** the **32 Round-of-32 teams** (the live field) — all fully grounded in
  this session's verified data; no gaps, no minnow guesswork.
- **Profile depth:** **lean-but-complete, fully-sourced.** Everything the
  methodology consumes (strength, form, availability, tactical), plus a one-line
  "read" only where it's well-established fact. **No invented history/tendencies.**
- **Old files:** **archived, not deleted** (moved to `data/teams/_archive/`).

## Architecture

Ratings live authoritatively **inside each team file** (the `CLAUDE.md` workflow
loads `data/teams/<team>.md`), with a single consolidated `data/sofifa-ratings.md`
as a dated snapshot/index. Both are regenerated together so they cannot drift.

## Deliverables

### 1. `data/sofifa-ratings.md` (new) — snapshot table
Provenance header (SoFIFA FC26, snapshot 24 Jun 2026; FIFA ranks 11 Jun 2026;
scraped via Playwright, Cloudflare-gated; all values parse-checked, no garbage),
then one row per team. **The authoritative numbers:**

| Team | Grp | OVR | ATT | MID | DEF | FIFA |
|------|-----|----:|----:|----:|----:|-----:|
| Argentina | J1 | 83 | 86 | 82 | 79 | 1 |
| France | I1 | 86 | 87 | 85 | 85 | 3 |
| Spain | H1 | 85 | 85 | 86 | 83 | 2 |
| England | L1 | 84 | 84 | 85 | 83 | 4 |
| Portugal | K2 | 84 | 83 | 86 | 83 | 5 |
| Brazil | C1 | 84 | 87 | 82 | 82 | 6 |
| Germany | E1 | 84 | 82 | 84 | 84 | 10 |
| Netherlands | F1 | 82 | 80 | 83 | 83 | 8 |
| Belgium | G1 | 81 | 82 | 82 | 77 | 9 |
| Croatia | L2 | 79 | 78 | 80 | 80 | 11 |
| Morocco | C2 | 79 | 79 | 78 | 79 | 7 |
| Norway | I2 | 79 | 81 | 80 | 75 | 31 |
| Senegal | 3I | 79 | 79 | 80 | 78 | 15 |
| Switzerland | B1 | 78 | 77 | 78 | 76 | 19 |
| Colombia | K1 | 78 | 79 | 78 | 79 | 13 |
| Ivory Coast | E2 | 78 | 79 | 77 | 78 | 33 |
| Austria | J2 | 78 | 76 | 78 | 79 | 24 |
| USA | D1 | 77 | 77 | 79 | 77 | 17 |
| Japan | F2 | 77 | 78 | 78 | 76 | 18 |
| Sweden | 3F | 77 | 84 | 76 | 76 | 38 |
| Mexico | A1 | 76 | 78 | 75 | 75 | 14 |
| Ecuador | 3E | 76 | 76 | 76 | 77 | 23 |
| Algeria | 3J | 76 | 74 | 75 | 77 | 28 |
| Canada | B2 | 75 | 77 | 73 | 75 | 30 |
| Ghana | 3L | 75 | 77 | 74 | 73 | 73 |
| Paraguay | 3D | 75 | 73 | 75 | 76 | 41 |
| Egypt | G2 | 74 | 76 | 74 | 71 | 29 |
| DR Congo | 3K | 74 | 78 | 73 | 74 | 47 |
| Bosnia & Herzegovina | 3B | 73 | 76 | 70 | 75 | 64 |
| Australia | D2 | 71 | 69 | 68 | 71 | 27 |
| South Africa | A2 | 70 | 70 | 69 | 70 | 60 |
| Cape Verde | H2 | 70 | 67 | 69 | 69 | 67 |

### 2. `data/teams/<team>.md` (rebuilt ×32) — lean-plus schema
```
# <Team> — Profile
_SoFIFA FC26 snapshot 24 Jun 2026 · news verified 28 Jun 2026_

## Strength
- SoFIFA: OVR <n> · ATT <n> · MID <n> · DEF <n>
- FIFA ranking: #<n>
- Manager: <name> · Tactical: <formation / style>

## Key players
- <3–5 names, position, one-clause role>

## This tournament
- Route: <group winner / runner-up / best-third>
- Group form: <results>

## Availability
- <confirmed injuries / suspensions, or "none reported">

## Read
- <one line: established tendency and/or well-known history — fact only>
```
Managers for all 32 are captured from this session's research (Scaloni, de la
Fuente, Deschamps, Tuchel, Martínez, Ancelotti, Nagelsmann, Koeman, Garcia, Dalić,
Ouahbi, Solbakken, Thiaw, Yakin, Lorenzo, Fae, Rangnick, Pochettino, Moriyasu,
Potter, Aguirre, Beccacece, Petković, Marsch, Queiroz, Alfaro, Hossam Hassan,
Desabre, Barbarez, Popovic, Broos, Bubista).

### 3. `data/teams/_archive/` (new)
Move the existing 26 `*.md` profiles here unchanged (preserve the prose). Keep
`_TEMPLATE.md` in `data/teams/` (update it to the lean-plus schema).

### 4. `methodology.md` (revised)
Keep the 7-factor → rounded-xG → Poisson-grid core (it already matches practice).
Add: SoFIFA-via-Playwright as the ratings source; the **expert-call (rounded xG)
vs model-mode** framing; **knockout handling** (90-minute headline, level ties go
to ET/penalties, flag coin-flips); and banked lessons — **respect the draw** in
tight asymmetric-motivation games; for pool play, **leverage coin-flips and copy
the locks** (don't fade heavy favourites or overturn a model mode on thin intel).

### 5. `CLAUDE.md` (revised)
Workflow updated to the real pipeline: locate fixture → load profile(s) from
`data/teams/` (ratings cached in `data/sofifa-ratings.md`; re-scrape SoFIFA via
Playwright only when stale) → FIFA-rank cross-check → live top-up (parallel
research agents for multi-match slates) → apply `methodology.md` → output a
self-contained data-driven HTML dossier (summary table + per-match cards: ratings
bars, form, key men, scenario, expert-call score + confidence dots + W/D/W +
Poisson "3 most likely" strip) → optionally score against `predictions/SCOREBOARD.md`.

### 6. `data/tournament.md` (refreshed)
Final standings for all 12 groups + the verified 16-tie R32 bracket (dates,
venues, R16 pairings).

### 7. Kept as-is
`predictions/` (MD3 + R32 HTML dossiers as worked examples), `SCOREBOARD.md`.

## Non-goals
- Not covering eliminated teams or the other 16 WC squads (archived/ignored).
- Not regenerating the prediction dossiers (already built and verified).
- No new app/code — this is a knowledge-file rebuild.

## Risks & notes
- **Staleness:** ratings are a 24 Jun 2026 FC26 snapshot; FIFA ranks 11 Jun. The
  snapshot date is stamped everywhere; re-scrape when it matters.
- **News volatility:** availability lines reflect 28 Jun 2026; flagged as such.
- **Destructive step:** archiving (not deleting) the 26 old files de-risks this;
  nothing is lost.

## Execution order
1. Create `data/teams/_archive/`, move the 26 existing profiles into it.
2. Write `data/sofifa-ratings.md`.
3. Update `data/teams/_TEMPLATE.md` to the lean-plus schema.
4. Write the 32 rebuilt `data/teams/<team>.md` profiles.
5. Revise `methodology.md` and `CLAUDE.md`.
6. Refresh `data/tournament.md`.

# WC-Prediction — How to Run a Prediction

This project predicts the **exact scoreline** of FIFA World Cup 2026 fixtures.
There is no application code — you (Claude) produce predictions by following this
workflow over the project's knowledge files.

When the user names two teams (or a fixture), produce an exact-scoreline prediction.

## Workflow
1. **Locate the fixture.** Use `data/tournament.md` for stage, venue (note
   altitude/climate), date, and the bracket. If the fixture isn't scheduled yet, ask
   the user for the stage.
2. **Load team strength.** Ratings are cached in `data/sofifa-ratings.md` and in each
   `data/teams/<team>.md`. If a team's profile is missing, build it from
   `data/teams/_TEMPLATE.md`. Ratings come from **SoFIFA** (EA FC) — it is
   Cloudflare-gated, so a plain WebFetch 403s; re-scrape only when the snapshot is
   stale, using the Playwright **browser** (`browser_navigate` + `browser_evaluate`
   on `sofifa.com/teams?type=national`), and delete any `.playwright-mcp/` folder
   afterward so it isn't committed.
3. **Cross-check** relative strength against the current FIFA world ranking.
4. **Live top-up (web research).** Injuries, suspensions, last 8–10 form, probable
   XI, venue weather, betting odds — as of today. For a multi-match slate, fan out
   **parallel research agents** (one per cluster of ties) and synthesise.
5. **Predict by judgment (the working method — no formula).** From the ratings +
   live news, estimate each team's expected goals by feel: start from the
   ratings/quality gap, then adjust for form, availability, tactical matchup, venue
   and motivation. From that, produce:
   - **Expert call** — the single most representative scoreline (a clear favourite's
     edge shows in the *margin*; genuinely tight games stay low).
   - **3 most likely** — a short list of plausible exact scores with rough,
     Poisson-shaped probabilities (calibrated estimates, not computed).
   - **W/D/W** — estimated home-win / draw / away-win odds.
   - **Confidence** — Low / Med / High by how separable the sides are.
   Knockouts: headline the 90-minute score; level ties go to extra time / penalties.
6. **Write the output.**
   - Single fixture → markdown via `predictions/_TEMPLATE.md`, saved to
     `predictions/YYYY-MM-DD-<teamA>-vs-<teamB>.md`.
   - A slate/round → a self-contained, data-driven **HTML dossier** (summary table +
     per-match cards: ratings bars, form, key men, scenario, expert-call score +
     confidence dots + W/D/W + Poisson "3 most likely" strip + bracket path). Use the
     `artifact-design` skill. See `predictions/2026-r32-knockouts.html` as the model.
   - When tracking a pool, score results against `predictions/SCOREBOARD.md`.

## Rules
- Show the reasoning chain: **ratings + live news → expected goals → scoreline**.
- Stay calibrated; favour realistic low scores. **Respect the draw only when the
  W/D/W is genuinely level — once it leans to a side, let the headline follow that
  favourite** (a narrow win, not a reflexive draw). Flag the biggest uncertainty.
- Keep the **expert call** (headline) and the **"3 most likely"** alternatives
  distinct — they legitimately differ (the single most likely *score* is often a
  tight draw even when a *win* is the most likely *outcome*).
- The W/D/W and "3 most likely" are **judgment estimates, not computed** — present
  them as such; never dress an estimate as precise model output.
- Build the xG prior from **actual group goals-for/against, not just SoFIFA ratings**
  — favourites get over-credited against stubborn or low-event defences.
- Cite live sources. Note and fix any data corrections (parse-garbage ratings, stale
  standings/records). Ratings/news carry snapshot dates — state them; re-verify stale data.

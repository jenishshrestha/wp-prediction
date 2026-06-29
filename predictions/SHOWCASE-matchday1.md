# How I Used Claude to Build a World Cup Prediction System 🏆

A real walkthrough of what Claude and I built for the WC2026 group stage —
no app, just Claude reasoning over data + a bit of math.

## What we built
1. **A knowledge base** — tournament data, team profiles built on demand via web research.
2. **A methodology** — seven factors (form, injuries, tactics, venue, market odds…) →
   an expected-goals figure per team → a Poisson scoreline distribution.
3. **An expected-points optimizer** — once I told Claude my pool's scoring rules
   (exact +10, goal difference +6, outcome +4, etc.), it computed the
   *highest-scoring* prediction for all 72 group matches, not just the most likely score.

## The big insight Claude found
Under my pool's scoring, **chasing exact scores is a trap.** Goal difference (+6)
and outcome (+4) together = +10, the same as an exact score, but *far* easier to hit.
So the optimal play is:
- **Favorite → 1–0** (banks the win-by-1 margin + clean-sheet bonus)
- **Even game → 1–1** (scoops +10 on *any* draw)
- **Big mismatch → 2–0**
- **2–1 is never optimal** — always prefer 1–0.

## Matchday 1 — how the calls actually did

| Match | Our read | Result | Points |
|---|---|---|---|
| Brazil–Morocco | 1–0, but **1–1 draw flagged "very live"** → played 1–1 | **1–1** | **+25** ✅ |
| Haiti–Scotland | Scotland to win, low-scoring | 0–1 | +7 |
| Qatar–Switzerland | Switzerland favored — but draws lurk | 1–1 | +2 |

The Brazil call is the headline: Claude flagged that Morocco — strikerless and
depleted — would still **sit deep and nick a goal**, making a 1–1 draw the live
alternative. It finished exactly 1–1. **+25 points.**

## The honest part
Exact scorelines are genuinely hard — even a great model nails the precise score
only ~11% of the time, and a couple of our higher picks (0–2s) got clipped by
1–1 draws. Claude was upfront about that ceiling the whole way, which is *why*
the strategy works: it optimizes for points, not for looking clever.

---

*Built entirely in a conversation with Claude. Want the same for your card?
Just tell it your teams and your pool's scoring rules.*

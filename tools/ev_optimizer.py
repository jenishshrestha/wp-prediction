#!/usr/bin/env python3
"""Expected-points optimizer for the WC-prediction pool.

Scoring (additive, per match), prediction (ph,pa) vs actual (ah,aa):
  exact      +10  ph==ah and pa==aa
  goal diff  +6   (ph-pa)==(ah-aa)
  outcome    +4   sign(ph-pa)==sign(ah-aa)   (draw vs draw etc.)
  one team   +3   ph==ah or pa==aa
  total      +2   (ph+pa)==(ah+aa)
  reverse    +1   ph==aa and pa==ah and not exact
Perfect prediction = 10+6+4+3+2 = 25.

For each match we model each team's goals as Poisson(lambda), build the joint
score distribution, and pick the prediction (0..6 each side) that MAXIMISES
expected points over that distribution.
"""
import math

MAXG = 10  # support for the actual-score distribution

def pois(k, lam):
    return math.exp(-lam) * lam**k / math.factorial(k)

def score(ph, pa, ah, aa):
    pts = 0
    if ph == ah and pa == aa:
        pts += 10
    if (ph - pa) == (ah - aa):
        pts += 6
    # outcome
    sp = (ph > pa) - (ph < pa)
    sa = (ah > aa) - (ah < aa)
    if sp == sa:
        pts += 4
    if ph == ah or pa == aa:
        pts += 3
    if (ph + pa) == (ah + aa):
        pts += 2
    if ph == aa and pa == ah and not (ph == ah and pa == aa):
        pts += 1
    return pts

def best_prediction(lh, la):
    # joint distribution of actual scores
    ph_dist = [pois(k, lh) for k in range(MAXG + 1)]
    pa_dist = [pois(k, la) for k in range(MAXG + 1)]
    best = None
    for ph in range(7):
        for pa in range(7):
            ev = 0.0
            for ah in range(MAXG + 1):
                pah = ph_dist[ah]
                if pah < 1e-9:
                    continue
                for aa in range(MAXG + 1):
                    paa = pa_dist[aa]
                    if paa < 1e-9:
                        continue
                    ev += pah * paa * score(ph, pa, ah, aa)
            if best is None or ev > best[0]:
                best = (ev, ph, pa)
    return best  # (ev, ph, pa)

# ---- team strength ratings (overall, ~1-10), rough but defensible (June 2026) ----
STRENGTH = {
    # Group A
    "Mexico": 6.6, "South Africa": 4.5, "South Korea": 6.0, "Czechia": 5.5,
    # Group B
    "Canada": 5.7, "Bosnia and Herzegovina": 5.0, "Qatar": 4.0, "Switzerland": 6.6,
    # Group C
    "Brazil": 8.5, "Morocco": 7.0, "Haiti": 3.0, "Scotland": 5.5,
    # Group D
    "United States": 6.6, "Paraguay": 5.0, "Australia": 5.5, "Turkiye": 6.5,
    # Group E
    "Germany": 8.0, "Curacao": 2.5, "Ivory Coast": 6.0, "Ecuador": 6.0,
    # Group F
    "Netherlands": 8.0, "Japan": 6.6, "Sweden": 5.5, "Tunisia": 5.0,
    # Group G
    "Belgium": 7.5, "Egypt": 5.5, "Iran": 5.5, "New Zealand": 3.5,
    # Group H
    "Spain": 9.0, "Cape Verde": 3.5, "Saudi Arabia": 4.5, "Uruguay": 7.0,
    # Group I
    "France": 9.0, "Senegal": 7.0, "Iraq": 4.0, "Norway": 6.5,
    # Group J
    "Argentina": 9.0, "Algeria": 5.5, "Austria": 6.0, "Jordan": 4.0,
    # Group K
    "Portugal": 8.0, "DR Congo": 5.0, "Uzbekistan": 4.5, "Colombia": 7.0,
    # Group L
    "England": 8.5, "Croatia": 7.0, "Ghana": 5.5, "Panama": 4.0,
}

GROUPS = {
    "A": ["Mexico", "South Africa", "South Korea", "Czechia"],
    "B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["United States", "Paraguay", "Australia", "Turkiye"],
    "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

def xg_from_gap(s_strong, s_weak):
    g = s_strong - s_weak
    strong = min(2.8, 1.25 + 0.27 * g)
    weak = max(0.35, 1.25 - 0.17 * g)
    return strong, weak

def matchups(teams):
    # all 6 pairings in a group
    out = []
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            out.append((teams[i], teams[j]))
    return out

total_ev = 0.0
n = 0
print(f"{'Group':<6}{'Match':<40}{'xG':<14}{'Pick':<8}{'E[pts]':<7}")
print("-" * 75)
for grp, teams in GROUPS.items():
    for a, b in matchups(teams):
        sa, sb = STRENGTH[a], STRENGTH[b]
        if sa >= sb:
            strong, weak = a, b
            ls, lw = xg_from_gap(sa, sb)
            # orient as a vs b => a is strong
            lh, la = ls, lw
        else:
            ls, lw = xg_from_gap(sb, sa)
            lh, la = lw, ls  # a is weaker
        ev, ph, pa = best_prediction(lh, la)
        total_ev += ev
        n += 1
        label = f"{a} vs {b}"
        print(f"{grp:<6}{label:<40}{f'{lh:.2f}-{la:.2f}':<14}{f'{ph}-{pa}':<8}{ev:<7.2f}")
print("-" * 75)
print(f"Matches: {n}   Total expected points: {total_ev:.1f}   Avg/match: {total_ev/n:.2f}")

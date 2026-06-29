# SoFIFA Ratings — WC2026 Round-of-32 field

_Source: SoFIFA, EA Sports **FC 26**, snapshot **24 Jun 2026** · scraped via Playwright
(sofia.com is Cloudflare-gated; plain fetch 403s). FIFA world ranking: **11 Jun 2026**
update. All four columns parse-checked for every team — no zero/garbage values._

This is the cached, authoritative ratings source for predictions. Re-scrape only
when the snapshot is materially stale. OVR = overall, ATT/MID/DEF = unit ratings.

| Team | Group slot | OVR | ATT | MID | DEF | FIFA rank |
|------|------------|----:|----:|----:|----:|----------:|
| France | I1 | 86 | 87 | 85 | 85 | 3 |
| Spain | H1 | 85 | 85 | 86 | 83 | 2 |
| England | L1 | 84 | 84 | 85 | 83 | 4 |
| Portugal | K2 | 84 | 83 | 86 | 83 | 5 |
| Brazil | C1 | 84 | 87 | 82 | 82 | 6 |
| Germany | E1 | 84 | 82 | 84 | 84 | 10 |
| Argentina | J1 | 83 | 86 | 82 | 79 | 1 |
| Netherlands | F1 | 82 | 80 | 83 | 83 | 8 |
| Belgium | G1 | 81 | 82 | 82 | 77 | 9 |
| Croatia | L2 | 79 | 78 | 80 | 80 | 11 |
| Morocco | C2 | 79 | 79 | 78 | 79 | 7 |
| Norway | I2 | 79 | 81 | 80 | 75 | 31 |
| Senegal | 3rd I | 79 | 79 | 80 | 78 | 15 |
| Switzerland | B1 | 78 | 77 | 78 | 76 | 19 |
| Colombia | K1 | 78 | 79 | 78 | 79 | 13 |
| Ivory Coast | E2 | 78 | 79 | 77 | 78 | 33 |
| Austria | J2 | 78 | 76 | 78 | 79 | 24 |
| USA | D1 | 77 | 77 | 79 | 77 | 17 |
| Japan | F2 | 77 | 78 | 78 | 76 | 18 |
| Sweden | 3rd F | 77 | 84 | 76 | 76 | 38 |
| Mexico | A1 | 76 | 78 | 75 | 75 | 14 |
| Ecuador | 3rd E | 76 | 76 | 76 | 77 | 23 |
| Algeria | 3rd J | 76 | 74 | 75 | 77 | 28 |
| Canada | B2 | 75 | 77 | 73 | 75 | 30 |
| Ghana | 3rd L | 75 | 77 | 74 | 73 | 73 |
| Paraguay | 3rd D | 75 | 73 | 75 | 76 | 41 |
| Egypt | G2 | 74 | 76 | 74 | 71 | 29 |
| DR Congo | 3rd K | 74 | 78 | 73 | 74 | 47 |
| Bosnia & Herzegovina | 3rd B | 73 | 76 | 70 | 75 | 64 |
| Australia | D2 | 71 | 69 | 68 | 71 | 27 |
| South Africa | A2 | 70 | 70 | 69 | 70 | 60 |
| Cape Verde | H2 | 70 | 67 | 69 | 69 | 67 |

## Notes on the rank-vs-rating divergences (cross-check, not corrections)
- **Ghana** sit FIFA #73 yet carry OVR 75 — SoFIFA rewards their Premier-League-calibre
  individuals (Williams/Ayew axis, Semenyo, Partey) more than FIFA's results-based ranking.
- **DR Congo** (#47) and **Bosnia** (#64) likewise rate higher on SoFIFA (74 / 73) than
  their ranking, on individual talent (Wissa/Bakambu; Džeko).
- **Sweden** carry an outlier ATT 84 (Isak + Gyökeres) on an otherwise OVR-77 side.
- Weight both signals; neither alone is decisive.

# The World in One Page — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/0xberuuu/news-24-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/0xberuuu/news-24-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Entry for the [news-image-20261124 bounty](https://make.fun/bounty/news-image-20261124): sum up 24 November's world news in one image.

`entry.png` is a 1024×1024 newspaper-style front page, drawn entirely in code with Python and Pillow — no AI-generated images, no photographs, no downloaded assets. Every story was verified against a reputable source on the day.

## Stories covered

1. **Drone strikes Riyadh tower, 11 hurt** — a drone attack hit the PIF Tower in Riyadh's financial district, the second strike on the capital in under a week (Al Jazeera).
2. **Huawei guilty of trade secrets theft** — a US jury found Huawei guilty of conspiracy to steal trade secrets and bank fraud, acquitting it of racketeering (BBC).
3. **Senegal win back Africa Cup title** — the Court of Arbitration for Sport returned the 2025 AFCON title to Senegal, overturning the ruling that had given the trophy to Morocco (Associated Press).
4. **Gunmen seize shoppers in Cartagena** — masked gunmen took about 30 people hostage at an Éxito supermarket in Cartagena, Colombia (CNN).
5. **Five killed in army helicopter crash** — a Turkish Air Force helicopter crashed after take-off from Eskisehir, killing all five crew (Turkish Ministry of National Defence).
6. **Ukraine hits Russian ships at sea** — Ukrainian drones struck the Russian cargo ship Sparta II in the Gulf of Finland and another vessel off Libya (Reuters).
7. **Madrid fight back to rout PSV 5-1** — Real Madrid came from a goal down to beat PSV 5-1 in the Champions League; Bellingham scored a stunning volley and Mbappé netted twice (Al Jazeera).

## Run it

Requirements: Python 3.10+ and Pillow (`pip install Pillow`). Uses only fonts already installed on the system (DejaVu).

```bash
python3 generate.py
```

This writes `entry.png` (1024×1024) in the current directory. The output is deterministic: running the command twice produces a byte-identical file (no randomness, no timestamps).

To reproduce the entry from this snapshot, run the entrypoint (Python standard library only — no third-party packages needed):

```bash
python3 main.py
```

This copies `entry.png` into the `out/` directory. A different output directory can be chosen with the `MAKEFUN_OUTPUT_DIR` environment variable:

```bash
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Either way the file written is byte-identical to the committed `entry.png`.

## Files

- `generate.py` — the program that draws the front page
- `main.py` — the entrypoint: copies `entry.png` into the output directory (`MAKEFUN_OUTPUT_DIR`, default `out/`)
- `entry.png` — the generated front page (1024×1024)
- `.makefun/owner.json` — entry owner wallet
- `LICENSE` — MIT

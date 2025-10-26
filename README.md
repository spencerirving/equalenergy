# EqualFlow — Natural Gas Price Equalization (Hackathon Prototype)

**Goal:** Given state-level **production** and **consumption**, compute:
1) **Statewise price** of natural gas (includes **transportation cost**), and
2) **Statewise source map** (who buys from whom and how much).

This is a **same-day prototype** designed for a hackathon.

## How it works (MVP)
- Build `State` objects from `data/states.csv`.
- Compute surplus/deficit.
- Build a **transport cost matrix** from state geo-coordinates (`data/state_latlon.csv`).
  - Cost model: `transport_cost($/MMBtu) = DIST_MILES * COST_PER_MILE`
  - Default `COST_PER_MILE = 0.0005` (tweakable in `src/config.py`).
- Greedy assignment of sellers → buyers minimizing **delivered unit cost** (`producer_base + transport`).
- Output state **price** as the average delivered cost for buyers (or base price for fulfilled producers).
- Output **flow network** CSV listing transfers.

> ⚠️ Data note: Replace `data/states.csv` with EIA-prepped values when ready.
> For a quick demo, a small sample is included.

## Files
- `src/models.py` — `State`, simple dataclasses
- `src/engine.py` — core matching + price computation
- `src/io.py` — CSV loaders/savers
- `src/config.py` — tunable params (base price, cost per mile)
- `src/run.py` — entry point
- `data/states.csv` — sample input (edit with real numbers)
- `data/state_latlon.csv` — centroids for distance
- `output/state_prices.csv` — final prices
- `output/flows.csv` — who sold to whom
- `output/summary.json` — basic metrics

## Quick start
```bash
python3 src/run.py
```
Then open files in `output/`.

## Assumptions (prototype)
- Units: **MMBtu** for pricing, **Bcf** for volume in input.
- Internal conversion assumes **1 Bcf ≈ 1,037,000 MMBtu**.
- Base producer price is uniform (`BASE_PRICE`), buyers pay **weighted avg delivered cost**.
- Greedy matching for speed; can be swapped for LP later.

## Next steps (tomorrow/presentation)
- Replace sample data with EIA numbers.
- Add distance weighting by pipeline corridors (if available) or bandwidth caps.
- Add UI map (Plotly/React) using `output/flows.csv`.

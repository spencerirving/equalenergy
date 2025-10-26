# EqualFlow - Natural Gas Priced Equalization

## Hack PSU Fall 2025

**Goal:** Given state-level **production** and **consumption** compute:

1. **Per State Price** of natural gas

- which is made up of per mile cost and a base cost

2. **Per State Source Map**

- this shows where each state should get its natural gas demand from that results in a narrower dispersion of prices

### How it works (MVP)

- Builds `State` objects from `data/states.csv `.
- Computes each state's surplus/deficit
- Uses state geo-coordinates from `data/state_latlon.csv` to determine the distance between each state.
  - Uses the distance between each state to calculate the `transportation_cost($/MMBtu) = distance_in_miles * COST_PER_MILE`
    - For this model we defined `COST_PER_MILE = 0.0005 ($/MMBtu)`
      - This value can be changed to account for a different cost per mile.
- Greedy assigns sellers to buyers to minimize **delivered unit cost**
- The price per state in `cost per MCF ($)` is calculated by `transportation_cost($/MMBtu) + BASE_COST`
  - For this model we defined `BASE_COST = 2.83 ($/MMBtu)`
    - This value can be changed to account for a different base cost
- The output flows and per state prices are outputted to `backend./equalflow/output`

### Files

- `src/models.py` - `State`, simple dataclass for each state
- `src/engine.py` - core matching + price computation
- `src/io.py` - CSV loaders/savers
- `src/run.py` - entry point
- `src/calculate_percentages.py` - calculates source percentages for each state
- `data/states.csv` - sample 2023 input (edit with real numbers)
- `data/states_latlon.csv` - central latitude and longitude coordianates of each state to calculate distance
- `data/current_state_prices_2023.csv`- actual 2023 state residential prices
- `output/state_prices.csv` - final prices
- `output/flows.csv` - who sold to whom
- `output/summary.json` - basic metrics
- `output/buyer_source_percentages` - percent of where each state recieved their natural gas from
- `frontend/2023_data_ui.py` - this is a map display the variation of actual 2023 prices
- `frontend/simulated_ui.py` - this is a map that displays our calculated variation prices

### Quick start

```bash
python3 backend/equalflow/run_EqualFlow.py
```

```bash
python3 frontend/simulated_ui.py
```

```bash
python3 frontend/old_2023_map_ui.py
```

### Assumptions

- Units: **MMBtu** for pricing, **Bcf** for volume in input.
- Internal conversion assumes **1 Bcf ≈ 1,037,000 MMBtu**.
- Base producer price (`BASE_PRICE`) is uniform.

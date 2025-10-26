import json, os
import subprocess
from .io import load_states, load_latlon, save_state_prices, save_flows
from .engine import convert_units, build_transport_costs, greedy_match, summarize

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")

def main():
    states = load_states(os.path.join(DATA_DIR, "states.csv")) #convert statewise consuption and production csv file to list
    latlon = load_latlon(os.path.join(DATA_DIR, "state_latlon.csv"))#convert statewise location csv file to list
    convert_units(states)#Bcf to MMBtu
    costs = build_transport_costs(states, latlon) #compute pairwise transport cost and stores in a dict
    greedy_match(states, costs)#finds out the most economically efficient deal and executes it
    save_state_prices(os.path.join(OUT_DIR, "state_prices.csv"), states)#save statewise prices
    save_flows(os.path.join(OUT_DIR, "flows.csv"), states)#save the entries made
    summary = summarize(states)#quantitative summary - total consuption, total production
    with open(os.path.join(OUT_DIR, "summary.json"), "w") as f:#readable output
        json.dump(summary, f, indent=2)
    src_dir = os.path.dirname(__file__)
    subprocess.run(
        ["python", "calculate_percentages.py"],
        check=True,
        cwd=src_dir  # <-- sets working directory before running the script
    )
    print("Done. See output/ for results.")

if __name__ == '__main__':
    main()

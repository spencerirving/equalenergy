#This program manages data input/output between the program and CSV files.

import csv
from typing import Dict, List
from .models import State

def load_states(path: str) -> List[State]:
    #Input: Path to your states.csv file.
    #Process: Reads each row (State, Production_Bcf, Consumption_Bcf) and creates a State object for it.
    #Output: Returns a list of State objects ready for implemennting in the engine.

    states = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            states.append(State(
                name=row['State'],
                produced_bcf=float(row['Production_Bcf']),
                consumed_bcf=float(row['Consumption_Bcf'])
            ))
    return states

def load_latlon(path: str) -> Dict[str, tuple]:
    #Input: Path to your state_latlon.csv file.
    #Process: Reads each state’s latitude and longitude.
    #Output: Returns a dict with elements "State": (long,lat)

    data = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row['State']] = (float(row['Lat']), float(row['Lon']))
    return data

def save_state_prices(path: str, states: List[State]):
    #Input: List of all State objects (after simulation).
    #Process: Extracts final price, fulfillment of the entry, and net production per state.
    #Output: Writes output/state_prices.csv, a clean table for presentation.
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['State','Price_USD_per_MMBtu','Fulfilled','Produced_Bcf','Consumed_Bcf','Net_Bcf'])
        for s in states:
            net_bcf = (s.net_mmbtu / 1_037_000)
            writer.writerow([s.name, round(s.price_usd_per_mmbtu, 4), s.fulfilled,
                             s.produced_bcf, s.consumed_bcf, round(net_bcf, 3)])

def save_flows(path: str, states: List[State]):
    #Input: List of State objects with sell_to data (who they sold to and how much).
    #Process: Loops through each seller and their buyers.
    #Output: Writes output/flows.csv, showing who sells gas to whom and volume (MMBtu).
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Seller','Buyer','MMBtu'])
        for s in states:
            for buyer, qty in s.sell_to:
                writer.writerow([s.name, buyer, round(qty, 2)])

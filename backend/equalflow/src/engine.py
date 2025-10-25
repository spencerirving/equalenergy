from typing import List, Dict, Tuple
import math
from .models import State
from . import config

def haversine_miles(lat1, lon1, lat2, lon2):
    #input - Latitudes and longitudes of 2 locations
    #process - Calculates shortest distance on two points on a shpere
    #output - Distance in miles

    R = 3958.8  # miles
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(a)) #Haversine Formula

def build_transport_costs(states: List[State], latlon: Dict[str, tuple]) -> Dict[Tuple[str,str], float]:
    # input  - List of states with names, and latitude/longitude mapping
    # process - Compute pairwise transport cost = distance × cost per mile
    # output  - Dictionary of transport costs between every state pair
  
    costs = {}
    for s in states:
        for t in states:
            if s.name == t.name: 
                continue
            if s.name in latlon and t.name in latlon:
                d = haversine_miles(*latlon[s.name], *latlon[t.name])
                costs[(s.name, t.name)] = d * config.COST_PER_MILE
    return costs

def convert_units(states: List[State]):
    # input  - List of states with production and consumption in Bcf
    # process - Convert values to MMBtu and compute net surplus/deficit
    # output  - Updated state objects with standardized energy units

    for s in states:
        s.produced_mmbtu = s.produced_bcf * config.BCF_TO_MMBTU
        s.consumed_mmbtu = s.consumed_bcf * config.BCF_TO_MMBTU
        s.net_mmbtu = s.produced_mmbtu - s.consumed_mmbtu
        s.fulfilled = s.net_mmbtu >= 0

def greedy_match(states: List[State], transport_costs: Dict[Tuple[str,str], float]):
    # input  - List of producer and consumer states with transport costs
    # process - Match sellers to buyers greedily to minimize delivered cost 
    # output  - Updated states with sell/buy lists and computed prices 

    producers = [s for s in states if s.net_mmbtu > 0]
    consumers = [s for s in states if s.net_mmbtu < 0]

    buyer_cost_buckets = {c.name: [] for c in consumers}

    
    for _ in range(10000): 
        consumers.sort(key=lambda x: x.net_mmbtu)  # Sort consumers by largest deficit first - most negative first
        for buyer in consumers:
            need = abs(buyer.net_mmbtu)
            # rank producers by delivered unit cost: base + transport
            ranked = sorted(
                [p for p in producers if p.net_mmbtu > 0],
                key=lambda p: (config.BASE_PRICE + transport_costs.get((p.name, buyer.name), 1e9))
            )

            for seller in ranked:
                if need <= 0: break
                available = seller.net_mmbtu
                if available <= 0: 
                    continue
    
                take = min(available, need, config.CHUNK_MMBTU)
                seller.net_mmbtu -= take  # Record enrty
                buyer.net_mmbtu += take
                seller.sell_to.append((buyer.name, take))
                buyer.buy_from.append((seller.name, take))

                # Price for this chunk at buyer = base + transport
                delivered = config.BASE_PRICE + transport_costs.get((seller.name, buyer.name), 0.0)
                buyer_cost_buckets[buyer.name].append((take, delivered))

                need -= take

    
    for s in states:# Final fulfillment flags
        s.fulfilled = s.net_mmbtu >= -1e-6  # if the difference in price is very small

   
    for s in states:  # Compute prices
        if s.name in buyer_cost_buckets and buyer_cost_buckets[s.name]:
            total_mmbtu = sum(q for q,_ in buyer_cost_buckets[s.name])
            avg_price = sum(q*price for q,price in buyer_cost_buckets[s.name]) / max(total_mmbtu, 1.0)
            s.price_usd_per_mmbtu = avg_price
        else:
            # Producer or self-sufficient: use base (slightly discounted if big surplus)
            discount = 0.05 if s.net_mmbtu > 0 else 0.0
            s.price_usd_per_mmbtu = config.BASE_PRICE * (1 - discount)

def summarize(states: List[State]):
    # input  - List of all state objects after matching
    # process - Aggregate totals and compute overall performance metrics
    # output  - Summary dictionary with production, consumption, deficit, and average price

    total_prod = sum(s.produced_mmbtu for s in states)
    total_cons = sum(s.consumed_mmbtu for s in states)
    deficits = [abs(s.net_mmbtu) for s in states if s.net_mmbtu < 0]
    unfulfilled = sum(1 for s in states if not s.fulfilled)
    return {
        'total_production_mmbtu': total_prod,
        'total_consumption_mmbtu': total_cons,
        'total_deficit_mmbtu_after': sum(deficits),
        'unfulfilled_states': unfulfilled,
        'average_price': sum(s.price_usd_per_mmbtu for s in states)/len(states)
    }

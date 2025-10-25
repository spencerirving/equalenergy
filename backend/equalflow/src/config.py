# Tunable parameters for the prototype - More can be added and tuned 


BASE_PRICE = 3.00 # Base commodity price ($/MMBtu) — uniform across producers for MVP
COST_PER_MILE = 0.0005 # Transport model: $ per MMBtu per mile (tweak during demo)
BCF_TO_MMBTU = 1_037_000 # Energy conversion: 1 Bcf to MMBtu (approximate)
CHUNK_MMBTU = 100_000_000 # Greedy matching chunk size (MMBtu) — smaller = more granular but slower

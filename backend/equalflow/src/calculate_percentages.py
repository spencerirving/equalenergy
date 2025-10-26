import pandas as pd

# Load your flows.csv
flows = pd.read_csv("../output/flows.csv")

flows_grouped = flows.groupby(["Buyer", "Seller"], as_index=False)["MMBtu"].sum()

# Group by buyer to get total inflow
buyer_totals = flows.groupby("Buyer")["MMBtu"].sum().reset_index()
buyer_totals.rename(columns={"MMBtu": "Total_MMBtu"}, inplace=True)

# Merge totals back to compute percentages
merged = flows.merge(buyer_totals, on="Buyer")
merged["Percent"] = (merged["MMBtu"] / merged["Total_MMBtu"]) * 100

# Optional: sort
merged = merged.sort_values(["Buyer", "Percent"], ascending=[True, False])
merged = merged.round({"Percent": 2})  # optional: round nicely

# Save to CSV
merged[["Buyer", "Seller", "Percent"]].to_csv("../output/buyer_source_percentages.csv", index=False)
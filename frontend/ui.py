import plotly.express as px
import pandas as pd
import csv
import json
from urllib.request import urlopen

# Read your CSV and convert numeric values
with open('../backend/equalflow/output/state_prices.csv', newline='') as csvfile:
    reader = list(csv.reader(csvfile))
    header = reader[0]
    data_rows = reader[1:]
    first_column = [row[0] for row in data_rows]
    second_column = [float(row[1]) for row in data_rows]  # Convert to float

df = pd.DataFrame({
    "state": first_column,
    "cost_per_mcf": second_column
})

# Load GeoJSON for US states
with urlopen("https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json") as response:
    states_geo = json.load(response)

# Custom purple gradient
custom_scale = [
    [0.0, "#240046"],  # Deep violet
    [0.17, "#3c096c"],
    [0.34, "#5a189a"],
    [0.51, "#7b2cbf"],
    [0.68, "#9d4edd"],
    [0.85, "#c77dff"],
    [1.0, "#e0aaff"]   # Light lavender
]

# Create the choropleth
fig = px.choropleth(
    df,
    geojson=states_geo,
    locations="state",
    featureidkey="properties.name",
    color="cost_per_mcf",
    color_continuous_scale=custom_scale,
    range_color=(df["cost_per_mcf"].min(), df["cost_per_mcf"].max()),
    scope="usa",
    title="Natural Gas Prices by State"
)

fig.update_traces(
    hovertemplate=
    "<b>%{location}</b><br>" +           # State name bolded
    "Cost per MCF: <b>$%{z:.2f}</b><extra></extra>",  # z is the color value
    hoverlabel=dict(
        bgcolor="#240046",  # deep purple hover background
        font_size=14,
        font_family="Arial",
        font_color="white",
        bordercolor="white"
    )
)

# Update map and layout styling
fig.update_geos(
    fitbounds="locations",
    visible=False,
    showlakes=False,
    showcountries=False,
    showframe=False,
    showcoastlines=False,
    bgcolor="#10002b"
)

fig.update_traces(marker_line_color="white", marker_line_width=1.2)  # White borders!

fig.update_layout(
    paper_bgcolor="#10002b",  # Ultra-dark background
    plot_bgcolor="#10002b",
    geo_bgcolor="#10002b",
    font=dict(color="white"),
    title_font=dict(size=22, color="white"),
)

fig.show()
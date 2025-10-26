import plotly.express as px
import pandas as pd
import json
from urllib.request import urlopen

# --- Load 2023 Price Data from CSV ---
df = pd.read_csv("../backend/equalflow/data/current_state_prices_2023.csv")

# --- Load GeoJSON for US States ---
with urlopen("https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json") as response:
    states_geo = json.load(response)

# --- Custom Blue Gradient (User's Palette) ---
custom_scale = [
    [0.0, "#03045e"],
    [0.12, "#023e8a"],
    [0.25, "#0077b6"],
    [0.38, "#0096c7"],
    [0.50, "#00b4d8"],
    [0.63, "#48cae4"],
    [0.75, "#90e0ef"],
    [0.88, "#ade8f4"],
    [1.0, "#caf0f8"]
]

# --- Create Choropleth ---
fig = px.choropleth(
    df,
    geojson=states_geo,
    locations="State",
    featureidkey="properties.name",
    color="2023_Price",
    color_continuous_scale=custom_scale,
    range_color=(df["2023_Price"].min(), df["2023_Price"].max()),
    scope="usa",
    title="2023 Natural Gas Prices by State"
)

# --- Hover Template ---
fig.update_traces(
    hovertemplate="<b>%{location}</b><br><br>2023 Price: <b>$%{z:.2f}</b><extra></extra>",
    hoverlabel=dict(
        bgcolor="#03045e",
        font_size=14,
        font_family="Arial",
        font_color="white",
        bordercolor="white"
    )
)

# --- Layout and Style ---
fig.update_layout(
    coloraxis_colorbar=dict(title="Price per MCF ($)"),
    paper_bgcolor="#001233",   # Deep navy background for contrast
    plot_bgcolor="#001233",
    geo_bgcolor="#001233",
    font=dict(color="white"),
    title_font=dict(size=22, color="white"),
)

fig.update_geos(
    fitbounds="locations",
    visible=False,
    showlakes=False,
    showcountries=False,
    showframe=False,
    showcoastlines=False,
    bgcolor="#001233"
)

fig.update_traces(marker_line_color="white", marker_line_width=1.2)

# --- Display ---
fig.show()

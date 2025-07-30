import pandas as pd
from bridges.bridges import Bridges
from bridges.data_src_dependent import get_us_map_county_data
from bridges.us_map import USMap
from bridges.color import Color

# Load county stats data
df = pd.read_csv("NC_county_stats.csv")

# Clean and prepare county names
df["County"] = df["County"].str.replace(" County", "").str.upper().str.strip()

# Convert bachelor degree percentages to floats
df["BachelorRate"] = df["Percentage of adults with a bachelor's degree"].str.replace("%", "").astype(float) / 100

# Create a dictionary: county name -> bachelor degree rate
bachelor_data = dict(zip(df["County"], df["BachelorRate"]))

color_scale = [
    Color(241, 238, 246),  # #f1eef6
    Color(189, 201, 225),  # #bdc9e1
    Color(116, 169, 207),  # #74a9cf
    Color(43, 140, 190),   # #2b8cbe
    Color(4, 90, 141),     # #045a8d
]

# Function to assign color by bachelor degree rate
def get_color(val):
    if val is None:
        return Color(220, 220, 220)
    elif val < 0.15:
        return color_scale[0]
    elif val < 0.25:
        return color_scale[1]
    elif val < 0.35:
        return color_scale[2]
    elif val < 0.45:
        return color_scale[3]
    else:
        return color_scale[4]

# Bridges
bridges = Bridges(102, "vilvt", "1609338639449")
bridges.set_title("Bachelor’s Degree Attainment Rates in NC Counties")
bridges.set_description(
    "This map visualizes the percentage of adults with a bachelor's degree by county in North Carolina."
    " Darker blue colors represent higher attainment rates based on the ColorBrewer pinks scale."
)

states = get_us_map_county_data(["North Carolina"], True)

# Color counties based on bachelor degree rate
for state in states:
    for county in state.counties:
        name = county.county_name.upper().replace(", NC", "").strip()
        val = bachelor_data.get(name)
        county.fill_color = get_color(val)
        county.stroke_color = Color(255, 255, 255)  # white borders

# Create and visualize map
map_obj = USMap(states)
bridges.set_data_structure(map_obj)
bridges.visualize()



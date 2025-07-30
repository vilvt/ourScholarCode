import pandas as pd
from bridges.bridges import Bridges
from bridges.data_src_dependent import get_us_map_county_data
from bridges.us_map import USMap
from bridges.color import Color

# Reading and defining csv file
df = pd.read_csv("NC_county_stats.csv")
df["County"] = df["County"].str.replace(" County", "").str.upper().str.strip()
df["Poverty200"] = df["Percentage of people with low incomes (under 200% of the  poverty level)"].str.replace("%", "").astype(float) / 100
poverty_data = dict(zip(df["County"], df["Poverty200"]))

color_scale = [
    Color(241, 238, 246),  # #f1eef6
    Color(189, 201, 225),  # #bdc9e1
    Color(116, 169, 207),  # #74a9cf
    Color(43, 140, 190),   # #2b8cbe
    Color(4, 90, 141),     # #045a8d
]

def get_color(val):
    if val is None:
        return Color(220, 220, 220)
    elif val < 0.30:
        return color_scale[0]
    elif val < 0.40:
        return color_scale[1]
    elif val < 0.50:
        return color_scale[2]
    elif val < 0.60:
        return color_scale[3]
    else:
        return color_scale[4]


# Initialize BRIDGES
bridges = Bridges(4, "vilvt", "1609338639449")
bridges.set_title("NC Poverty Rates (<200%)")
bridges.set_description("Percent of population under 200% of the poverty line.")

# Get NC counties
states = get_us_map_county_data(["North Carolina"], True)
for state in states:
    for county in state.counties:
        name = county.county_name.upper().replace(", NC", "").strip()
        val = poverty_data.get(name)
        county.fill_color = get_color(val) if val is not None else Color(220, 220, 220)
        county.stroke_color = Color(255, 255, 255)

# Create map
map_obj = USMap(states)
bridges.set_data_structure(map_obj)
bridges.visualize()


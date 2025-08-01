from bridges.bridges import Bridges
from bridges.data_src_dependent import get_us_map_county_data
from bridges.us_map import USMap
from bridges.color import Color
import pandas as pd

# Load rural/urban classification data
df = pd.read_csv("RuralUrbanTable.csv")
df["County"] = df["County"].str.upper().str.strip()
classification_dict = dict(zip(df["County"], df["Classification"]))

# ColorBrewer-style diverging colors
classification_colors = {
    "Rural": Color(198, 102, 102),     # Red
    "Suburban": Color(170, 145, 188), # Purple
    "Urban": Color(120, 150, 200)        # Blue
}

# Initialize Bridges
bridges = Bridges(3, "vilvt", "1609338639449")
bridges.set_title("NC Counties: Rural vs Suburban vs Urban, 2020")
bridges.set_description("Color-coded by classification using ColorBrewer-style diverging scale. Rural: Red. Suburban: Purple. Urban: Blue.")

# Load North Carolina counties
state_info = get_us_map_county_data(["North Carolina"], True)

for state in state_info:
    if state.state_name == "North Carolina":
        for county in state.counties:
            county_name = county.county_name.upper().replace(", NC", "").strip()
            classification = classification_dict.get(county_name, None)

            if classification:
                color = classification_colors.get(classification, Color(200, 200, 200))
            else:
                color = Color(220, 220, 220)  # Default gray for missing

            county.fill_color = color
            county.stroke_color = Color(255, 255, 255)  # White borders

# Visualize map
my_map = USMap(state_info)
bridges.set_data_structure(my_map)
bridges.visualize()

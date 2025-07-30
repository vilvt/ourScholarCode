from bridges.bridges import Bridges
from bridges.data_src_dependent import get_us_map_county_data
from bridges.us_map import USMap
from bridges.color import Color
import pandas as pd

# Load Medicaid data
df = pd.read_csv("NC_2024_Medicaid.csv")
df["COUNTY NAME"] = df["COUNTY NAME"].str.upper().str.strip()
medicaid_dict = dict(zip(df["COUNTY NAME"], df["RATE ENROLLED"]))

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
    elif val < 0.15:
        return color_scale[0]
    elif val < 0.30:
        return color_scale[1]
    elif val < 0.45:
        return color_scale[2]
    elif val < 0.60:
        return color_scale[3]
    else:
        return color_scale[4]


# Initialize Bridges
bridges = Bridges(5, "vilvt", "1609338639449")
bridges.set_title("NC Counties: 2024 Medicaid Enrollment Rate")
bridges.set_description("Color-coded by percentage of population enrolled in Medicaid using ColorBrewer 5-blue scale.")

# Load North Carolina county map
state_info = get_us_map_county_data(["North Carolina"], True)

for state in state_info:
    if state.state_name == "North Carolina":
        for county in state.counties:
            county_name = county.county_name.upper().replace(", NC", "").strip()
            percent = medicaid_dict.get(county_name, None)

            if percent is not None:
                color = get_color(percent)
            else:
                color = Color(220, 220, 220)  # Gray if data missing

            county.fill_color = color
            county.stroke_color = Color(255, 255, 255)  # White border

# Visualize map
my_map = USMap(state_info)
bridges.set_data_structure(my_map)
bridges.visualize()

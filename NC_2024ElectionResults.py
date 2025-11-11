from bridges.bridges import Bridges
from bridges.data_src_dependent import get_us_map_county_data
from bridges.us_map import USMap
from bridges.color import Color
import pandas as pd

def hex_to_color(hex_str):
    hex_str = hex_str.lstrip("#")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return Color(r, g, b)

# 9-step diverging scale
def get_detailed_diverging_color(norm_score):
    norm_score = max(min(norm_score, 1), -1)
    colors = [
        ("#08306B", -1.0),
        ("#2171B5", -0.75),
        ("#6BAED6", -0.5),
        ("#BDD7E7", -0.25),
        ("#F7F7F7", 0.0),
        ("#FCAE91", 0.25),
        ("#FB6A4A", 0.5),
        ("#DE2D26", 0.75),
        ("#A50F15", 1.0),
    ]
    for i in range(len(colors) - 1):
        low_color, low_val = colors[i]
        high_color, high_val = colors[i + 1]
        if low_val <= norm_score <= high_val:
            mid_val = (low_val + high_val) / 2
            chosen = low_color if norm_score < mid_val else high_color
            return hex_to_color(chosen)
    return hex_to_color("#F7F7F7")

# Reading and defining csv file
def make_map(year, assignment_num, df, state_info):
    df["year"] = df["year"].astype(int)
    df["party"] = df["party"].str.upper().str.strip()

    df_year = df[df["year"] == year].copy()
    print(f"Year {year} rows: {len(df_year)}")  # Debug info

    # Determine county column name ('county_name' or 'county')
    county_col = "county_name" if "county_name" in df_year.columns else "county"
    df_year[county_col] = df_year[county_col].str.upper().str.strip()

    df_year = df_year[df_year["party"].isin(["DEMOCRAT", "REPUBLICAN"])]

    pivot = df_year.pivot_table(
        index=county_col, columns="party", values="candidatevotes", aggfunc="sum", fill_value=0
    )

    #Count and normalize votes into color category
    for county in state_info[0].counties:
        county_name = county.county_name.upper().replace(", NC", "").strip()
        if county_name in pivot.index:
            rep_votes = pivot.loc[county_name].get("REPUBLICAN", 0)
            dem_votes = pivot.loc[county_name].get("DEMOCRAT", 0)
            total_votes = rep_votes + dem_votes
            norm_score = (rep_votes - dem_votes) / total_votes if total_votes > 0 else 0
            county.fill_color = get_detailed_diverging_color(norm_score)
            county.stroke_color = Color(40, 40, 40)
        else:
            county.fill_color = Color(200, 200, 200)
            county.stroke_color = Color(100, 100, 100)

    us_map = USMap(state_info)
    bridges = Bridges(assignment_num, username, apikey)
    bridges.set_title(f"NC {year} Presidential Election Results by County")
    bridges.set_description(
        "Map of North Carolina election results by county. "
        "Color intensity reflects the margin between Republican (red) and Democrat (blue) "
        "using a 9-step diverging scale. Counties near white are more evenly split."
    )
    bridges.set_data_structure(us_map)
    bridges.visualize()
    print(f"Visualized {year} election map.")

# Print and process info
def main():
    df = pd.read_csv("NC_countypresresults_2000-2024.csv")

    state_info = get_us_map_county_data(["North Carolina"], True)

    make_map(2000, 1, df, state_info)
    make_map(2024, 10, df, state_info)

if __name__ == "__main__":
    main()




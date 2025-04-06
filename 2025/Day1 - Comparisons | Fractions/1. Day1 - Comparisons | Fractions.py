# IMPORT LIBRARIES
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as mticker
#pip install pycountry
import pycountry
import geopandas as gpd
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

# IMPORT DATA
gdf = gpd.read_file("/content/drive/MyDrive/30DayChartChallenge/datasets/blue economy/eez_v10.shp")# https://doi.org/10.14284/312]
df_land = pd.read_csv("/content/drive/MyDrive/30DayChartChallenge/datasets/blue economy/API_AG.LND.TOTL.K2_DS2_en_csv_v2_26346/API_AG.LND.TOTL.K2_DS2_en_csv_v2_26346.csv",skiprows=4) #https://data.worldbank.org/indicator/AG.LND.TOTL.K2?end=2022&name_desc=false&start=2022&view=map

# PROCESS DATA
# drop useless columns
columns_to_keep_gdf = ['Sovereign1', 'ISO_Ter1','Area_km2']
gdf = gdf[columns_to_keep_gdf]
columns_to_keep_df_land = ['Country Code', 'Country Name','2021']
df_land = df_land[columns_to_keep_df_land]
# merge dataframes
df = pd.merge(df_land, gdf, left_on='Country Code', right_on='ISO_Ter1', how='left')
df.rename(columns={'2021': 'Land Area','Area_km2': 'EEZ Area'}, inplace=True)
df = df.drop_duplicates(subset=['Country Code'], keep='last')
# add Fraction column
df['Fraction %'] = (df['EEZ Area'] / df['Land Area']) * 100
df['Fraction %'] = df['Fraction %'].round(0)
# sort DATA
df = df.sort_values(by='EEZ Area', ascending=False).head(20) # use choosen variable
center_sorted = []
left = True
for i in range(len(df)):
    if left:
        center_sorted.insert(0, df.iloc[i])  # insert at beginning
    else:
        center_sorted.append(df.iloc[i])     # insert at end
    left = not left
df = pd.DataFrame(center_sorted).reset_index(drop=True)

# PLOT BIHISTOGRAM
x = df['Country Name']
eez = df['EEZ Area']
land = -df['Land Area']  # Negative

fig, ax = plt.subplots(figsize=(12, 6))
bars_eez = ax.bar(x, eez, color='#0099FF', label='EEZ Area (km²)', alpha=0.5)
bars_land = ax.bar(x, land, color='#33FFA2', label='Land Area (km²)', alpha=0.5)

# DESIGN
# add df['Fraction %'] as label
for i, bar in enumerate(bars_eez):
    fraction = df.iloc[i]['Fraction %']
    if pd.notna(fraction):
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # center of bar
            bar.get_height() + 50000,           # slightly above bar
            f"{int(fraction)}%",                # round and format
            ha='center', va='bottom', fontsize=8, fontweight='light'
        )
fig.patch.set_facecolor('oldlace')
ax.set_facecolor('oldlace')
ax.set_ylabel("")
ax.set_yticks([])
ax.set_xticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
# add image
img = mpimg.imread('/content/drive/MyDrive/30DayChartChallenge/datasets/blue economy/8666692_power_icon.png')
imagebox = OffsetImage(img, zoom=0.9)
ab = AnnotationBbox(imagebox, (20, 10), frameon=False)  # (x,y) position
ax.add_artist(ab)

# ANNOTATIONS
ax.set_title("FRACTION: MARITIME EXCLUSIVE ECONOMIC ZONE AREA/ LAND AREA \nTOP 20 EEZ AREAS\n", fontsize=16, fontweight='bold')
ax.text(10, -30000000, "matplotlib | #30DayChartChallenge | ade yang | Day 1 - Fraction", ha='center', fontsize=10, fontweight='light', color='gray')
ax.set_xticks(np.arange(len(x)))
ax.set_xticklabels(x, rotation=45, ha='right')
ax.legend(loc='upper right')

plt.tight_layout()
plt.show()

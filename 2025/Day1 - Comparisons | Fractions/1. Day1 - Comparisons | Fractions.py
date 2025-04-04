# IMPORT LIBRARIES
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as mticker
import pycountry
import geopandas as gpd

# IMPORT DATA
gdf = gpd.read_file("/content/drive/MyDrive/30DayChartChallenge/datasets/blue economy/eez_v10.shp")# https://doi.org/10.14284/312]
df_land = pd.read_csv("/content/drive/MyDrive/30DayChartChallenge/datasets/blue economy/API_AG.LND.TOTL.K2_DS2_en_csv_v2_26346/API_AG.LND.TOTL.K2_DS2_en_csv_v2_26346.csv",skiprows=4) #https://data.worldbank.org/indicator/AG.LND.TOTL.K2?end=2022&name_desc=false&start=2022&view=map

# PROCESS DATA
  # ADD ISO COUNTRY CODE
def get_country_code(name):
    try:
        return pycountry.countries.lookup(name).alpha_3
    except:
        return None  # if no match is found
gdf['Country Code'] = gdf['Sovereign1'].apply(get_country_code)
columns_to_keep = ['Country Code', 'Country Name','2021']
df_land = df_land[columns_to_keep]
  # MERGE THE DFs
df = pd.merge(dff, df_land, on='Country Code', how='left')
df.rename(columns={
    '2021': 'Land Area',
    'Area_km2': 'EEZ Area'
}, inplace=True)
df['Fraction %'] = (df['EEZ Area'] / df['Land Area']) * 100
df['Fraction %'] = df['Fraction %'].round(0)  # maybe I won't use it....

# PROCESS DATA #2 FOR PLOT
df_top = df.sort_values(by='Land Area', ascending=False).head(10)

x = df_top['Country Code']
eez = df_top['EEZ Area']
land = -df_top['Land Area']  # Negative 

# BIHISTOGRAM PLOT
fig, ax = plt.subplots(figsize=(12, 6))
bars_eez = ax.bar(x, eez, color='steelblue', label='EEZ Area (km²)', alpha=0.5)
bars_land = ax.bar(x, land, color='darkgreen', label='Land Area (km²)', alpha=0.5)

# DESIGN
for i, bar in enumerate(bars_eez):
    fraction = df_top.iloc[i]['Fraction %']
    if pd.notna(fraction):
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # center of bar
            bar.get_height() + 50000,           # slightly above bar
            f"{int(fraction)}%",                # round and format
            ha='center', va='bottom', fontsize=9, fontweight='bold'
        )
fig.patch.set_facecolor('oldlace')
ax.set_facecolor('oldlace')
ax.set_ylabel("")
ax.set_yticks([])
ax.set_xticks([])
ax.spines['left'].set_color('oldlace')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# ANNOTATIONS
ax.set_title("FRACTION: MARITIME EXCLUSIVE ECONOMIC ZONE / LAND AREA \nTOP 10 LAND AREAS\n", fontsize=16, fontweight='bold')
ax.text(4.5, min(land)*1.1, "matplotlib | #30DayChartChallenge | ade yang | Day 1 - Fraction", 
        ha='center', fontsize=10, fontweight='light', color='gray')
ax.set_xticks(np.arange(len(x)))
ax.set_xticklabels(x, rotation=45, ha='right')

plt.tight_layout()
plt.show()

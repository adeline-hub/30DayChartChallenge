#IMPORT USEFULL LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

#IMPORT DATA
# LAND (129,718,826.2, km2 WORLD BANK)
df_land = pd.read_csv("/content/drive/MyDrive/30DayChartChallenge/datasets/blue economy/API_AG.LND.TOTL.K2_DS2_en_csv_v2_26346/API_AG.LND.TOTL.K2_DS2_en_csv_v2_26346.csv",skiprows=4)
print(df_land.shape)
columns_to_keep = ['Country Code', 'Country Name','2021']
df_land = df_land[columns_to_keep]
# EEZ
import geopandas as gpd
gdf = gpd.read_file("/content/drive/MyDrive/30DayChartChallenge/datasets/blue economy/eez_v10.shp")
columns_to_keep = ['Sovereign1', 'ISO_Ter1','Area_km2']
gdf = gdf[columns_to_keep]

# MERGE DATA
df = pd.merge(df_land, gdf, left_on='Country Code', right_on='ISO_Ter1', how='left')
df.rename(columns={
    '2021': 'Land Area',
    'Area_km2': 'EEZ Area'
}, inplace=True)

# CLEAN DATA
df['EEZ Area'].fillna(0, inplace=True)
df['Land Area'].fillna(0, inplace=True)
df['EEZ Area'] = df['EEZ Area'].astype(float)
df['Land Area'] = df['Land Area'].astype(float)
df['ISO_Ter1'].fillna(df['Country Code'], inplace=True)
df['Sovereign1'].fillna(df['Country Name'], inplace=True)
codes_to_drop = [
    'WLD','IBT','ECS','TEC','IBD','TLA','LCN','LAC','NAC','LTE','HIC','LMY','MIC',
    'ECA','IDA','UMC','FCS','IDX','AFE','TSS','SSF','SSA','LIC','LDC','HPC','PRE',
    'EAR','PST','LMC','IDB','EUU','CEB','EMU','OED','TEA','EAP','MEA','TMN','MNA',
    'TSA','SAS','AFW','EAS','ARB'
]
df = df[~df['Country Code'].isin(codes_to_drop)]
df['Total Claimed Area'] = df['Land Area'] + df['EEZ Area']

earth_surface_km2 = 510_072_000
total_land_km2 = 129_718_826.2
total_eez_km2 = df['EEZ Area'].sum()
free_ocean_km2 = earth_surface_km2 - total_land_km2 - total_eez_km2

#PROCESS DATA #2 (PLOT)
# Normalize widths
land_width = total_land_km2 / earth_surface_km2
eez_width = total_eez_km2 / earth_surface_km2
free_width = free_ocean_km2 / earth_surface_km2
colors = [
    (0.2, 1.0, 0.63, 0.6),  # #33FFA2 with alpha = 0.3
    (0.45, 0.57, 0.7, 0.4),  # #7393B3 with alpha = 0.3
    (0.0, 0.6, 1.0, 0.7)     # #0099FF with alpha = 0.3
] # land, EEZ, free ocean

sizes = [1]

# NESTED PIE PLOT
fig, ax = plt.subplots(figsize=(10, 13)) 
fig.patch.set_facecolor('oldlace') 
ax.set_facecolor('oldlace')  

ax.pie(sizes, colors=[colors[2]], startangle=90, wedgeprops={'width': free_width, 'edgecolor': 'oldlace'}, radius=1.0) #OCEAN
ax.pie(sizes, colors=[colors[1]], startangle=90, wedgeprops={'width': eez_width, 'edgecolor': 'oldlace'}, radius=1.0 - free_width) #EEZ
ax.pie(sizes, colors=[colors[0]], startangle=90, wedgeprops={'width': land_width, 'edgecolor': 'oldlace'}, radius=1.0 - free_width - eez_width) #LAND
#ax.set(aspect="equal", title='Earth Surface Composition by Area\n(Land, EEZ, Free Ocean)')


# ANNOTATIONS
ax.text(0.42, 0.5, "129,718,826 km2", fontsize=11, fontweight='light', fontname="Sans Serif", ha='left', va='top', transform=ax.transAxes, color="black", rotation=0)
ax.text(0.42, 0.65, "124,237,419 km²", fontsize=11, fontweight='light', fontname="Sans Serif", ha='left', va='top', transform=ax.transAxes, color="white", rotation=0)
ax.text(0.42, 0.8, "256,115,755 km²", fontsize=11, fontweight='light', fontname="Sans Serif", ha='left', va='top', transform=ax.transAxes, color="white", rotation=0)

ax.text(0.5, 0.55, "Land", fontsize=14, fontweight='light', fontname="Sans Serif",ha='center', va='top', transform=ax.transAxes, color="black", rotation=0)
ax.text(0.5, 0.36, "EEZ", fontsize=14, fontweight='light', fontname="Sans Serif",ha='center', va='top', transform=ax.transAxes, color="white", rotation=0)
ax.text(0.5, 0.23, "High Seas", fontsize=14, fontweight='light', fontname="Sans Serif",ha='center', va='top', transform=ax.transAxes, color="white", rotation=0)

earth_surface_km2 = 510_072_000  
total_land_km2 = total_land_km2 
total_eez_km2 = df['EEZ Area'].sum()
total_water_km2 = earth_surface_km2 - total_land_km2 - total_eez_km2
pct_land = total_land_km2 / earth_surface_km2 * 100
pct_eez = total_eez_km2 / earth_surface_km2 * 100
pct_free_water = total_water_km2 / earth_surface_km2 * 100
ax.text(0, -0.25, f"{pct_land:.1f}%", ha='center', va='center', fontsize=12, color='black', bbox=dict(facecolor='#33FFA2', edgecolor='oldlace', boxstyle='circle,pad=0.1'))
ax.text(-0.4, 0.38, f"{pct_eez:.1f}%", ha='center', va='center', fontsize=12, color='white', bbox=dict(facecolor='#7393B3', edgecolor='oldlace', boxstyle='circle,pad=0.1'))
ax.text(0.4, 0.89, f"{pct_free_water:.1f}%", ha='center', va='center', fontsize=12, color='white', bbox=dict(facecolor='#0099FF', edgecolor='oldlace', boxstyle='circle,pad=0.1'))

ax.text(0.5, -0.07, "Source: World Bank, VLIZ | matplotlib | #30DayChartChallenge | ade yang | Day 3 – Circular", fontsize=10, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="black")

#DESIGN PART #2
ax.set_title("AEARTH =\nLAND + EXCLUSIVE ECONOMIC ZONES (EEZ)\n+ HIGH SEAS\n", fontsize=18)

plt.show()

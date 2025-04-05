# IMPORT LIBRARIES
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle

# IMPORT DATA
df_land = pd.read_csv(    "/content/drive/MyDrive/30DayChartChallenge/datasets/blue economy/API_AG.LND.TOTL.K2_DS2_en_csv_v2_26346/API_AG.LND.TOTL.K2_DS2_en_csv_v2_26346.csv", skiprows=4)

# PROCESS DATA
  # DROP COLUMNS & ROWS
columns_to_keep = ['Country Code', 'Country Name', '1961', '2021']
df_land = df_land[columns_to_keep]
codes_to_drop = [
    'WLD','IBT','ECS','TEC','IBD','TLA','LCN','LAC','NAC','LTE','HIC','LMY','MIC',
    'ECA','IDA','UMC','FCS','IDX','AFE','TSS','SSF','SSA','LIC','LDC','HPC','PRE',
    'EAR','PST','LMC','IDB','EUU','CEB','EMU','OED','TEA','EAP','MEA','TMN','MNA',
    'TSA','SAS','AFW','EAS','ARB'
]
df_land = df_land[~df_land['Country Code'].isin(codes_to_drop)]
  # ADD COLUMN 'BETWEEN'
df_land[['1961', '2021']] = df_land[['1961', '2021']].fillna(0)
df_land['Between'] = df_land['2021'] - df_land['1961']
df_filtered = df_land[df_land['Between'] < 0].sort_values(by='Between').head(10)
  # MANUAL SCALING 
scaling_factors = {'United States': 10, 'Canada': 10, 'Iran, Islamic Rep.': 3, 'Cuba':1.15}
df_filtered['1961_adj'] = df_filtered.apply(
    lambda row: row['1961'] / scaling_factors.get(row['Country Name'], 1), axis=1)
df_filtered['2021_adj'] = df_filtered.apply(
    lambda row: row['2021'] / scaling_factors.get(row['Country Name'], 1), axis=1)
df_long = pd.melt(df_filtered, id_vars=['Country Name'], value_vars=['1961_adj', '2021_adj'],
                  var_name='Year', value_name='Land Area (km²)')
df_long['Year'] = df_long['Year'].map({'1961_adj': 1961, '2021_adj': 2021})

# PLOT SLOPE CHART
fig, ax = plt.subplots(figsize=(10, 13))

for country in df_long['Country Name'].unique():
    data = df_long[df_long['Country Name'] == country]
    ax.plot(data['Year'], data['Land Area (km²)'], marker='o', linewidth=4, alpha=0.4)
    # Annotate with land area values
    ax.text(1961 - 8, data['Land Area (km²)'].values[0], f"{data['Land Area (km²)'].values[0]:,.0f} km²",
            va='center', ha='left', fontsize=9, color='oldlace') 
    ax.text(2021 + 1, data['Land Area (km²)'].values[1], f"{data['Land Area (km²)'].values[1]:,.0f} km²", 
            va='center', ha='left', fontsize=9, color='oldlace')
    # Country label and change, move above the lines in black
    ax.text(1991, (data['Land Area (km²)'].values[0] + data['Land Area (km²)'].values[1]) / 2,
            f"{country}", va='baseline', ha='center', fontsize=14, color='grey')

# DESIGN
ax.set_xticks([1961, 2021])
ax.set_yticks([])
ax.set_xticklabels(['1961', '2021'], fontsize=12, fontweight='bold')
ax.set_facecolor('oldlace')
fig.patch.set_facecolor('oldlace')
for spine in ax.spines.values():
    spine.set_visible(False)

# ANNOTATIONS
ax.text( -0.017, 0.96, "9,158,960 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #USA
ax.text( -0.017, 0.94, "8,965,590 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #CAN
ax.text( -0.017, 0.57, "1,628,760 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #IRAN
ax.text( -0.017, 0.465, "437,370 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #IRAK
ax.text( -0.017, 0.39, "366,700 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #JAPAN
ax.text( -0.017, 0.35, "325,490 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #VIETNAM
ax.text( -0.017, 0.30, "276,840 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #ECUADOR
ax.text( -0.017, 0.123, "110,630 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #BULGARIA
ax.text( -0.017, 0.11, "107,400 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #CUBA
ax.text( -0.017, 0.055, "46,723 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #BUTHAN

ax.text( 1.019, 0.96, "9,147,420 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #USA
ax.text( 1.019, 0.925, "8,788,700 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #CAN
ax.text( 1.019, 0.57, "1,622,500 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #IRAN
ax.text( 1.019, 0.462, "434,128 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #IRAK
ax.text( 1.019, 0.385, "364,500 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #JAPAN
ax.text( 1.019, 0.342, "313,429 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #VIETNAM
ax.text( 1.019, 0.272, "248,360 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #ECUADOR
ax.text( 1.019, 0.123, "108,560 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #BULGARIA
ax.text( 1.019, 0.105, "103,800 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #CUBA
ax.text( 1.019, 0.050, "38,140 km²", fontsize=9, ha='center', va='top', transform=ax.transAxes, color="grey") #BUTHAN

ax.text( 0.70, 0.98, "THAWING OF\nTHE ARTIC", fontsize=13, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=90)
ax.text( 0.85, 0.905, "FLOODING\nAND\nCOASTAL EROSION", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=0)
ax.text( 0.85, 0.270, "COASTAL\n   EROSION", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=0) #ECUADOR
ax.text( 0.9, 0.343, "MEKONG\nDELTA\nFLOODING", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=0) #VIETNAM
ax.text( 0.6, 0.999, "HURRICANE\nKATRINA", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=0)
ax.text( 0.3, 0.055, "HYDROELECTRIC\nDAMS", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=0)
ax.text( 0.5, 0.64, "WATER\nSCARCITY", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=0)
ax.text( 0.7, 0.62, "LAKE URMIA\nCRISIS", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=90)
ax.text( 0.6, 0.11, "HURRICANES", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=0)
ax.text( 0.5, 0.8, "RISING SEA LEVEL", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=45)
ax.text( 0.2, 0.495, "GULF\nWAR", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=0)
ax.text( 0.8, 0.495, "ISIS\nCONFLICT", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=0)
ax.text( 0.8, 0.42, "TOHOKU\nEARTHQUAKE\nAND TSUNAMI", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=0)
ax.text( 0.35, 0.175, "MARKET\nECONOMY\nTRANSITION", fontsize=12, fontweight='light', fontname="Sans Serif", ha='center', va='top', transform=ax.transAxes, color="brown", rotation=0)

ax.set_title("\nTEN COUNTRIES WITH BIGGGEST LAND AREA LOSS\n(1961–2021)\n", fontsize=16, fontweight='bold')
plt.figtext(0.5, 0.01, "Source: World Bank | matplotlib | #30DayChartChallenge | ade yang | Day 2 – Slope", 
            ha='center', fontsize=9, color='gray')

plt.tight_layout()
plt.show()

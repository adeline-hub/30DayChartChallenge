# IMPORT LIBRARIES
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import geopandas as gpd
#pip install pycountry
#pip install pycountry_convert
import pycountry
import pycountry_convert as pc
from pycountry_convert import country_alpha2_to_continent_code
import seaborn as sns

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

# add Continent column
continents = {'NA': 'North America', 'SA': 'South America', 'AS': 'Asia', 'OC': 'Oceania', 'AF': 'Africa', 'EU': 'Europe'}
def alpha3_to_continent(alpha3):
    try:
        country = pycountry.countries.get(alpha_3=alpha3)
        alpha2 = country.alpha_2
        continent_code = country_alpha2_to_continent_code(alpha2)
        return continents.get(continent_code)
    except:
        return None
df['Continent'] = df['Country Code'].apply(alpha3_to_continent)
df = df[df['Continent'].notna()]

# groupby Continent
dff = df.groupby('Continent').agg({'EEZ Area': 'sum', 'Land Area': 'sum'}).reset_index()
dff['Fraction %'] = round((dff['EEZ Area'] / dff['Land Area']) * 100,1)

# save dff
dff.to_csv('/content/drive/MyDrive/30DayChartChallenge/datasets/blue economy/dff.csv', index=False)

# SCATER PLOT
plt.figure(figsize=(10, 10))
sns.scatterplot(data=dff, x="Land Area", y="EEZ Area", size="Land Area", hue="Continent", sizes=(1000, 15000), palette="pastel", alpha=0.6, edgecolor="#33FFA2")

# DESIGN PLOT
for i in range(dff.shape[0]):  
    plt.text(dff['Land Area'].iloc[i], dff['EEZ Area'].iloc[i], dff['Continent'].iloc[i], 
             fontsize=12, color='black', ha='center', va='center')
    plt.text(dff['Land Area'].iloc[i], dff['EEZ Area'].iloc[i] - 500000,  
             f"{dff['Fraction %'].iloc[i]:,.0f}%",  
             fontsize=8, color='black', ha='center', va='center')
plt.legend().set_visible(False)
fig = plt.gcf()  
fig.patch.set_facecolor('oldlace')  
ax = plt.gca()  
ax.set_facecolor('oldlace')  
for spine in ax.spines.values():
    spine.set_visible(False)
plt.xticks([]) 
plt.yticks([]) 

# ANNOTATIONS
plt.xlabel("Land Area (km²)", fontsize=12)
plt.ylabel("EEZ Area (km²)", fontsize=12)
plt.title("\nEXCLUSIVE ECONOMIC ZONE & LAND AREA DISTRIBUTION\nBY CONTINENT\n (EEZ/Land)", fontsize=16)
plt.text(12000000, 500000, "source: World Bank, VLIZ | #30DayChartChallenge | ade yang | Day 4 - Big & Small", fontsize=10, fontweight='light', color='gray')
plt.text(7500000, 21000000, "y-axis", fontsize=11, fontweight='light', fontname="Sans Serif", ha='left', va='top',  color="black", rotation=90, bbox=dict(facecolor='#33FFA2', edgecolor='black', boxstyle='rarrow,pad=1.2'))
plt.text(24000000, 3000000, "x-axis", fontsize=11, fontweight='light', fontname="Sans Serif", ha='left', va='top',  color="black", rotation=0, bbox=dict(facecolor='#33FFA2', edgecolor='black', boxstyle='rarrow,pad=1.2'))



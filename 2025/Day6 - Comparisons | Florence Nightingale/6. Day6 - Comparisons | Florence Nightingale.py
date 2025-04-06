# IMPORT LIBRARIES
import pandas as pd
#pip install pycountry
#pip install pycountry_convert
import pycountry
import pycountry_convert as pc
from pycountry_convert import country_alpha2_to_continent_code

# IMPORT DATA
df = pd.read_csv("/content/drive/MyDrive/30DayChartChallenge/datasets/blue economy/SGD14_Data.csv") #https://databank.worldbank.org/source/sustainable-development-goals-(sdgs)

# PROCESS DATA
# clean Data
def clean_df(df):
    df_cleaned = df.dropna(subset=['Country Name', 'Country Code'])
    df_cleaned = df_cleaned.dropna(how='all', subset=['2016 [YR2016]', '2017 [YR2017]', '2018 [YR2018]', '2019 [YR2019]', '2020 [YR2020]'])
    df_cleaned = df_cleaned[~df_cleaned['Country Name'].str.contains("Data from database|Last Updated", na=False)]
    year_columns = ['2016 [YR2016]', '2017 [YR2017]', '2018 [YR2018]', '2019 [YR2019]', '2020 [YR2020]']
    for col in year_columns:
        df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
    df_cleaned = df_cleaned.reset_index(drop=True)
    return df_cleaned
df_cleaned = clean_df(df)

columns_to_keep = ['Country Name', 'Country Code', 'Series Name', '2016 [YR2016]', '2017 [YR2017]', '2018 [YR2018]', '2019 [YR2019]', '2020 [YR2020]']
df_filtered = df_cleaned[columns_to_keep]

# FILTER DATA
df_filtered = df_filtered[df_filtered['Series Name'].str.contains('Aquaculture|Capture fisheries', case=False, na=False)]

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
df_filtered['Continent'] = df_filtered['Country Code'].apply(alpha3_to_continent)
df_filtered = df_filtered[df_filtered['Continent'].notna()]

# Garde uniquement les colonnes utiles (2016 à 2020)
years = ['2016 [YR2016]', '2017 [YR2017]', '2018 [YR2018]', '2019 [YR2019]', '2020 [YR2020]']
df_melted = df_filtered.melt(
    id_vars=['Country Name', 'Country Code', 'Continent', 'Series Name'],
    value_vars=years,
    var_name='Year',
    value_name='Value'
)

# Nettoyer l'année (enlever [YRxxxx])
df_melted['Year'] = df_melted['Year'].str.extract(r'(\d{4})')

# Pivot pour avoir Aquaculture et Capture côte à côte
df_pivot = df_melted.pivot_table(
    index=['Continent', 'Year'],
    columns='Series Name',
    values='Value',
    aggfunc='sum'
).reset_index()

# Groupby par continent
df_pivot.columns.name = None  # Supprimer l'intitulé de colonne "Series Name"
df_pivot.head()

# PROCESS DATA

df_Europe = df_pivot[df_pivot['Continent'] == 'Europe'].copy()
df_long = df_Europe.melt(id_vars='Year',value_vars=['Aquaculture production (metric tons)', 'Capture fisheries production (metric tons)'],var_name='Production Type',value_name='Value')
years = df_long['Year'].unique()
production_types = df_long['Production Type'].unique()
angles = np.linspace(0, 2 * np.pi, len(years), endpoint=False)

# PLOT NIGHTINGALE ROSE CHART
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
custom_colors = ['#0099FF', '#33FFA2'] 
for i, production_type in enumerate(production_types):
    production_data = df_long[df_long['Production Type'] == production_type]
    values = production_data.sort_values('Year')['Value'].values
    ax.bar(angles, values, width=1.2, bottom=0, color=custom_colors[i], label=production_type,  alpha=0.3)

# DESIGN
fig.patch.set_facecolor('oldlace')
ax.set_facecolor('oldlace')

# ANNOTATIONS
ax.set_title("\nTOP 10 MARINE PROTECTED AREAS IN 2018\nSGD 14", fontsize=16, fontweight='bold')
plt.figtext(0.5, 0.01, "Source: World Bank SDG | matplotlib | #30DayChartChallenge | ade yang | Day 6 – Nightingale",
            ha='center', fontsize=9, color='gray')
ax.set_title('\nAQUACULTURE VS CAPTURE FISHERIES BY YEAR IN EUROPE\nSDG 14\n', size=16)#pad=20
ax.set_xticks(angles)  
ax.set_xticklabels(years) 
ax.legend(title='Production Type', bbox_to_anchor=(0.1, 0), loc='lower center')

plt.show()

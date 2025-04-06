# IMPORT LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

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

columns_to_keep = ['Country Name', 'Country Code', 'Series Name', '2018 [YR2018]']
df_filtered = df_cleaned[columns_to_keep]

# FILTER DATA
df_filtered = df_filtered[df_filtered['Series Name'] == 'Marine protected areas (% of territorial waters)']
df_filtered = df_filtered.dropna(subset=['2018 [YR2018]'])
df_filtered['2018 [YR2018]'] = round(df_filtered['2018 [YR2018]'],2)
df_filtered = df_filtered[df_filtered['Country Name'] != 'Slovenia'] #outlier, error in dataset?
df_top_10 = df_filtered.sort_values(by='2018 [YR2018]', ascending=False).head(10)

# ISOTYPE HORIZONTAL BAR PLOT

# DATA
countries = df_top_10['Country Name']
values = df_top_10['2018 [YR2018]']
unit = 5  # 1 icône = 5%

# IMPORT ISOTYPE IMAGE
algae_img = mpimg.imread("/content/drive/MyDrive/30DayChartChallenge/datasets/blue economy/8935918_coral_diving_nature_ocean_reef_icon.png")  

# PLOT
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(-1, max(values) / unit + 3)
ax.set_ylim(-1, len(countries))

for i, (country, value) in enumerate(zip(countries, values)):
    count = int(value / unit)
    for j in range(count):
        imagebox = OffsetImage(algae_img, zoom=0.8)  
        ab = AnnotationBbox(imagebox, (j, i), frameon=False)
        ax.add_artist(ab)
    ax.text(count + 0.5, i, f"{value}%", va='center', fontsize=10)

# DESIGN
fig.patch.set_facecolor('oldlace')
ax.set_facecolor('oldlace')
ax.set_yticks(range(len(countries)))
ax.set_yticklabels(countries)
ax.set_xticks([])
ax.invert_yaxis()
for spine in ax.spines.values():
    spine.set_visible(False)

# ANNOTATIONS
ax.set_title("\nTOP 10 MARINE PROTECTED AREAS IN 2018\nSGD 14", fontsize=16, fontweight='bold')
plt.figtext(0.5, 0.01, "Source: World Bank | matplotlib | #30DayChartChallenge | ade yang | Day 5 – Ranking",
            ha='center', fontsize=9, color='gray')

plt.tight_layout()
plt.show()



import pandas as pd
import matplotlib.pyplot as plt

gdp_world_bank_csv = "data/world_bank_GDP.csv"
lookup_csv = "data/continent_to_country_lookup.csv"

gdp_df = pd.read_csv(gdp_world_bank_csv)
lookup_df = pd.read_csv(lookup_csv)

# Preparing the data
gdp_df.drop(['Country Code', 'Indicator Name', 'Indicator Code'], axis=1, inplace=True)
gdp_df.rename(columns={"Country Name": "Country_Name"}, inplace=True)

gdp_df = pd.merge(gdp_df, lookup_df, on="Country_Name")

gdp_df.drop(['Country_Name'], axis=1, inplace=True)

gdp_df = gdp_df.groupby('Continent_Name').sum()
gdp_df = gdp_df.T

# Converting to percentage out of 100
gdp_100_df = gdp_df.div(gdp_df.sum(axis=1), axis=0)


# Making the chart
bottom_list = []

for i in gdp_100_df.columns:
    b = list(gdp_100_df.loc[:, gdp_df.columns[0]: i].sum(axis=1))
    bottom_list.append(b)

fig, ax = plt.subplots()

x_ax = gdp_100_df.index

for i, v in enumerate(gdp_100_df.columns):
    if i == 0:
        # First column is at bottom of chart (so is 0 and doesn't need to be specified).
        plt.bar(x_ax, gdp_100_df[v])
    else:
        plt.bar(x_ax, gdp_100_df[v], bottom=bottom_list[i - 1])

# y-axis formatting
y_vals = ax.get_yticks()
ax.set_yticklabels(['{:.0%}'.format(y) for y in y_vals])

# x-axis formatting
n = 5  # Keeps every nth label
[l.set_visible(False) for (i, l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]

# Other formatting
plt.legend(labels=gdp_100_df.columns)
plt.title('Distribution of GDP by continent over time')

plt.show()

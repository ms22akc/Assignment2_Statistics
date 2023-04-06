import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def read_data(file):
    # Read the data from the file into a pandas dataframe
    df = pd.read_csv(file, header=1, skiprows=range(3))

    # Add an extra index column to the dataframe
    df.insert(0, 'Index', range(1, len(df)+1))

    # Write the modified dataframe to a new CSV file
    df.to_csv('C:/Users/samre/Downloads/New folder (2)/New folder/climate data.csv', index=False)

    # Transpose the dataframe so that years are columns and countries are rows
    df_transposed = df.transpose()

    # Assign the correct column names
    df_transposed.columns = df_transposed.iloc[0]
    df_transposed = df_transposed.iloc[1:]

    # Drop any rows with missing data and drop the 'Indicator Code' column
    df_transposed.dropna(inplace=True)
    if 'Indicator Code' in df_transposed.columns:
        df_transposed.drop('Indicator Code', axis=1, inplace=True)

    # Separate the dataframes into one with years as columns and one with countries as columns
    df_by_years = df_transposed.copy()
    df_by_years.columns = pd.to_numeric(df_by_years.columns, errors='coerce')
    df_by_years.dropna(axis=1, inplace=True)
    df_by_countries = df_transposed.transpose()

    return df_by_years, df_by_countries

# Calculate summary
def calculate_summary(df_by_countries, countries, indicators, year_cols):
    # Use loc to select the rows that meet the conditions
    selected_cols = ['Country Name', 'Indicator Name'] + year_cols
    selected_rows = df_by_countries.loc[(df_by_countries['Country Name'].isin(countries)) & 
                                     (df_by_countries['Indicator Name'].isin(indicators)), selected_cols]

    selected_rows.fillna(selected_rows.mean(), inplace=True)

    # Calculate summary statistics for the selected countries and indicators
    summary_stats = selected_rows.groupby(['Country Name', 'Indicator Name'])[year_cols].agg(['mean', 'median', 'std'])

    return summary_stats

# Bar chart Total greenhouse gas emissions (kt of CO2 equivalent)
def plot_bar_chart(df, countries, indicator, year_cols):
    # Use loc to select the rows that meet the conditions
    selected_cols = ['Country Name', 'Indicator Name'] + year_cols
    selected_rows = df.loc[(df['Country Name'].isin(countries)) & 
                           (df['Indicator Name'] == indicator), selected_cols]

    # Fill in missing values with 0
    selected_numeric_cols = year_cols
    selected_rows[selected_numeric_cols] = selected_rows[selected_numeric_cols].fillna(0)

    # Transpose the selected rows to make the years the columns and the countries the rows
    selected_transposed = selected_rows.set_index(['Country Name', 'Indicator Name']).transpose()

    # Replace the index name with 'Year'
    selected_transposed.index.name = 'Year'

    # Reset the index to turn the year columns into a regular column
    selected_transposed = selected_transposed.reset_index()

    # Melt the data to create separate columns for each country
    melted_data = pd.melt(selected_transposed, id_vars='Year', var_name='Country Name', value_name=indicator)

    # Replace long country names with abbreviations
    melted_data['Country Name'] = melted_data['Country Name'].map(country_abbr).fillna(melted_data['Country Name'])

    # Use seaborn to create a bar plot
    plt.figure(figsize=(5, 5))
    sns.barplot(x='Country Name', y=indicator, hue='Year', data=melted_data)
    plt.title(indicator, fontsize='14')
    plt.xlabel('Country', fontsize='14') 
    plt.legend(title='Year', loc='center left', bbox_to_anchor=(1, 0.5), fontsize='14')
    plt.show()

    return selected_rows

# Bar chart CO2 emissions (metric tons per capita)
def plot_bar_chart1(df, countries, indicator, year_cols):
    # Use loc to select the rows that meet the conditions
    selected_cols = ['Country Name', 'Indicator Name'] + year_cols
    selected_rows = df.loc[(df['Country Name'].isin(countries)) & 
                           (df['Indicator Name'] == indicator), selected_cols]

    # Fill in missing values with 0
    selected_numeric_cols = year_cols
    selected_rows[selected_numeric_cols] = selected_rows[selected_numeric_cols].fillna(0)

    # Transpose the selected rows to make the years the columns and the countries the rows
    selected_transposed = selected_rows.set_index(['Country Name', 'Indicator Name']).transpose()

    # Replace the index name with 'Year'
    selected_transposed.index.name = 'Year'

    # Reset the index to turn the year columns into a regular column
    selected_transposed = selected_transposed.reset_index()

    # Melt the data to create separate columns for each country
    melted_data = pd.melt(selected_transposed, id_vars='Year', var_name='Country Name', value_name=indicator)

    # Replace long country names with abbreviations
    melted_data['Country Name'] = melted_data['Country Name'].map(country_abbr).fillna(melted_data['Country Name'])

    # Use seaborn to create a bar plot
    plt.figure(figsize=(5, 5))
    sns.barplot(x='Country Name', y=indicator, hue='Year', data=melted_data)
    plt.title(indicator, fontsize='14')
    plt.xlabel('Country', fontsize='14')
    plt.ylabel(indicator, fontsize='14')
    plt.legend(title='Year', loc='center left', bbox_to_anchor=(1, 0.5), fontsize='14')
    plt.show()

    return selected_rows

# Correlation Heatmap
def plot_heatmap(df_by_countries, country, indicators, year_cols):
    # Select data for a specific country
    selected_cols = ['Indicator Name'] + year_cols
    selected_rows = df_by_countries.loc[(df_by_countries['Country Name'] == country) & 
                                         (df_by_countries['Indicator Name'].isin(indicators)), selected_cols]

    # Pivot the data to create a correlation matrix
    corr = selected_rows.pivot_table(index=None, columns='Indicator Name', values=year_cols).corr()

    # Plot a heatmap of the correlation matrix
    plt.figure(figsize=(5, 5))
    sns.heatmap(corr, cmap='YlOrRd', annot=True, vmin=-1, vmax=1)
    plt.xlabel('Indicator Name', fontsize=14)
    plt.ylabel('Indicator Name', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.title(f'Correlation between selected indicators for {country} for year 2000 t0 2005', fontsize='14')
    plt.show()
    
# Time seriesplot
def plot_time_series(df_by_countries, countries, indicator, year_cols, legend_size=14):
    # Use loc to select the rows that meet the conditions
    selected_cols = ['Country Name', 'Indicator Name'] + year_cols
    selected_rows = df_by_countries.loc[(df_by_countries['Country Name'].isin(countries)) & 
                                         (df_by_countries['Indicator Name'] == indicator), selected_cols]

    # Plot line charts to visualize trends over time for each country
    plt.figure(figsize=(5, 5))
    plt.title(f'Trends over time for {indicator} in selected countries')
    for country in countries:
        abbr = country_abbr.get(country, country) # Use the abbreviation if available, otherwise use the country name
        data = selected_rows.loc[selected_rows['Country Name'] == country, year_cols].values[0]
        plt.plot(year_cols, data, label=abbr)
    plt.xlabel('Year')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14)
    plt.show()

# Call the read_data function
df_by_years, df_by_countries = read_data('C:/Users/samre/Downloads/New folder (2)/New folder/climate data.csv')

# Select the columns with the specified countries, indicators, and years
countries = ['Africa Eastern and Southern', 'Afghanistan', 'Africa Western and Central', 'Angola', 'Albania', 'Andorra', 'Arab World', 'United Arab Emirates', 'Argentina', 'Armenia']
indicators = ['Total greenhouse gas emissions (kt of CO2 equivalent)', 'Population growth (annual %)', 'Forest area (sq. km)', 'CO2 emissions (metric tons per capita)', 'Arable land (% of land area)']
year_cols = ['2000', '2001', '2002', '2003', '2004', '2005']

# Define a dictionary of country name abbreviations
country_abbr = {'Africa Eastern and Southern': 'AFE', 'Afghanistan':'AFG', 'Africa Western and Central': 'AFW',
                'Angola': 'ANG', 'Albania': 'ALB', 'Andorra': 'AND', 'Arab World': 'ARB', 
                'United Arab Emirates': 'ARE', 'Argentina': 'ARG', 'Armenia': 'ARM'}

# Call the bar_chart function
# Call the function for Total greenhouse gas emissions and store the selected rows in a variable
selected_data = plot_bar_chart(df_by_countries, countries, 'Total greenhouse gas emissions (kt of CO2 equivalent)', year_cols)

# Call the function for CO2 emissions (metric tons per capita) and store the selected rows in a variable
selected_data = plot_bar_chart1(df_by_countries, countries, 'CO2 emissions (metric tons per capita)', year_cols)

# Use the selected_data variable to access the countries and year_cols variables
print(selected_data['Country Name'].unique()) # Output: ['Africa Eastern and Southern' 'Afghanistan' 'Africa Western and Central' 'Albania' 'Algeria' 'Andorra' 'Angola' 'Arab World' 'United Arab Emirates' 'Argentina' 'Armenia']
print(selected_data.columns[2:]) # Output: Index(['2000', '2001', '2002', '2003', '2004', '2005'], dtype='object')

# Call the plot_heatmap function
plot_heatmap(df_by_countries, 'Arab World', ['Total greenhouse gas emissions (kt of CO2 equivalent)', 'Population growth (annual %)', 'Forest area (sq. km)', 'CO2 emissions (metric tons per capita)', 'Arable land (% of land area)'], ['2000', '2001', '2002', '2003', '2004', '2005'])

# Call the plot_time_series function
plot_time_series(df_by_countries, countries, 'Population growth (annual %)', year_cols)

# Calculate summary statistics for the selected countries and indicators
summary_stats = calculate_summary(df_by_countries, countries, indicators, year_cols)
print(summary_stats)

# Save the summary file
summary_stats.to_csv('D:/New folder/summary_stats.csv')

# Create histrogram
def plot_histogram(df_by_countries, country, indicators, year_col):
    # Select data for a specific country and year
    selected_cols = ['Indicator Name'] + year_col
    selected_rows = df_by_countries.loc[(df_by_countries['Country Name'] == country) &
                                         (df_by_countries['Indicator Name'].isin(indicators)), selected_cols]

    # Melt the data to create a long format dataframe
    df_melt = selected_rows.melt(id_vars=['Indicator Name'], value_vars=year_col)
    df_melt['value'] = pd.to_numeric(df_melt['value'], errors='coerce')

    # Plot a histogram of the data
    plt.figure(figsize=(8, 4))
    sns.histplot(data=df_melt, x='value', bins=10)
    plt.title(f'Histogram of {country} for year {year_col[0]}')
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('Values', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.show()

# For selected data
country = 'Argentina'
year_col = ['2001']
indicators = ['Total greenhouse gas emissions (kt of CO2 equivalent)', 'Population growth (annual %)', 'Forest area (sq. km)', 'CO2 emissions (metric tons per capita)', 'Arable land (% of land area)']
plot_histogram(df_by_countries, country, indicators, year_col)

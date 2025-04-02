import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Function to fetch COVID-19 data from a public API
def fetch_covid_data(country):
    """
    Fetch COVID-19 data for a specific country using the disease.sh API
    """
    # Using disease.sh API which doesn't require authentication
    base_url = f"https://disease.sh/v3/covid-19/historical/{country}"
    params = {'lastdays': 30}  # Get data for the last 30 days
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Fetch data for two countries
usa_data = fetch_covid_data('usa')
uk_data = fetch_covid_data('uk')

# Process the data into pandas DataFrames
def process_covid_data(data, country_name):
    """
    Process the raw API response into a pandas DataFrame
    """
    if not data or 'timeline' not in data:
        print(f"No data available for {country_name}")
        return None
    
    cases_data = data['timeline']['cases']
    deaths_data = data['timeline']['deaths']
    
    # Convert to DataFrame
    df = pd.DataFrame({
        'Date': [datetime.strptime(date, '%m/%d/%y') for date in cases_data.keys()],
        'Cases': list(cases_data.values()),
        'Deaths': list(deaths_data.values()),
        'Country': country_name
    })
    
    return df

usa_df = process_covid_data(usa_data, 'USA')
uk_df = process_covid_data(uk_data, 'UK')

# Combine the DataFrames
if usa_df is not None and uk_df is not None:
    covid_df = pd.concat([usa_df, uk_df])
    
    # Create visualizations
    plt.figure(figsize=(14, 10))
    
    # Plot 1: COVID-19 Cases over time
    plt.subplot(2, 1, 1)
    for country, group in covid_df.groupby('Country'):
        plt.plot(group['Date'], group['Cases'], marker='o', linestyle='-', label=country)
    
    plt.title('COVID-19 Cases Comparison')
    plt.xlabel('Date')
    plt.ylabel('Total Cases')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Format the x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()  # Rotate date labels
    
    # Plot 2: COVID-19 Deaths over time
    plt.subplot(2, 1, 2)
    for country, group in covid_df.groupby('Country'):
        plt.plot(group['Date'], group['Deaths'], marker='o', linestyle='-', label=country)
    
    plt.title('COVID-19 Deaths Comparison')
    plt.xlabel('Date')
    plt.ylabel('Total Deaths')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Format the x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()  # Rotate date labels
    
    plt.tight_layout()
    plt.show()
else:
    print("Unable to create visualizations due to missing data")

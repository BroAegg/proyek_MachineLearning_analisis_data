import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
daily_rentals_df = pd.read_csv('dashboard/day.csv')
hourly_rentals_df = pd.read_csv('dashboard/hour.csv')

# Helper function to convert temperature to Celsius
def convert_temp_to_celsius(df):
    temp_max, temp_min = 39, -8
    df['temp_celsius'] = df['temp'] * (temp_max - temp_min) + temp_min
    return df

# Helper function to calculate rentals based on working day
def calculate_rentals_by_working_day(df):
    working_day_rentals = df.groupby('workingday')['cnt'].sum().reset_index()
    working_day_rentals['workingday'] = working_day_rentals['workingday'].replace({0: 'Non-Working Day', 1: 'Working Day'})
    return working_day_rentals

# Helper function to extract yearly data
def extract_yearly_data(df):
    df['year'] = pd.to_datetime(df['dteday']).dt.year
    return df

# Helper function to summarize rentals by season
def summarize_rentals_by_season(df):
    seasonal_rentals = df.groupby('season')['cnt'].sum().reset_index()
    seasonal_rentals['season'] = seasonal_rentals['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    return seasonal_rentals.sort_values(by='cnt', ascending=False)

# Streamlit app setup
st.title("Bike Sharing Analysis Dashboard")

# Sidebar configuration with interactive date filter
with st.sidebar:
    st.header("Dashboard Settings")
    st.image("logo.png", caption="Powered by Aegner Billik")
    # Date range filter
    st.subheader("Filter by Date")
    min_date = pd.to_datetime(daily_rentals_df['dteday']).min()
    max_date = pd.to_datetime(daily_rentals_df['dteday']).max()
    date_range = st.date_input(
        "Select Date Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

# Filter data based on the selected date range
filtered_data = daily_rentals_df[
    (pd.to_datetime(daily_rentals_df['dteday']) >= pd.Timestamp(date_range[0])) &
    (pd.to_datetime(daily_rentals_df['dteday']) <= pd.Timestamp(date_range[1]))
]

# Visualization: Rentals vs Temperature
st.subheader("Daily Bike Rentals vs Temperature (Filtered Data)")
filtered_temp_df = convert_temp_to_celsius(filtered_data)
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(
    x='temp_celsius', y='cnt', data=filtered_temp_df,
    ax=ax, hue='temp_celsius', palette='coolwarm', legend=False
)
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Number of Bike Rentals')
st.pyplot(fig)

# Visualization: Rentals vs Working Day
st.subheader("Daily Bike Rentals vs Working Day (Filtered Data)")
working_day_rentals_df = calculate_rentals_by_working_day(filtered_data)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='workingday', y='cnt', data=working_day_rentals_df,
    ax=ax, palette='pastel', ci=None
)
ax.set_xlabel('Day Type')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)

# Visualization: Rentals Over the Years
st.subheader("Daily Bike Rentals Over the Years (Filtered Data)")
filtered_yearly_data = extract_yearly_data(filtered_data)
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    x='dteday', y='cnt', data=filtered_yearly_data,
    hue='year', palette='tab10', ax=ax
)
ax.set_xlabel('Date')
ax.set_ylabel('Number of Rentals')
plt.xticks(rotation=45)
st.pyplot(fig)

# Visualization: Rentals vs Season
st.subheader("Daily Bike Rentals vs Season (Filtered Data)")
seasonal_rentals_df = summarize_rentals_by_season(filtered_data)
most_popular_season = seasonal_rentals_df.iloc[0]['season']
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='season', y='cnt', data=seasonal_rentals_df,
    palette=['#2E86C1' if season == most_popular_season else '#AED6F1' for season in seasonal_rentals_df['season']],
    ax=ax
)
ax.set_xlabel('Season')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)

st.caption("Copyright © Aegner Billik")
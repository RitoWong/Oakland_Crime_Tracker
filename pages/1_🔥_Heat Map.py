import pandas as pd
import streamlit as st
import folium
from folium.plugins import HeatMap
from datetime import datetime, timedelta

# Load the crime data from CSV file
@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    # Extracting latitude and longitude from the Location column
    data[['Longitude', 'Latitude']] = data['Location'].str.extract(r'POINT \((-?\d+\.\d+) (-?\d+\.\d+)\)')
    data['Latitude'] = data['Latitude'].astype(float)
    data['Longitude'] = data['Longitude'].astype(float)
    # Convert DATETIME to datetime object
    data['DATETIME'] = pd.to_datetime(data['DATETIME'], format='%m/%d/%Y %I:%M:%S %p')
    return data

def filter_data(data, days):
    # Get the current time
    now = datetime.now()
    # Calculate the time delta
    time_delta = now - timedelta(days=days)
    # Filter the data by time 
    return data[data['DATETIME'] >= time_delta]

def plot_heatmap(data):
    center_lat = data['Latitude'].mean() if not data.empty else 37.8045         # Default latitude for Oakland
    center_long = data['Longitude'].mean() if not data.empty else -122.2712     # Default longitude for Oakland
    m = folium.Map(location=[center_lat, center_long], zoom_start=11)
    if not data.empty:
        HeatMap(data[['Latitude', 'Longitude']], radius=15).add_to(m)
    from streamlit_folium import folium_static
    folium_static(m)


def main():
    st.set_page_config(page_title="Oakland Crime Tracker", page_icon="📌")
    
    st.title("Oakland Crime Heat Map🔥")

    filepath = "C:/Users/ritow/Desktop/Rito project/data.csv"  
    data = load_data(filepath)

    st.sidebar.title("Options")

    # Time frame selection
    time_frame = st.sidebar.selectbox(
        "Select the time frame:",
        options=["Past 24 hours", "Past 2 days", "Past 3 days", "Past week", "Past month"],
        index=2  # Default to "Past 3 days"
    )
    
    # Map the selection to the selected number of days
    time_frame_days = {
        "Past 24 hours": 1,
        "Past 2 days": 2,
        "Past 3 days": 3,
        "Past week": 7,
        "Past month": 30
    }

    # Filter data based on time frame selection
    filtered_data_heatmap = filter_data(data, time_frame_days[time_frame])
    
    # Plot the heat map
    plot_heatmap(filtered_data_heatmap)

if __name__ == "__main__":
    main()

# This final project is developed by Chun San Wong (Rito) for CIS 27 

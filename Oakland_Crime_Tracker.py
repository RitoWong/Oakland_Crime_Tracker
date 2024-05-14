import pandas as pd
import streamlit as st
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

def filter_data_by_description(data, description_query):
    # Filter data by different keywords
    return data[data['DESCRIPTION'].str.contains(description_query, case=False, na=False)]

def filter_data(data, days, selected_types):
    # Get the current time
    now = datetime.now()
    # Calculate the time delta
    time_delta = now - timedelta(days=days)
    # Filter the data by time and different crime types
    return data[(data['DATETIME'] >= time_delta) & (data['CRIMETYPE'].isin(selected_types))]


def display_crime_data(data):
    if not data.empty:
        # Sort data by DATETIME in descending order
        sorted_data = data.sort_values(by='DATETIME', ascending=False)
        sorted_data.reset_index(drop=True, inplace=True)
        sorted_data.index += 1
        # Display the columns that necessary
        st.dataframe(sorted_data[['DATETIME', 'DESCRIPTION', 'ADDRESS', 'CITY', 'STATE']])
    else:
        st.write("No incidents found matching the search criteria.")



def main():
    st.set_page_config(page_title="Oakland Crime Tracker", page_icon="📌")
    
    st.title("Hate Crime Incidents💥")
    
    filepath = "data.csv"
    data = load_data(filepath)
    
    st.sidebar.title("Search Options")

    # Date range selection
    start_date = st.sidebar.date_input("Start date", datetime.today() - timedelta(days=7))
    end_date = st.sidebar.date_input("End date", datetime.today())
    if start_date > end_date:
        st.sidebar.error("Error: End date must fall after start date.")

    # Allow the user input the crime type
    location_input = st.sidebar.text_input("Enter location keywords (e.g., Main St, School):")

    # Filter data based on the date range and location
    filtered_data = data[(data['DATETIME'] >= pd.Timestamp(start_date)) & (data['DATETIME'] <= pd.Timestamp(end_date))]
    if location_input:
        filtered_data = filtered_data[filtered_data['ADDRESS'].str.contains(location_input, case=False, na=False)]

    # Allow the user to input crime type
    crime_type_input = st.sidebar.text_input("Enter crime type keywords (e.g., Theft, Vehicle, Vandalism):")
    if crime_type_input:
        filtered_data = filtered_data[filtered_data['DESCRIPTION'].str.contains(crime_type_input, case=False, na=False)]

    # Display filtered data
    display_crime_data(filtered_data)



if __name__ == "__main__":
    main()

# This final project is developed by Chun San Wong (Rito) for CIS 27 

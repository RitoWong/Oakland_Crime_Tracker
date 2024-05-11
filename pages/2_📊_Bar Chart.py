import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import plotly.express as px

# Load the data
@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    # Extracting latitude and longitude from the 'Location' column
    data[['Longitude', 'Latitude']] = data['Location'].str.extract(r'POINT \((-?\d+\.\d+) (-?\d+\.\d+)\)')
    data['Latitude'] = data['Latitude'].astype(float)
    data['Longitude'] = data['Longitude'].astype(float)
    # Convert 'DATETIME' to datetime object
    data['DATETIME'] = pd.to_datetime(data['DATETIME'], format='%m/%d/%Y %I:%M:%S %p')
    return data

def filter_data(data, days, selected_types):
    # Get the current time
    now = datetime.now()
    # Calculate the time delta
    time_delta = now - timedelta(days=days)
    # Filter the data by time and crime types
    return data[(data['DATETIME'] >= time_delta) & (data['CRIMETYPE'].isin(selected_types))]

def plot_bar_chart(data):
    if not data.empty:
        crime_counts = data['CRIMETYPE'].value_counts().reset_index()
        crime_counts.columns = ['CRIMETYPE', 'count']  # Rename columns
        fig = px.bar(crime_counts, x='CRIMETYPE', y='count', 
                     labels={'CRIMETYPE': 'Crime Type', 'count': 'Frequency'}, 
                     title='Distribution of Crime Types')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available to plot the distribution.")

# Initialize the Streamlit app
def main():
    st.set_page_config(page_title="Oakland Crime Tracker", page_icon="📌")
    st.title("Crime Bar Chart📊")

    filepath = "C:/Users/ritow/Desktop/Rito project/data.csv"  # Update the file path
    data = load_data(filepath)

    st.sidebar.title("Options")

    # Time frame selection in the sidebar
    time_frame = st.sidebar.selectbox(
        "Select the time frame:",
        options=["Past 3 days", "Past week", "Past month"],
        index=1  # Default to "Past 2 days"
    )
    
    # Map the selection to the corresponding number of days
    time_frame_days = {
        "Past 3 days": 3,
        "Past week": 7,
        "Past month": 30
    }

    # Expander for selecting crime types for bar chart
    crime_types_bar_chart = data['CRIMETYPE'].unique().tolist()
    with st.sidebar.expander("Select crime types for Bar Chart:"):
        all_bar_chart = st.checkbox("Select all", value=True, key="all_bar_chart")
        if all_bar_chart:
            selected_crime_types_bar_chart = crime_types_bar_chart
        else:
            selected_crime_types_bar_chart = st.multiselect('', crime_types_bar_chart, default=crime_types_bar_chart)

    # Filter data based on selection for bar chart
    filtered_data_bar_chart = filter_data(data, time_frame_days[time_frame], selected_crime_types_bar_chart)
    
    # Plot bar chart
    plot_bar_chart(filtered_data_bar_chart)

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import openrouteservice
from shapely.geometry import Point, LineString
import geopandas as gpd
import datetime
import os

# Load the crime data from CSV file
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')
    df['lon'] = df['Location'].apply(lambda x: float(x.split()[1].strip('(')))
    df['lat'] = df['Location'].apply(lambda x: float(x.split()[2].strip(')')))
    df['geometry'] = df.apply(lambda x: Point(x['lon'], x['lat']), axis=1)
    df['DATETIME'] = pd.to_datetime(df['DATETIME'], format='%m/%d/%Y %I:%M:%S %p')
    return gpd.GeoDataFrame(df, geometry='geometry')

def parse_coordinates(coords):
    try:
        lat, lon = coords.split(',')
        return float(lat.strip()), float(lon.strip())
    except ValueError:
        st.error('Invalid coordinate format. Please use the format: lat,lon')
        return None, None

def save_map(map, filename='map.html'):
    map.save(filename)
    return filename

@st.cache_resource
def get_route(start_coords, end_coords, _client):
    start_lat, start_lon = start_coords
    end_lat, end_lon = end_coords
    coords = [[start_lon, start_lat], [end_lon, end_lat]]
    return _client.directions(coordinates=coords, profile='driving-car', format='geojson')

def main():
    st.set_page_config(page_title="Oakland Crime Tracker", page_icon="📌")
    st.title("City Navigation and Crime Map🛣")
    st.write('Explore the city, find routes, and view crime hotspots using coordinates.')
    client = openrouteservice.Client(key='5b3ce3597851110001cf624825b44055c4344562b3a21df58da89bbd')

    # Input fields for start and end locations
    start_coords = st.text_input('Enter start location (format: lat,lon):')
    end_coords = st.text_input('Enter end location (format: lat,lon):')

    if st.button('Start'):
        st.session_state['start_coords'] = start_coords
        st.session_state['end_coords'] = end_coords

    if 'start_coords' in st.session_state and 'end_coords' in st.session_state:
        start_coords = parse_coordinates(st.session_state['start_coords'])
        end_coords = parse_coordinates(st.session_state['end_coords'])

        if start_coords and end_coords:
            try:
                route = get_route(start_coords, end_coords, client)
                folium_map = folium.Map(location=[start_coords[0], start_coords[1]], zoom_start=12)

                # Add markers for the start and end locations
                folium.Marker([start_coords[0], start_coords[1]], tooltip='Start Location',
                              icon=folium.Icon(color='blue', icon='play')).add_to(folium_map)
                folium.Marker([end_coords[0], end_coords[1]], tooltip='End Location',
                              icon=folium.Icon(color='blue', icon='flag')).add_to(folium_map)
                folium.GeoJson(route, name='route').add_to(folium_map)

                route_line = LineString([tuple(coord) for coord in route['features'][0]['geometry']['coordinates']])
                folium_map.fit_bounds([[route_line.bounds[1], route_line.bounds[0]], [route_line.bounds[3], route_line.bounds[2]]])

                # Load recent crime data
                gdf = load_data()
                current_date = datetime.datetime.now()
                fourteen_days_ago = current_date - datetime.timedelta(days=14)
                gdf = gdf[gdf['DATETIME'] >= fourteen_days_ago]
                gdf['distance'] = gdf.apply(lambda row: route_line.distance(row['geometry']), axis=1)
                gdf_filtered = gdf[gdf['distance'] <= 50]

                # Add crime data markers to the map
                for index, crime in gdf_filtered.iterrows():
                    folium.Marker(
                        [crime.geometry.y, crime.geometry.x],
                        popup=f"Crime Type: {crime['CRIMETYPE']}<br>Description: {crime['DESCRIPTION']}<br>Date/Time: {crime['DATETIME']}",
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(folium_map)

                folium_display = st_folium(folium_map, width=725, height=500)

                # Allow the user to download the screenshot
                html_path = save_map(folium_map)
                with open(html_path, "rb") as file:
                    st.download_button(
                        label="Download Map as HTML",
                        data=file,
                        file_name="map.html",
                        mime="text/html"
                    )

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

# This final project is developed by Chun San Wong (Rito) for CIS 27 

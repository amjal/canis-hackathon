import streamlit as st
import pandas as pd
import os
import json
from geopy.geocoders import Nominatim
import geopandas as gpd
from shapely.geometry import Point
import threading
from collections import Counter
import pydeck as pdk


class Agent:
	def __init__(self, users_dir, following_dir):
		self.users_dir = users_dir	
		self.following_dir = following_dir

	def cities2coords_cached(self, cities, coord_file):
		coords = []
		with open(coord_file, 'r') as f: 
			coord_data = json.load(f)
		for city in cities:
			try:
				coords.append(coord_data[city])
			except:
				pass
		return coords

	def cities2coords(self, cities, results=None):
		coord_list = {}
		geolocator = Nominatim(user_agent="follower-canis-hackathon")
		count =0
		for city in cities:
			count +=1 
			print(city + " " + str(count) + "/" + str(len(cities)))
			if len(city):
				try:
					location = geolocator.geocode(city)
					if location:
						coord_list[city] = (location.latitude, location.longitude)
				except Exception:
					print("Caught Exception")
		if results == None:
			return coord_list
		else:
		  	results = results.extend(coord_list)

	def users2cities(self):
		cities = []
		for filename in os.listdir(self.users_dir):
			if filename.endswith('.json') and filename != "coords.json":
				file_path = os.path.join(self.users_dir, filename)
				with open(file_path, 'r') as file:
					data = json.load(file)
					city = data["data"]["user"]["result"]["legacy"]["location"]
					if len(city):
						cities.append(city)
		return cities
	
	def following2cities(self):
		cities = []
		for filename in os.listdir(self.following_dir):
			if filename.endswith('.json'):
				file_path = os.path.join(self.following_dir, filename)
				with open(file_path, 'r') as file: 
					print(file_path)
					data = json.load(file)
					try:
						for entry in data['data']['user']['result']['timeline']['timeline']['instructions']:
							if entry['type'] == "TimelineAddEntries":
								for user in entry['entries']:
									try:
										cities.append(user['content']['itemContent']['user_results']['result']['legacy']['location'])
									except KeyError:
										pass
					except KeyError:
						 pass

		return cities
	
	def coords2country_counts(self, **kwargs):
		for key, value in kwargs.items():
			if key == "file":
				coords_file = value
				with open(coords_file, 'r') as f: 
					coords = json.load(f)	
			elif key == "array":
			  	coords = value
		coords = [tuple(item) for item in coords]
		gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lat, lon in coords])
		world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
		gdf = gpd.sjoin(gdf, world, how="inner", op='intersects')
		country_counts = gdf['name'].value_counts()
		return country_counts


	def generate_pointmap(self, **kwargs):
		for key, value in kwargs.items():
			if key == "file": 
				with open(value, 'r') as f:
					coords = json.load(f)
					coords = [tuple(item) for item in coords]
			elif key == "array":
				coords = value
		df = pd.DataFrame(coords, columns=['lat', 'lon'])
		return df
	
	def generate_heatmap(self, df):
		# Define the layer for pydeck
		layer = pdk.Layer(
			"HeatmapLayer",
			df,
			get_position=['lon', 'lat'],
			radius_pixels=60,
			opacity=0.9,
			get_weight=1  # Assuming each point has equal weight
		)

		# Set the initial view state for pydeck
		view_state = pdk.ViewState(
			latitude=0,  # Central latitude, adjust as needed
			longitude=0,  # Central longitude, adjust as needed
			zoom=1,
			pitch=0
		)

		# Render the deck.gl map in Streamlit
		r = pdk.Deck(layers=[layer], initial_view_state=view_state)
		return r
	
	def generate_heatmap_by_country(self, geojson_filename, locs):
		with open(geojson_filename, 'r') as f: 
			countries_geojson = json.load(f)
		country_counts = self.coords2country_counts(array=locs)
		country_counts = country_counts.reset_index()
		country_counts.columns = ['name', 'count']
		min_value = country_counts['count'].min()
		max_value = country_counts['count'].max()

		def normalize(value):
			return (value - min_value) / (max_value - min_value) if max_value > min_value else 0

		def value_to_color(value):
			red = 255
			green = blue = int (255 * (1 -value)**3)
			return [red, green, blue, 255]  # RGBA format, producing shades from white to dark red

		country_counts['color'] = country_counts['count'].apply(lambda x: value_to_color(normalize(x)))
		def get_color(country_name):
			selected_row = country_counts[country_counts['name'] == country_name]
			if not selected_row.empty:
				return selected_row['color'].iloc[0]
			else: 
				return [255, 255, 255, 255]


		for feature in countries_geojson['features']:
			country_name = feature['properties']['name']
			feature['properties']['color'] = get_color(country_name)

		layer = pdk.Layer(
			"GeoJsonLayer",
			countries_geojson,
			get_fill_color="properties.color",
			pickable=True
		)
		view_state = pdk.ViewState(latitude=0, longitude=0, zoom=1)
		r = pdk.Deck(layers=[layer], initial_view_state=view_state)
		return r

if __name__ == "__main__":
	agent = Agent("../twitter/users/")
	'''
	gdf = agent.coords2country_counts("../twitter/users/coords.json")
	agent.generate_heatmap(gdf)
	'''
	'''
	cities = agent.users2cities()
	uniq_cities = Counter(cities)
#uniq_cities = {item: count for item, count in uniq_cities.items() if count > 4}

	coords = agent.cities2coords(list(uniq_cities.keys()))
	with open('../twitter/loc2coord-3.json', 'w') as f:
		json.dump(coords, f)
	'''
	'''
	cities = agent.get_cities()
	coords = agent.convert2coords(cities)
	with open('../twitter/users/coords.json', 'w') as f: 
		json.dump(coords, f)
	'''

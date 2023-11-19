import streamlit as st
import pandas as pd
import os
import json
from geopy.geocoders import Nominatim


class Agent:
	def __init__(self, users_dir):
		self.users_dir = users_dir	

	def convert2coords(self, cities):
		coord_list = []
		geolocator = Nominatim(user_agent="canis-hackathon-amjal")
		for city in cities:
			print(city)
			try:
				location = geolocator.geocode(city)
				if location:
					coord_list.append((location.latitude, location.longitude))
			except Exception:
				print("Caught Exception")
		return coord_list

	def get_cities(self):
		cities = []
		for filename in os.listdir(self.users_dir):
			if filename.endswith('.json'):
				file_path = os.path.join(self.users_dir, filename)
				with open(file_path, 'r') as file:
					data = json.load(file)
					city = data["data"]["user"]["result"]["legacy"]["location"]
					if len(city):
						cities.append(city)
		return cities

	def create_map(self, **kwargs):
		for key, value in kwargs.items():
			if key == "file": 
				with open(value, 'r') as f:
					coords = json.load(f)
					coords = [tuple(item) for item in coords]
			elif key == "array":
				coords = value
		df = pd.DataFrame(coords, columns=['lat', 'lon'])
		return df

if __name__ == "__main__":
	agent = Agent("../twitter/users/")
	'''
	cities = agent.get_cities()
	coords = agent.convert2coords(cities)
	with open('../twitter/users/coords.json', 'w') as f: 
		json.dump(coords, f)
	'''
	print(agent.create_map(file="../twitter/users/coords.json"))

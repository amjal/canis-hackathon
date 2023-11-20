import sys
sys.path.append('../python_scripts')
import PlotlyAgent
import WorldMapAgent
import WikiGraph
import streamlit as st
from python_scripts import TwitterContent
import pandas as pd
import plotly.graph_objects as go
import FollowGraph

# Streamlit app layout
st.title("Streamlit App with Plotly Plot")

# Sidebar navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
	"Choose a page:",
	("Home", "Twitter Content Analysis", "Plotly Plot", "Wiki Network Graph", "Geo Map", "Following Graph")
)


# Page content based on navigation
if option == "Home":
	st.write("Welcome to the Home Page")
elif option == "Twitter Content Analysis":
	time_series_agent = TwitterContent.Agent()
	fig = time_series_agent.show_hashtags_plot()
	st.plotly_chart(fig)
	fig = time_series_agent.show_hashtags_trend()
	st.plotly_chart(fig)
	fig = time_series_agent.show_topics_trend()
	st.plotly_chart(fig)
	fig = time_series_agent.show_topics_per_parent()
	st.plotly_chart(fig)
	fig = time_series_agent.show_most_impactful_topics()
	st.plotly_chart(fig)
elif option == "Plotly Plot":
	st.write("Plotly Plot")
	plotly_agent = PlotlyAgent.Agent()
	# Call the function to create and display the Plotly plot
	fig = plotly_agent.plot_3d_heat('Entity owner (English)', 'Region of Focus', 10)
	st.plotly_chart(fig)
elif option == "Wiki Network Graph":
	st.write("Wiki Network Graph")
	networx_agent = WikiGraph.Agent()
	graph = networx_agent.plot_network_graph()
	st.components.v1.html(graph, height=800, width=800, scrolling=True)
elif option == "Geo Map":
	geo_agent = WorldMapAgent.Agent("../twitter/users/")
	locs = geo_agent.generate_pointmap(file="../twitter/users/coords.json")
	st.map(locs)
	country_counts = geo_agent.coords2country_counts("../twitter/users/coords.json")
#r = geo_agent.generate_heatmap(locs)
	r = geo_agent.generate_heatmap_by_country("../data/custom.geo.json", country_counts)
	st.pydeck_chart(r)
elif option == "Following Graph":
	agent = FollowGraph.Agent()
	st.write("Following Graph")
	df = pd.read_csv('../3d-network-visualization/clean_csvs/network.csv')
	user_parent_entity = st.multiselect('select user parent entity', df['user_parent_entity'].unique())
	following_parent_entity = st.multiselect('Select following parent entity', df['following_parent_entity'].unique())
	fig = agent.plot_network_graph(user_parent_entity, following_parent_entity)
	st.plotly_chart(fig, use_container_width=True)


	

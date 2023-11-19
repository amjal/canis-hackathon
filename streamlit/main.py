import sys
sys.path.append('../python_scripts')
import PlotlyAgent
import WorldMapAgent
import WikiGraph
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Streamlit app layout
st.title("Streamlit App with Plotly Plot")

# Sidebar navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
	"Choose a page:",
	("Home", "Plotly Plot", "Wiki Network Graph", "Geo Map")
)


# Page content based on navigation
if option == "Home":
	st.write("Welcome to the Home Page")
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

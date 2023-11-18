import sys
sys.path.append('../python_scripts/')
import PlotlyAgent
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Streamlit app layout
st.title("Streamlit App with Plotly Plot")

# Sidebar navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
	"Choose a page:",
	("Home", "Plotly Plot", "Another Page")
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
elif option == "Another Page":
	st.write("Welcome to Another Page")


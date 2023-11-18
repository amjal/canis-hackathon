import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to create the Plotly plot
def create_plotly_plot():
	df = pd.read_excel('../data/CANIS_PRC_state_media_on_social_media_platforms-2023-11-03.xlsx')
# Identify the top 10 entity owners and regions of focus
	top_entity_owners = df['Entity owner (English)'].value_counts().nlargest(10).index
	top_regions_of_focus = df['Region of Focus'].value_counts().nlargest(10).index
# Filter the dataset
	filtered_data = df[df['Entity owner (English)'].isin(top_entity_owners) & df['Region of Focus'].isin(top_regions_of_focus)]
# Group by 'Entity owner (English)' and 'Region of Focus', count the number of entities
	grouped_data = filtered_data.groupby(['Entity owner (English)', 'Region of Focus']).size().reset_index(name='Entity Count')
# Custom color scale (black to red)
	color_scale = [[0, 'black'], [1, 'red']]
# Creating the 3D plot
	fig = go.Figure()
# Add the scatter points
	fig.add_trace(go.Scatter3d(
		x=grouped_data['Entity owner (English)'],
		y=grouped_data['Region of Focus'],
		z=grouped_data['Entity Count'],
		mode='markers',
		marker=dict(
			size=5,
			color=grouped_data['Entity Count'],  # set color based on the Entity Count
			colorscale=color_scale,  # use the custom color scale
			opacity=0.8
		)
	))
# Add lines to the XY plane
	for i in range(len(grouped_data)):
		fig.add_trace(go.Scatter3d(
			x=[grouped_data['Entity owner (English)'][i], grouped_data['Entity owner (English)'][i]],
			y=[grouped_data['Region of Focus'][i], grouped_data['Region of Focus'][i]],
			z=[0, grouped_data['Entity Count'][i]],
			mode='lines',
			line=dict(color='gray', width=4, dash='dash'),  # Increased line width
			showlegend=False
		))
# Customizing the axis
	fig.update_layout(
		scene=dict(
			xaxis=dict(
#title='Entity Owner (English)',
				tickmode='array',
				tickvals=list(range(10)),
				ticktext=top_entity_owners.to_list(),
#tickangle=-45
			),
			yaxis=dict(
#title='Region of Focus',
				tickmode='array',
				tickvals=list(range(10)),
				ticktext=top_regions_of_focus.to_list(),
#tickangle=-45
			),
			zaxis=dict(
				title='Number of Entities'
			)
		),
		margin=dict(r=0, l=0, b=0, t=0)
	)
	return fig

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
	# Call the function to create and display the Plotly plot
	fig = create_plotly_plot()
	st.plotly_chart(fig)
elif option == "Another Page":
	st.write("Welcome to Another Page")


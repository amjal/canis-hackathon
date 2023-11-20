import pandas as pd
import plotly.graph_objects as go

class Agent:
	def __init__(self):
		self.df = pd.read_excel('../data/CANIS_PRC_state_media_on_social_media_platforms-2023-11-03.xlsx')
	def plot_3d_heat(self, x_axis_column, y_axis_column, num_data):
		top_entity_owners = self.df[x_axis_column].value_counts().nlargest(num_data).index
		top_regions_of_focus = self.df[y_axis_column].value_counts().nlargest(num_data).index
		filtered_data = self.df[self.df[x_axis_column].isin(top_entity_owners) & self.df[y_axis_column].isin(top_regions_of_focus)]
		grouped_data = filtered_data.groupby([x_axis_column, y_axis_column]).size().reset_index(name='Entity Count')
		color_scale = [[0, 'black'], [1, 'red']]
		fig = go.Figure()

		# Add the scatter points
		fig.add_trace(go.Scatter3d(
			x=grouped_data[x_axis_column],
			y=grouped_data[y_axis_column],
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
				x=[grouped_data[x_axis_column][i], grouped_data[x_axis_column][i]],
				y=[grouped_data[y_axis_column][i], grouped_data[y_axis_column][i]],
				z=[0, grouped_data['Entity Count'][i]],
				mode='lines',
				line=dict(color='white', width=20, dash='dash'),  # Increased line width
				showlegend=False
			))

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
		fig.update_layout(width = 1200, height = 1000)
		return fig

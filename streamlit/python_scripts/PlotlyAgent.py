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
        
        # Use a diverging color scale for better visual differentiation
        color_scale = 'Viridis'

        fig = go.Figure()

        # Add the scatter points with hover text
        fig.add_trace(go.Scatter3d(
            x=grouped_data[x_axis_column],
            y=grouped_data[y_axis_column],
            z=grouped_data['Entity Count'],
            mode='markers+text',
            marker=dict(
                size=7,
                color=grouped_data['Entity Count'] * 10,  # set color based on the Entity Count
                colorscale=color_scale,  # use a built-in color scale
                opacity=0.8
            ),
            text=grouped_data['Entity Count'],  # hover text goes here
            hoverinfo='text+x+y'
        ))

        # Modify lines to not overshadow points
        for i in range(len(grouped_data)):
            fig.add_trace(go.Scatter3d(
                x=[grouped_data[x_axis_column][i], grouped_data[x_axis_column][i]],
                y=[grouped_data[y_axis_column][i], grouped_data[y_axis_column][i]],
                z=[0, grouped_data['Entity Count'][i]],
                mode='lines',
                line=dict(color='grey', width=2),  # Adjust line properties
                showlegend=False
            ))

        # Update layout for improved readability
        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    # title=x_axis_column.replace('_', ' ').title(),
					title='',
                    tickvals=list(range(num_data)),
                    ticktext=top_entity_owners.to_list(),
                ),
                yaxis=dict(
                    # title=y_axis_column.replace('_', ' ').title(),
					title='',
                    tickvals=list(range(num_data)),
                    ticktext=top_regions_of_focus.to_list(),
                ),
                zaxis=dict(
                    title='Number of Entities'
                ),
                # Adjust camera angle for better perspective
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=0.5)
                )
            ),
            margin=dict(r=0, l=0, b=0, t=0)
        )

        fig.update_layout(width=1200, height=1000)

        # Add titles and improve font
        fig.update_layout(
            title={
                'text': "3D Heat Map of Entity Count",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="#7f7f7f"
            )
        )

        return fig

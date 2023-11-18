import pandas as pd
import plotly.graph_objects as go

# Load the data
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

# Add simulated bars as lines
for i, row in grouped_data.iterrows():
    fig.add_trace(go.Scatter3d(
        x=[row['Entity owner (English)'], row['Entity owner (English)']],
        y=[row['Region of Focus'], row['Region of Focus']],
        z=[0, row['Entity Count']],
        mode='lines',
        line=dict(
            color=row['Entity Count'],
            colorscale=color_scale,
            width=10  # Adjust line width to mimic bar width
        )
    ))

# Customizing the axis
fig.update_layout(
    scene=dict(
        xaxis=dict(
            title='Entity Owner (English)',
            tickmode='array',
            tickvals=list(range(10)),
            ticktext=top_entity_owners.to_list(),
            tickangle=-45
        ),
        yaxis=dict(
            title='Region of Focus',
            tickmode='array',
            tickvals=list(range(10)),
            ticktext=top_regions_of_focus.to_list(),
            tickangle=-45
        ),
        zaxis=dict(
            title='Number of Entities'
        )
    ),
    margin=dict(r=0, l=0, b=0, t=0)
)

# Show plot
fig.show()


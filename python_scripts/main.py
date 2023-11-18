import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# Load the data
df = pd.read_excel('../data/CANIS_PRC_state_media_on_social_media_platforms-2023-11-03.xlsx')

# Identify the top 10 entity owners and regions of focus
top_entity_owners = df['Entity owner (English)'].value_counts().nlargest(10).index
top_regions_of_focus = df['Region of Focus'].value_counts().nlargest(10).index

# Filter the dataset
filtered_data = df[df['Entity owner (English)'].isin(top_entity_owners) & df['Region of Focus'].isin(top_regions_of_focus)]

# Group by 'Entity owner (English)' and 'Region of Focus', count the number of entities
grouped_data = filtered_data.groupby(['Entity owner (English)', 'Region of Focus']).size().reset_index(name='Entity Count')

# Creating the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extracting the data for plotting
x = grouped_data['Entity owner (English)']
y = grouped_data['Region of Focus']
z = grouped_data['Entity Count']

# Mapping each entity owner and region of focus to a numerical value for plotting
x_labels = x.unique()
x_to_num = {p:i for i, p in enumerate(x_labels)}
y_labels = y.unique()
y_to_num = {p:i for i, p in enumerate(y_labels)}

# Plotting with a colormap
scatter = ax.scatter(x.map(x_to_num), y.map(y_to_num), z, c=z, cmap=cm.hot)

# Drawing dashed lines to the XY plane
for i in range(len(x)):
    ax.plot([x.map(x_to_num)[i], x.map(x_to_num)[i]], [y.map(y_to_num)[i], y.map(y_to_num)[i]], [0, z[i]], 'gray', linestyle='dashed', linewidth=0.5)

# Setting labels
#ax.set_xlabel('Entity Owner (English)')
#ax.set_ylabel('Region of Focus')
ax.set_zlabel('Number of Entities')
ax.set_xticks(range(len(x_labels)))
ax.set_xticklabels(x_labels, rotation=90)
ax.set_yticks(range(len(y_labels)))
ax.set_yticklabels(y_labels)

# Adding a color bar
cbar = fig.colorbar(scatter, ax=ax, extend='max')
cbar.set_label('Number of Entities')

# Show plot
plt.show()


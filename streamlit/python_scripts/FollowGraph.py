import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import random


class Agent:
    def get_pleasing_random_color(self):
        pleasing_colors = [
            '#FF5733',  # Vibrant Red
            '#33FF57',  # Vivid Green
            '#3357FF',  # Bright Blue
            '#FF33FF',  # Magenta
            '#FFFF33',  # Yellow
            '#33FFFF',  # Cyan
            '#FF7F50',  # Coral
            '#9370DB',  # Medium Purple
            '#3CB371',  # Medium Sea Green
            '#FFD700',  # Gold
            '#FF69B4',  # Hot Pink
            '#87CEEB',  # Sky Blue
            '#FF6347',  # Tomato
            '#40E0D0',  # Turquoise
            '#EE82EE',  # Violet
            '#DA70D6',  # Orchid
            '#6495ED',  # Cornflower Blue
            '#FFB6C1',  # Light Pink
            '#BC8F8F',  # Rosy Brown
            '#F08080',  # Light Coral
            '#7B68EE',  # Medium Slate Blue
            '#6B8E23',  # Olive Drab
        ]

        return random.choice(pleasing_colors)

    def plot_network_graph(self, user_parent_entity, following_parent_entity):
        df = pd.read_csv('../3d-network-visualization/clean_csvs/network.csv')
        df = df[df['user_parent_entity'].isin(user_parent_entity) & df['following_parent_entity'].isin(
            following_parent_entity)]

        if df.shape[0] == 0:
            return go.Figure()

        G = nx.from_pandas_edgelist(df, 'user', 'following', create_using=nx.DiGraph())

        pos = nx.spring_layout(G, iterations=10)

        parent_entity_color_map = {entity: self.get_pleasing_random_color() for entity in
                                   set(df['user_parent_entity'].unique()).union(
                                       set(df['following_parent_entity'].unique()))}

        node_in_degree = dict(G.in_degree())
        max_in_degree = max(node_in_degree.values())
        node_size = [10 + 10 * (node_in_degree[node] / max_in_degree) for node in
                     G.nodes()]
        

        edge_x, edge_y = [], []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.2, color='#888'), mode='lines', hoverinfo='none')

        node_x, node_y, node_color, node_text = [], [], [], []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

            is_start_node = G.in_degree(node) == 0 and G.out_degree(node) > 0

            node_info = df[(df['user'] == node) | (df['following'] == node)].iloc[0]
            parent_entity = node_info['user_parent_entity'] if is_start_node else node_info['following_parent_entity']
            node_color.append(parent_entity_color_map[parent_entity])

            node_text.append(f'{node}, Parent Entity: {parent_entity}')

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                size=node_size,
                color=node_color,
                line_width=2))

        node_trace.text = node_text

        fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
            title='<br>Network graph made with Python',
            titlefont_size=16,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        ))

        return fig

import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import os
import tempfile
import matplotlib.pyplot as plt
import matplotlib

class Agent:
    def plot_network_graph(self):
        # Sample DataFrame
        df = pd.read_csv('data/wiki_category_network.csv')

        # Initialize a directed graph
        G = nx.from_pandas_edgelist(df, 'title', 'category', create_using=nx.DiGraph())

        # Streamlit app
        st.title("Network Graph Visualization")

        # Create a directed Pyvis network graph
        net = Network(height='500px', width='100%', bgcolor='#222222', font_color='white', directed=True)

        def get_node_color(out_degree, max_degree):
            # Normalize the out_degree value
            normalized_degree = out_degree / max_degree
            # Use a colormap to generate colors
            color = plt.cm.coolwarm(normalized_degree)  # You can choose any available colormap
            # Convert matplotlib color to hex format
            return matplotlib.colors.rgb2hex(color)

        max_degree = max(G.out_degree(node) for node in G.nodes)

        def get_node_size(degree):
            base_size = 10  # Base size for all nodes
            size_increment = 1000  # Increment per degree
            return base_size + size_increment * degree

        # Add nodes and edges with specific colors for nodes based on their out-degree
        for node in G.nodes:
            in_degree = G.in_degree(node)
            node_color = get_node_color(in_degree, max_degree)
            node_size = get_node_size(in_degree)
            net.add_node(node, title=node, color=node_color)

        for edge in G.edges:
            net.add_edge(edge[0], edge[1])

        # Generate and save the network graph to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            net.save_graph(tmpfile.name)
            html_file = tmpfile.name

        # Read the HTML file
        html_string = ''
        with open(html_file, 'r', encoding='utf-8') as f:
            html_string = f.read()

        # Remove the temporary file
        os.unlink(html_file)

        # Display the HTML using st.components.v1.html
        return html_string
    

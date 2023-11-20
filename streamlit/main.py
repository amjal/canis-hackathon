import sys

import pandas as pd

import streamlit as st
from python_scripts import TwitterContent, CanisContent, FollowGraph, PlotlyAgent, WorldMapAgent, WikiGraph, semantic

# Streamlit app layout
st.set_page_config(layout="wide")
st.title("📊 CANIS DataViz Challenge | Hackathon 2023")

tab_home, tab_canis, tab_twitter_content, tab_network = st.tabs(
    ["🏠 Home", "📊 Canis Data Analysis", "🐦 Twitter Content Analysis", "🌐 Following Graph"]
)

# Page content based on navigation
with tab_home:
    # Homepage title
    st.title("🔍 CANIS DataViz Hackathon Project by Team Insightful Four")

    # Brief Introduction
    st.markdown("""
    Welcome to our project dashboard! We're Team Insightful Four, comprised of Alireza, Morteza, Amir, and Mohammad Reza, 
    bringing together our diverse skills to tackle the CANIS Data Visualization Challenge. 🚀
    """)

    # About the Challenge
    st.header("🎯 About Our Challenge")
    st.markdown("""
    Diving deep into data, our mission was to transform a raw dataset into a captivating visual narrative. 
    We began by dissecting the CANIS data, seeking patterns and stories hidden within. Our journey took a 
    twist as we embarked on scraping Twitter, gleaning insights from the web of interactions and content 
    created by the users provided to us.
    """)

    # Our Process
    st.header("🔬 Our Analytical Process")
    st.markdown("""
    Our approach was systematic and exploratory:
    - **Data Analysis**: Initiated with a thorough analysis of CANIS data.
    - **Twitter Scraping**: Progressed to scraping Twitter for user profiles, their networks, and recent tweets.
    - **Insight Extraction**: Delved into the data to uncover trends, anomalies, and noteworthy findings.
    - **Visualization**: Transformed our discoveries into an array of engaging, insightful visuals.
    """)

    # Submission Requirements
    st.header("📑 Submission Highlights")
    st.markdown("""
    In our submission, you'll find:
    - **Structured Presentation**: A cohesive narrative of our data journey, from raw figures to polished graphs.
    - **Methodology Summary**: Insight into the analytical tools and techniques we employed.
    - **Codebase**: Access to the code that powered our analysis, showcasing our technical acumen.
    """)

    # Final Thoughts
    st.header("💡 Parting Thoughts")
    st.markdown("""
    Whether you're a data enthusiast, a visualization whiz, or just curious about the power of data, we invite you to 
    explore our findings. Together, let's celebrate the fusion of data, creativity, and technology!
    """)

    # Footer
    st.markdown("---")
    st.markdown("""
    Made with ❤️ by Team Insightful Four: Alireza, Morteza, Amir, and Mohammad Reza.
    """)

with tab_canis:
    canis_agent = CanisContent.Agent()
    fig = canis_agent.show_distribution_of_social_media()
    st.plotly_chart(fig)
    fig = canis_agent.show_distribution_of_parent_entities()
    st.plotly_chart(fig)
    fig = canis_agent.show_distribution_of_records_per_parents()
    st.plotly_chart(fig)

    geo_agent = WorldMapAgent.Agent("../twitter/users/")
    st.write("Geo Location")
    locs = geo_agent.generate_pointmap(file="../twitter/users/coords.json")
    st.map(locs)
    country_counts = geo_agent.coords2country_counts("../twitter/users/coords.json")
    # r = geo_agent.generate_heatmap(locs)
    st.write("Geo Heatmap")
    r = geo_agent.generate_heatmap_by_country("../data/custom.geo.json", country_counts)
    st.pydeck_chart(r)
    st.write("Plotly Plot")
    plotly_agent = PlotlyAgent.Agent()
    fig = plotly_agent.plot_3d_heat('Entity owner (English)', 'Region of Focus', 10)
    st.plotly_chart(fig)

with tab_twitter_content:
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

with tab_network:
    agent = FollowGraph.Agent()
    semantic_agent = semantic.Agent()
    st.write("Following Graph")
    df = pd.read_csv('../3d-network-visualization/clean_csvs/network.csv')
    text = st.text_input('Enter a text to analyse', 'all')
    if text == 'all':
        users = None
    else:
        users = semantic_agent.get_users(text)
    user_parent_entity = st.multiselect('select user parent entity', df['user_parent_entity'].unique())
    col1, col2 = st.columns(2)
    following_parent_entity = col1.multiselect('Select following parent entity', df['following_parent_entity'].unique())
    fig = agent.plot_network_graph(user_parent_entity, following_parent_entity, users)
    col1.plotly_chart(fig, use_container_width=True)
    following_parent_entity_2 = col2.multiselect('Select following parent entity to compare', df['following_parent_entity'].unique())
    fig2 = agent.plot_network_graph(user_parent_entity, following_parent_entity_2)
    col2.plotly_chart(fig2, use_container_width=True)
    st.write("Wiki Network Graph")
    networx_agent = WikiGraph.Agent()
    graph = networx_agent.plot_network_graph()
    st.components.v1.html(graph, height=800, width=800, scrolling=True)

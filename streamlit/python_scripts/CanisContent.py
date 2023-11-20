import pandas as pd
import plotly.express as px


class Agent:
    def __init__(self):
        self.canis_df = pd.read_csv('../data/CANIS_PRC_state_media_on_social_media_platforms-2023-11-03.csv')

    def show_distribution_of_social_media(self):
        platform_columns = [
            'X (Twitter) Follower #',
            'Facebook Follower #',
            'Instagram Follower #',
            'Threads Follower #',
            'YouTube Subscriber #',
            'TikTok Subscriber #'
        ]
        top_parent_entities = self.canis_df['Parent entity (English)'].value_counts().head(9).index
        top_entities_df = self.canis_df.copy(deep=True)
        top_entities_df.loc[
            ~top_entities_df['Parent entity (English)'].isin(top_parent_entities), 'Parent entity (English)'
        ] = 'Other'

        melted_df = top_entities_df.melt(id_vars=['Parent entity (English)'], value_vars=platform_columns,
                                         var_name='Platform', value_name='Follower Count')
        fig = px.bar(
            melted_df,
            x='Platform',
            y='Follower Count',
            color='Parent entity (English)',
            title='Distribution of Followers on Different Platforms per Top 9 Parent Entities',
            labels={'Platform': 'Platform', 'Follower Count': 'Follower Count'},
        )
        return fig

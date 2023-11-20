import pandas as pd
import plotly.express as px


def show_trend(df, key, title, count):
    df['created_at'] = pd.to_datetime(df['created_at'])
    last_month_records = df[df['created_at'] >= df['created_at'].max() - pd.DateOffset(months=1)]
    last_month_records['day_month'] = last_month_records['created_at'].dt.to_period('2D')
    records_counts = last_month_records.groupby(['day_month', key]).size().unstack().fillna(0)
    top_20_records = records_counts.sum().nlargest(count).index
    fig = px.line(records_counts, x=records_counts.index.astype(str), y=top_20_records, labels={'value': 'Count'},
                  title=title)
    fig.update_traces(hovertemplate='<b>%{y}</b>')
    fig.update_layout(xaxis=dict(tickangle=45))
    return fig


class Agent:
    def __init__(self):
        self.canis_df = pd.read_csv('../data/CANIS_PRC_state_media_on_social_media_platforms-2023-11-03.csv')
        self.hashtags_df = pd.read_csv('../hashtags.csv')
        self.tweets_df = pd.read_csv('../twitter/text/tweets_with_topic.csv')
        result = pd.merge(self.canis_df, self.tweets_df[self.tweets_df['topic'].notna()],
                          left_on='X (Twitter) handle', right_on='screen_name')
        weights = {'favorite_count': 1, 'reply_count': 2, 'quote_count': 3, 'retweet_count': 0}
        result['impression_score'] = (
                result['favorite_count'] * weights['favorite_count'] +
                result['quote_count'] * weights['quote_count'] +
                result['reply_count'] * weights['reply_count'] +
                result['retweet_count'] * weights['retweet_count']
        )
        self.result = result[result['topic'] != '-1_itiswhatitis_texte_complet_sacked']

    def show_hashtags_plot(self):
        hashtags_count = self.hashtags_df['hashtag'].value_counts()
        top_hashtags_df = pd.DataFrame(
            {'Hashtags': hashtags_count.head(20).index, 'Count': hashtags_count.head(20).values}
        )

        fig = px.bar(
            top_hashtags_df,
            x='Hashtags',
            y='Count',
            title='Top Hashtags',
            labels={'Hashtags': 'Hashtags', 'Count': 'Count'},
            category_orders={'Hashtags': hashtags_count.head(20).index},
        )

        fig.update_layout(xaxis=dict(tickangle=45, tickmode='array'))
        return fig

    def show_hashtags_trend(self):
        return show_trend(self.hashtags_df, key='hashtag', count=20,
                          title='Trends of Top 20 Hashtags Over the Last Month (Grouped by 2 Days)')

    def show_topics_trend(self):
        return show_trend(self.result, key='topic', count=50,
                          title='Trends of Top 50 Topics Over the Last Month (Grouped by 2 Days)')

    def show_topics_per_parent(self):
        top_10_entities = self.canis_df['Parent entity (English)'].value_counts().head(10).keys()
        filtered_df = self.result[self.result['Parent entity (English)'].isin(top_10_entities)]
        top_50_topics = filtered_df.groupby('topic')['impression_score'].sum().nlargest(50).index
        top_50_topics_df = filtered_df[filtered_df['topic'].isin(top_50_topics)]

        top_topics_per_entity = (
            top_50_topics_df.groupby(['Parent entity (English)', 'topic'])
            .size()
            .groupby(level=0, group_keys=False)
            .nlargest(100)
            .reset_index(name='count')
        )

        fig = px.bar(
            top_topics_per_entity,
            x='Parent entity (English)',
            y='count',
            color='topic',
            barmode='stack',
            labels={'count': 'Topic Count'},
            title='Distribution of the Top 50 Topics per top 10 Parent Entity',
        )
        fig.update_layout(height=800)
        return fig

    def show_most_impactful_topics(self):
        aggregated_df = self.result.groupby('topic')['impression_score'].sum().reset_index()
        aggregated_df['normalized_impression_score'] = (
                aggregated_df['impression_score'] / aggregated_df['impression_score'].sum()
        )
        top_topics_df = aggregated_df.sort_values(by='normalized_impression_score', ascending=False).head(20)
        fig = px.bar(
            top_topics_df,
            x='topic',
            y='normalized_impression_score',
            title='Top 20 Impressive Topics (Normalized)',
            labels={'topic': 'Topic', 'normalized_impression_score': 'Normalized Impression Score'},
            category_orders={'topic': top_topics_df['topic']},
        )
        fig.update_layout(xaxis=dict(tickangle=45, tickmode='array'))
        return fig

from bertopic import BERTopic
import pandas as pd

# topic_model = BERTopic.load("../twitter/text/topic.pkl", embedding_model="all-mpnet-base-v2")
# df = pd.read_csv("../twitter/text/tweets_with_topic_loc.csv")


class Agent:
    def __init__(self):
        pass

    def get_locations(self, text):
        return []
        similar_topics, similarity = topic_model.find_topics(text, top_n=3)
        topic_names = [topic_model.get_topic_info(t)["Name"] for t in similar_topics]
        topic_names = [t.values[0] for t in topic_names]
        return df[df["topic"].isin(topic_names)]['location']

    def get_users(self, text):
        return []
        similar_topics, similarity = topic_model.find_topics(text, top_n=3)
        topic_names = [topic_model.get_topic_info(t)["Name"] for t in similar_topics]
        topic_names = [t.values[0] for t in topic_names]
        return df[df["topic"].isin(topic_names)]['location']

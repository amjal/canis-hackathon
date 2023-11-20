from bertopic import BERTopic
import pandas as pd
topic_model = BERTopic.load("./topic.pkl")
df = pd.read_csv("../../twitter/text/tweets_with_topic_with_loc.csv")

class Agent:
	def __init__(self):
		pass

	def get_locations(self, text):
		similar_topics, similarity = topic_model.find_topics(text, top_n=3)
		topic_names = [topic_model.get_topic_info(t)["Name"] for t in similar_topics]
		topic_names = [t.values[0] for t in topic_names]
		return df[df["topic"].isin(topic_names)]['screen_name']



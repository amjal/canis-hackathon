from bertopic import BERTopic
import pandas as pd
import re
import emoji

topic_model = BERTopic.load("../twitter/text/topic.pkl", embedding_model="all-mpnet-base-v2")
df = pd.read_csv("../twitter/text/tweets_with_topic_loc.csv")

def clean_tweet_df(row):
    tweet = row["full_text"]
    tweet = re.sub("@[A-Za-z0-9]+","",tweet) #Remove @ sign
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
    tweet = " ".join(tweet.split())
    tweet = ''.join(c for c in tweet if c not in emoji.EMOJI_DATA)
    tweet = tweet.replace("#", "").replace("_", " ").replace("RT ", "").replace('&amp;', '&') #Remove hashtag sign but keep the text
    return tweet

df["cleaned_full_text"] = df.apply(clean_tweet_df, axis=1)

class Agent:
	def __init__(self):
		pass

	def get_locations(self, text):
		similar_topics, similarity = topic_model.find_topics(text, top_n=3)
		topic_names = [topic_model.get_topic_info(t)["Name"] for t in similar_topics]
		topic_names = [t.values[0] for t in topic_names]
		return df[df["topic"].isin(topic_names)]['location']

	def get_users(self, text):
		similar_topics, similarity = topic_model.find_topics(text, top_n=3)
		topic_names = [topic_model.get_topic_info(t)["Name"] for t in similar_topics]
		topic_names = [t.values[0] for t in topic_names]
		return df[df["topic"].isin(topic_names)]['location']

	def get_clean_tweets(self, text):
		similar_topics, similarity = topic_model.find_topics(text, top_n=3)
		topic_names = [topic_model.get_topic_info(t)["Name"] for t in similar_topics]
		topic_names = [t.values[0] for t in topic_names]
		return df[df["topic"].isin(topic_names)]["cleaned_full_text"]


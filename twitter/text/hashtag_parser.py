import json
import os

import pandas as pd

TWEETS_DIR = "twitter/tweets"


class NoTweetInFile(Exception):
    pass


def process_tweets_in_file(file_name):
    f = open(file_name, "r")
    tweets = json.load(f)
    intructions = tweets["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]

    tweet_entries = list(
        filter(lambda item: item.get("type") == "TimelineAddEntries", intructions)
    )
    if len(tweet_entries) == 0 or len(tweet_entries[0].get("entries", [])) == 0:
        raise NoTweetInFile()
    else:
        entries = tweet_entries[0].get("entries", [])
        items = []
        for entry in entries:
            entry_id = entry.get("entryId")
            if entry_id is None:
                continue
            if "promoted" in entry.get("entryId"):
                continue
            if "who-to" in entry.get("entryId"):
                continue

            if entry["content"]["entryType"] == "TimelineTimelineItem":
                items.append(entry["content"]["itemContent"]["tweet_results"])
            elif entry["content"]["entryType"] == "TimelineTimelineModule":
                content = entry["content"]
                for item in content["items"]:
                    if item["item"]["itemContent"]["itemType"] == "TimelineTweet":
                        items.append(item["item"]["itemContent"]["tweet_results"])

        entry_dicts = []
        for entry in items:
            if 'tweet' in entry["result"]:
                result = entry["result"]["tweet"]
            else:
                result = entry["result"]
            user_source = result["core"]["user_results"]["result"]["legacy"]
            tweet_source = result["legacy"]
            retweet_user_source = tweet_source.get("retweeted_status_result", {}).get("result", {}).get("core", {}).get("user_results", {}).get("result", {}).get("legacy", {})
            qoute_user_source = entry["result"].get("quoted_status_result", {}).get("result", {}).get("core", {}).get("user_results", {}).get("result", {}).get("legacy", {})

            def enrich_entry():
                entry_dict = {}
                from_tweet = ["bookmark_count", "created_at", "favorite_count", "full_text", "id_str", "lang", "possibly_sensitive", "quote_count", "reply_count", "retweet_count", "user_id_str"]
                from_user = ["screen_name"]
                from_retweet_user = ["screen_name", "location"]
                from_qoute_user = ["screen_name", "location"]

                for field in from_tweet:
                    entry_dict[field] = tweet_source.get(field)
                for field in from_user:
                    entry_dict[field] = user_source.get(field)
                for field in from_retweet_user:
                    entry_dict[f"retweet-{field}"] = retweet_user_source.get(field)
                for field in from_qoute_user:
                    entry_dict[f"qoute-{field}"] = qoute_user_source.get(field)
                return entry_dict

            entry_dict = enrich_entry()
            entry_dicts.append(entry_dict)
        return entry_dicts


def process_tweets_in_dir(directory):
    all_tweets = []
    for file in os.listdir(directory):
        file_path = f"{directory}/{file}"
        tweets = process_tweets_in_file(file_path)
        all_tweets += tweets
    return all_tweets
    

if __name__ == "__main__":
    tweets = process_tweets_in_dir("twitter/tweets")
    df = pd.DataFrame(tweets)
    df.to_csv("tweets.csv", index=None)
    print(len(df))

import json
import os

import pandas as pd

TWEETS_DIR = "twitter/tweets"


class NoTweetInFile(Exception):
    pass


def process_hashtags_in_file(file_name):
    f = open(file_name, "r")
    tweets = json.load(f)
    intructions = tweets["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]
    tweet_entries = list(filter(lambda item: item.get("type") == "TimelineAddEntries", intructions))

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
            hashtag_sources = result["legacy"]["entities"]["hashtags"]
            tweet_source = result["legacy"]

            def enrich_entry(hashtag_source):
                entry_dict = {}
                from_tweet = ["id_str", "user_id_str", "created_at"]
                from_user = ["screen_name", "location"]
                from_hashtag_source = ["text"]

                for field in from_tweet:
                    entry_dict[field] = tweet_source.get(field)
                for field in from_user:
                    entry_dict[field] = user_source.get(field)
                for field in from_hashtag_source:
                    entry_dict[f"hashtag"] = hashtag_source.get(field)
                return entry_dict

            entries = list(map(enrich_entry, hashtag_sources))
            entry_dicts.extend(entries)
        return entry_dicts


def process_hashtags_in_dir(directory):
    all_hashtags = []
    for file in os.listdir(directory):
        file_path = f"{directory}/{file}"
        hashtags = process_hashtags_in_file(file_path)
        all_hashtags += hashtags
    return all_hashtags
    

if __name__ == "__main__":
    tweets = process_hashtags_in_dir("twitter/tweets")
    df = pd.DataFrame(tweets)
    df.to_csv("hashtags.csv", index=None)
    print(len(df))

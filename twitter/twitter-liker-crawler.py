import json
import random
import time

import requests

import setting

url = 'https://twitter.com/i/api/graphql/zXD9lMy1-V_N1OcON9JtEQ/Favoriters'

variables = {
    "tweetId": "1725974266405859330",
    "count": 20,
    "includePromotedContent": False
}


def fetch_likers(path, tweet_id, cursor=None):
    global entries_cnt
    variables["tweetId"] = tweet_id
    if cursor is not None:
        variables["cursor"] = cursor
    payload = {
        "variables": json.dumps(variables),
        "features": json.dumps(setting.tweet_features)
    }
    response = requests.get(url, headers=setting.headers, params=payload)
    data = response.json()

    f = open(f"twitter/likers/{path}.json", "w")
    f.write(json.dumps(data))
    f.flush()
    f.close()

    instructions = data["data"]["favoriters_timeline"]["timeline"]["instructions"]
    entries = list(filter(lambda x: x["type"] == "TimelineAddEntries", instructions))[0]["entries"]
    cursor = list(filter(lambda x: "cursor-bottom" in x["entryId"], entries))[0]["content"]["value"]
    entries_curr = len(entries) - 2
    entries_cnt += entries_curr
    print(f"\tfetched {path} with {entries_curr} items - total fetched {entries_cnt}")

    sleepy = random.randint(0, 5)
    time.sleep(sleepy)

    if len(entries) == 0:
        return None

    return cursor


tweet_id = "ada"  # sys.argv[1]
print(f"{tweet_id}")
page = 1
entries_cnt = 0
path = f"{tweet_id}-{page}"
cursor = fetch_likers(path, tweet_id)
while cursor is not None and page < 3:
    page += 1
    path = f"{tweet_id}-{page}"
    cursor = fetch_likers(path, tweet_id, cursor)
    sleepy = random.randint(0, 5)
    time.sleep(sleepy)

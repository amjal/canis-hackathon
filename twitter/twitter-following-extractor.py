import json
import os
import random
import sys
import time

import requests

# from twitter
import priorities
import setting

# from twitter.csrf import get_csrf

csrf_counter = 1
entries_cnt = 0
url = 'https://twitter.com/i/api/graphql/8cyc0OKedV_XD62fBjzxUw/Following'

variables = {
    "userId": "35175126",
    "count": 20,
    "includePromotedContent": False
}


def fetch_following_page(user, user_id, page=1, cursor=None):
    global csrf_counter, entries_cnt
    variables["userId"] = user_id
    if cursor is not None:
        variables["cursor"] = cursor
    payload = {
        "variables": json.dumps(variables),
        "features": json.dumps(setting.tweet_features)
    }
    response = requests.get(url, headers=setting.headers, params=payload)
    data = response.json()

    f = open(f"twitter/followers/{user}-P{page}.json", "w")
    f.write(json.dumps(data))
    f.flush()
    f.close()

    instructions = data["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]
    entries = list(filter(lambda x: x["type"] == "TimelineAddEntries", instructions))[0]["entries"]
    cursor = list(filter(lambda x: "cursor-bottom" in x["entryId"], entries))[0]["content"]["value"]
    entries_curr = len(entries) - 2
    entries_cnt += entries_curr
    print(f"\tfetched page {page} with {entries_curr} items - total fetched {entries_cnt}")

    sleepy = random.randint(0, 5)
    time.sleep(sleepy)
    csrf_counter += 1

    return cursor


users = priorities.C[:]
index = int(sys.argv[1])

user = users[index]
print(f"{index + 1}/{len(users)}. {user}")
file_name = f"twitter/users/{user}.json"
cursor = None
if os.path.exists(file_name):
    f = open(file_name)
    data = json.load(f)
    user_id = data["data"]["user"]["result"]["rest_id"]
    followings = data["data"]["user"]["result"]["legacy"]["friends_count"]
    print(f"\t{followings} followings")
    page = 1
    entries_cnt = 0
    cursor = fetch_following_page(user, user_id)
    while not cursor.startswith("0|") and page < 10:
        page += 1
        cursor = fetch_following_page(user, user_id, page, cursor)

    if (entries_cnt / followings) < 0.9 and page < 8:
        # headers['x-csrf-token'] = get_csrf()
        # headers['cookie'] = headers['cookie'].split("ct0=")[0] + 'ct0=' + headers['x-csrf-token']
        print("\t\tNot enough!!! Try again")
        sleepy = random.randint(0, 5)
        time.sleep(sleepy)

    sleepy = random.randint(0, 5)
    time.sleep(sleepy)
else:
    print("\tnot found!")

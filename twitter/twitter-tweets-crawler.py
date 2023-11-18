import json
import os
import random
import sys
import time

import requests

# from twitter
import priorities

csrf_counter = 1
entries_cnt = 0
url = 'https://twitter.com/i/api/graphql/VgitpdpNZ-RUIp5D1Z_D-A/UserTweets'

headers = {
    'authority': 'twitter.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'authorization': 'Bearer ***REMOVED***',
    'content-type': 'application/json',
    'cookie': '_ga=GA1.2.880126000.1691779904; lang=en; guest_id=v1%3A169998054129071930; g_state={"i_p":1699987747887,"i_l":1}; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGudvM6LAToMY3NyZl9p%250AZCIlNzQ2Mzg4ZTM5ODYzOTAxY2I3ZWM2YjRjNTRkYWQ1YTE6B2lkIiUyN2Uy%250ANjE3MzIzZmY0OTYzNDNhNDY5MTMwMDdkYTY5MQ%253D%253D--3cf6a17c9d77e47d3bc3731964da5b89ff7de02d; kdt=UANhrHFuDXkxjTcjAOgq9DIF5QLSJdxD1OElHybR; auth_token=5cd2e6077966875d663293e4101b96fbedb5818b; guest_id_ads=v1%3A169998054129071930; guest_id_marketing=v1%3A169998054129071930; twid=u%3D767620711414456320; night_mode=1; _gid=GA1.2.1404017273.1700157076; external_referer=8e8t2xd8A2w%3D|0|S38otfNfzYt86Dak8Eqj76tqscUAnK6Lq4vYdCl5zxIvK6QAA8vRkA%3D%3D; personalization_id="v1_ZvzweLlSDUIk0+Mbg7mCzw=="; ct0=012b4da978acb746321d790e49f1833c9cfcd23491669aae749aa99b16afa23f4f57d94680adea1e3b30431994975fd0adae6bb42bc874e4adb80d8b1453336f269dbb8c790ef1aca67ccf69fa23bd63',
    'referer': 'https://twitter.com/CGTNOfficial/following',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-client-transaction-id': 'gZgAfoFmEHPWvZX8xnRjarX9eUStbO03b3MOhcOH0xfpkkKWPP9bVMVE9NKoJ6MFOxA+iYCg2m3hpj5MwTu83hmGkap3gA',
    'x-csrf-token': '012b4da978acb746321d790e49f1833c9cfcd23491669aae749aa99b16afa23f4f57d94680adea1e3b30431994975fd0adae6bb42bc874e4adb80d8b1453336f269dbb8c790ef1aca67ccf69fa23bd63',
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-client-language': 'en',
}

variables = {
    "userId": "35175126",
    "count": 20,
    "includePromotedContent": False,
    "withQuickPromoteEligibilityTweetFields": True,
    "withVoice": True,
    "withV2Timeline": True
}

features = {
    "responsive_web_graphql_exclude_directive_enabled": True,
    "verified_phone_label_enabled": False,
    "responsive_web_home_pinned_timelines_enabled": True,
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "responsive_web_graphql_timeline_navigation_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "c9s_tweet_anatomy_moderator_badge_enabled": True,
    "tweetypie_unmention_optimization_enabled": True,
    "responsive_web_edit_tweet_api_enabled": True,
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
    "view_counts_everywhere_api_enabled": True,
    "longform_notetweets_consumption_enabled": True,
    "responsive_web_twitter_article_tweet_consumption_enabled": False,
    "tweet_awards_web_tipping_enabled": False,
    "freedom_of_speech_not_reach_fetch_enabled": True,
    "standardized_nudges_misinfo": True,
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
    "longform_notetweets_rich_text_read_enabled": True,
    "longform_notetweets_inline_media_enabled": True,
    "responsive_web_media_download_video_enabled": False,
    "responsive_web_enhance_cards_enabled": False
}


def fetch_tweets(path, user_id, cursor=None):
    global csrf_counter, entries_cnt
    variables["userId"] = user_id
    if cursor is not None:
        variables["cursor"] = cursor
    payload = {
        "variables": json.dumps(variables),
        "features": json.dumps(features)
    }
    response = requests.get(url, headers=headers, params=payload)
    data = response.json()

    f = open(f"twitter/tweets/{path}.json", "w")
    f.write(json.dumps(data))
    f.flush()
    f.close()

    instructions = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]
    entries = list(filter(lambda x: x["type"] == "TimelineAddEntries", instructions))[0]["entries"]
    cursor = list(filter(lambda x: "cursor-bottom" in x["entryId"], entries))[0]["content"]["value"]
    entries_curr = len(entries) - 2
    entries_cnt += entries_curr
    print(f"\tfetched {path} with {entries_curr} items - total fetched {entries_cnt}")

    sleepy = random.randint(0, 5)
    time.sleep(sleepy)
    csrf_counter += 1

    return cursor


users = priorities.A[:]
index = int(sys.argv[1])

user = users[index]
print(f"{index + 1}/{len(users)}. {user}")
file_name = f"twitter/users/{user}.json"
cursor = None
if os.path.exists(file_name):
    f = open(file_name)
    data = json.load(f)
    user_id = data["data"]["user"]["result"]["rest_id"]
    tweets = data["data"]["user"]["result"]["legacy"]["statuses_count"]
    print(f"\t{tweets} tweets")
    page = 1
    entries_cnt = 0
    path = f"{user}-{page}"
    cursor = fetch_tweets(path, user_id)
    while not cursor.startswith("0|") and page < 3:
        page += 1
        path = f"{user}-{page}"
        cursor = fetch_tweets(path, user_id, cursor)

    if (entries_cnt / tweets) < 0.9 and page < 2:
        # headers['x-csrf-token'] = get_csrf()
        # headers['cookie'] = headers['cookie'].split("ct0=")[0] + 'ct0=' + headers['x-csrf-token']
        print("\t\tNot enough!!! Try again")
        sleepy = random.randint(0, 5)
        time.sleep(sleepy)

    sleepy = random.randint(0, 5)
    time.sleep(sleepy)
else:
    print("\tnot found!")

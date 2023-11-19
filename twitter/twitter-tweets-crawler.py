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
    'cookie': '_ga=GA1.2.969896973.1696998755; g_state={"i_l":0}; dnt=1; kdt=wjkhgLelgg2ZvM8BrIgwC6dYROEtrqXRTid31Azn; auth_multi="1506423965765361668:985c89ca780926e7b0216c93bb736dceccf471ba"; auth_token=9f609bebca2a6b78cc9b5817dfccef5747f557e4; guest_id=v1%3A169827441278458399; twid=u%3D317718475; ct0=eaf17f3f562aa2e83ce28c617b63fe115ef9631ae11919961a894ceda0444858d89f5bd74cc4647dac36d94c58a843ae6a62299f4347ba5c3b58c4bf618dc40bddb847af7f5a6d3c5e0c61fffe51a11e; guest_id_ads=v1%3A169827441278458399; guest_id_marketing=v1%3A169827441278458399; lang=en; _gid=GA1.2.2110745042.1700191550; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|ziZgIoZIK4nlMKUVLq9KcnBFms0d9TqBqrE%2FyjvSFlFJR45yIlYF%2Bw%3D%3D; des_opt_in=Y; personalization_id="v1_ndcezjNfcxEINDZLydTLTw=="',
    'referer': 'https://twitter.com/CGTNOfficial/following',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-client-transaction-id': 'KBiScTuWMoMo4aKIzI9zNjmRG9UQ/uS1jRqZFXxDYts/OBNtCH9/yTDjGnLuRbLwxRuZISmQzk8YtUtdv7NusZs+JlNFKQ',
    'x-csrf-token': 'eaf17f3f562aa2e83ce28c617b63fe115ef9631ae11919961a894ceda0444858d89f5bd74cc4647dac36d94c58a843ae6a62299f4347ba5c3b58c4bf618dc40bddb847af7f5a6d3c5e0c61fffe51a11e',
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


users = priorities.B[:]
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

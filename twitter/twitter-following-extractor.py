import json
import os
import time

import requests

from twitter import priorities

url = 'https://twitter.com/i/api/graphql/8cyc0OKedV_XD62fBjzxUw/Following'

headers = {
    'authority': 'twitter.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'authorization': 'Bearer ***REMOVED***',
    'content-type': 'application/json',
    'cookie': '_ga=GA1.2.880126000.1691779904; lang=en; guest_id=v1%3A169998054129071930; g_state={"i_p":1699987747887,"i_l":1}; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGudvM6LAToMY3NyZl9p%250AZCIlNzQ2Mzg4ZTM5ODYzOTAxY2I3ZWM2YjRjNTRkYWQ1YTE6B2lkIiUyN2Uy%250ANjE3MzIzZmY0OTYzNDNhNDY5MTMwMDdkYTY5MQ%253D%253D--3cf6a17c9d77e47d3bc3731964da5b89ff7de02d; kdt=UANhrHFuDXkxjTcjAOgq9DIF5QLSJdxD1OElHybR; auth_token=5cd2e6077966875d663293e4101b96fbedb5818b; ct0=6c9a01b4537405170d2ce35ebc721e389bc72ecf9266643694b5048791bb8ca62767c6f0c99960e26b92a810ae2bea1e6c20f2773d2ad79bcfca3854b2b29b719ba337b1d7aba2f74ec5d217bccefa9c; guest_id_ads=v1%3A169998054129071930; guest_id_marketing=v1%3A169998054129071930; twid=u%3D767620711414456320; night_mode=1; _gid=GA1.2.1404017273.1700157076; external_referer=8e8t2xd8A2w%3D|0|S38otfNfzYt86Dak8Eqj76tqscUAnK6Lq4vYdCl5zxIvK6QAA8vRkA%3D%3D; personalization_id="v1_ANpSW3bOa9K3GJ5d0599tw=="',
    'referer': 'https://twitter.com/CGTNOfficial/following',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-client-transaction-id': 'gZgAfoFmEHPWvZX8xnRjarX9eUStbO03b3MOhcOH0xfpkkKWPP9bVMVE9NKoJ6MFOxA+iYCg2m3hpj5MwTu83hmGkap3gA',
    'x-csrf-token': '6c9a01b4537405170d2ce35ebc721e389bc72ecf9266643694b5048791bb8ca62767c6f0c99960e26b92a810ae2bea1e6c20f2773d2ad79bcfca3854b2b29b719ba337b1d7aba2f74ec5d217bccefa9c',
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-client-language': 'en',
}

variables = {
    "userId": "35175126",
    "count": 20,
    "includePromotedContent": False
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
    "responsive_web_enhance_cards_enabled": False,
}


def fetch_following_page(user_id, page=1, cursor=None):
    variables["userId"] = user_id
    if cursor is not None:
        variables["cursor"] = cursor
    payload = {
        "variables": json.dumps(variables),
        "features": json.dumps(features)
    }
    response = requests.get(url, headers=headers, params=payload)
    data = response.json()

    f = open(f"twitter/followers/{user}-P{page}.json", "w")
    f.write(json.dumps(data))
    f.flush()
    f.close()

    instructions = data["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]
    entries = list(filter(lambda x: x["type"] == "TimelineAddEntries", instructions))[0]["entries"]
    cursor = list(filter(lambda x: "cursor-bottom" in x["entryId"], entries))[0]["content"]["value"]
    print(f"\tfetched page {page} with {len(entries)} items")

    time.sleep(5)

    return cursor


for index, user in enumerate(priorities.A[17:]):
    print(f"{index + 1}/{len(priorities.A)}. {user}")
    file_name = f"twitter/users/{user}.json"
    if os.path.exists(file_name):
        f = open(file_name)
        data = json.load(f)
        user_id = data["data"]["user"]["result"]["rest_id"]
        followings = data["data"]["user"]["result"]["legacy"]["friends_count"]
        print(f"\t{followings} followings")
        page = 1
        cursor = fetch_following_page(user_id)
        while not cursor.startswith("0|") and page < 10:
            page += 1
            cursor = fetch_following_page(user_id, page, cursor)
    else:
        print("\tnot found!")

import json
import os
import time

import requests

from twitter import priorities

url = 'https://twitter.com/i/api/graphql/G3KGOASz96M-Qu0nwmGXNg/UserByScreenName'
headers = {
    'authority': 'twitter.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'authorization': 'Bearer ***REMOVED***',
    'content-type': 'application/json',
    'cookie': '_ga=GA1.2.880126000.1691779904; lang=en; guest_id=v1%3A169998054129071930; g_state={"i_p":1699987747887,"i_l":1}; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGudvM6LAToMY3NyZl9p%250AZCIlNzQ2Mzg4ZTM5ODYzOTAxY2I3ZWM2YjRjNTRkYWQ1YTE6B2lkIiUyN2Uy%250ANjE3MzIzZmY0OTYzNDNhNDY5MTMwMDdkYTY5MQ%253D%253D--3cf6a17c9d77e47d3bc3731964da5b89ff7de02d; kdt=UANhrHFuDXkxjTcjAOgq9DIF5QLSJdxD1OElHybR; auth_token=5cd2e6077966875d663293e4101b96fbedb5818b; ct0=6c9a01b4537405170d2ce35ebc721e389bc72ecf9266643694b5048791bb8ca62767c6f0c99960e26b92a810ae2bea1e6c20f2773d2ad79bcfca3854b2b29b719ba337b1d7aba2f74ec5d217bccefa9c; guest_id_ads=v1%3A169998054129071930; guest_id_marketing=v1%3A169998054129071930; twid=u%3D767620711414456320; night_mode=1; external_referer=8e8t2xd8A2w%3D|0|Row7tAmsAfIEmjPNOVSmwU7WBxyUUJED%2FJi%2FFP0ccJQLMXwElqvDBJpHIUJZymRK; _gid=GA1.2.1404017273.1700157076; personalization_id="v1_Nncd/7EOq1XD3iTJ4IPDFg=="',
    'referer': 'https://twitter.com/Zhou_Li_CHN',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-client-transaction-id': 'mepvdEj48PGrv2nkzYYsI6vWn5jUNa0g8ZeafmEe7fLilDEjVv2tABZ3W6UVelJDST02kZhGezldMaxaIhPFhhsXZtZimA',
    'x-csrf-token': '6c9a01b4537405170d2ce35ebc721e389bc72ecf9266643694b5048791bb8ca62767c6f0c99960e26b92a810ae2bea1e6c20f2773d2ad79bcfca3854b2b29b719ba337b1d7aba2f74ec5d217bccefa9c',
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-client-language': 'en',
}

# Variables and payload
variables = {
    "screen_name": "_bubblyabby_",
    "withSafetyModeUserFields": True
}
features = {
    "hidden_profile_likes_enabled": True,
    "hidden_profile_subscriptions_enabled": True,
    "responsive_web_graphql_exclude_directive_enabled": True,
    "verified_phone_label_enabled": False,
    "subscriptions_verification_info_is_identity_verified_enabled": True,
    "subscriptions_verification_info_verified_since_enabled": True,
    "highlights_tweets_tab_ui_enabled": True,
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "responsive_web_graphql_timeline_navigation_enabled": True
}
field_toggles = {
    "withAuxiliaryUserLabels": False
}

rest_map = {}

for index, user in enumerate(priorities.A):
    variables["screen_name"] = user
    payload = {
        "variables": json.dumps(variables),
        "features": json.dumps(features),
        "fieldToggles": json.dumps(field_toggles)
    }

    print(f"{index + 1}/{len(priorities.A)} Crawling for {user}")
    try:
        file_name = f"users/{user}.json"
        if os.path.exists(file_name):
            print("\talready existed")
            continue
        response = requests.get(url, headers=headers, params=payload)
        data = response.json()
        rest_map[user] = data["data"]["user"]["result"]["rest_id"]

        f = open(file_name, "w")
        f.write(json.dumps(data))
        f.flush()
        f.close()
    except Exception as ex:
        print("\tfailed to fetch")

    time.sleep(5)

print("---------------------------------------------------")
print(rest_map)

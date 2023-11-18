import json
import os
import time

import requests

import priorities

url = 'https://twitter.com/i/api/graphql/G3KGOASz96M-Qu0nwmGXNg/UserByScreenName'

headers = {
    'authority': 'twitter.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'authorization': 'Bearer ***REMOVED***',
    'content-type': 'application/json',
    'cookie': 'guest_id=v1%3A167350876100677622; g_state={"i_l":0}; kdt=xxgDTka3gPA9K52pGpzLqIyTVhLSkzbbCCi9LrGB; lang=en; auth_token=6082046d8211db8cfee616c4cde5e47d37240dc2; twid=u%3D4717658005; d_prefs=MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; guest_id_ads=v1%3A167350876100677622; guest_id_marketing=v1%3A167350876100677622; _ga=GA1.2.1608448632.1685820982; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCPr64AqKAToMY3NyZl9p%250AZCIlYTFmMjY2ZGZhNTEwZGFkMDVmY2IyMDc4Nzc3M2UyNTA6B2lkIiU1MjI2%250AYTg0YzY4NDE0OTIxYTBjNWUxNDk4MTI1NzEzNA%253D%253D--78dc5e27db9695fe3633744e0069af8c76e31f48; _gid=GA1.2.2124721875.1699936592; amp_6e403e=R8o1-v5YjN-agALg1Wiuqz...1hf61rot4.1hf61rot4.0.0.0; external_referer=padhuUp37zhoIGvF4Apzqg16MfI8H6yPtDDLSRhJjFDoN8U3lRYvbg%3D%3D|0|8e8t2xd8A2w%3D; ct0=61f0daef94373e3a527f51d416f51818335bd50dc51ffab6a3f9e5f33b40ad519c84fdf43438bcf92784a7fd6d62c6b855f93f8a829f2b749ee7a40887f384bb9e42cc404865a8cb7f149975867817fe; personalization_id="v1_KAWK/rvpfCeWooUGySFWpQ=="',
    'referer': 'https://twitter.com/Zhou_Li_CHN',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-client-transaction-id': 'mepvdEj48PGrv2nkzYYsI6vWn5jUNa0g8ZeafmEe7fLilDEjVv2tABZ3W6UVelJDST02kZhGezldMaxaIhPFhhsXZtZimA',
    'x-csrf-token': '61f0daef94373e3a527f51d416f51818335bd50dc51ffab6a3f9e5f33b40ad519c84fdf43438bcf92784a7fd6d62c6b855f93f8a829f2b749ee7a40887f384bb9e42cc404865a8cb7f149975867817fe',
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

for index, user in enumerate(priorities.B):
    variables["screen_name"] = user
    payload = {
        "variables": json.dumps(variables),
        "features": json.dumps(features),
        "fieldToggles": json.dumps(field_toggles)
    }

    print(f"{index + 1}/{len(priorities.A)} Crawling for {user}")
    try:
        file_name = f"twitter/users/{user}.json"
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
        print(ex)
        print("\tfailed to fetch")

    time.sleep(3)

print("---------------------------------------------------")
print(rest_map)

import json

import requests

url = 'https://twitter.com/i/api/graphql/G3KGOASz96M-Qu0nwmGXNg/UserByScreenName'
headers = {
    'authority': 'twitter.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer ***REMOVED***',
    'content-type': 'application/json',
    'cookie': '_ga=GA1.2.1516747026.1700257313; _gid=GA1.2.384391922.1700257313; guest_id=v1%3A170025731328715985; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGW7O9%252BLAToMY3NyZl9p%250AZCIlMDgwMmFjMTU0ZmJjNDJiM2Y5ZTcwNjYyZDMzYjdhY2E6B2lkIiVkY2Qy%250AYmUxM2JkMDMxODU4YzZlODk3Y2RiZmRlMTAwMw%253D%253D--5f2904f6c9f2d0a1b3f164574c9061c6eb913821; kdt=IvRhczUxIttZZxeD91D1kMq3g3eBZkSAYgRGgaD7; auth_token=ae3fcf71d1d450cc2bcd271eea70b0140c024cb6; ct0=a6c4ad6ac22cdafb75c9b5165389533f59a6b0bbe8a4648859036e38eecd108076e15b4b476a8167de9516f0974a95d6e31d436084f790b471b16592d6827a98c6546f7b2b1465d6677eab26eb25d0ed; att=1-KZ219hVs1tUWvfDG6d41QU5YJq7DuU8L6uGgXAPc; guest_id_ads=v1%3A170025731328715985; guest_id_marketing=v1%3A170025731328715985; lang=en; twid=u%3D767620711414456320; personalization_id="v1_NiRxj5bQIG4W+c6MBQ587A=="',
    'referer': 'https://twitter.com/_bubblyabby_',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-client-transaction-id': 'nxYjqv9368nh5726ylPaAnQ9IczOUf5SQfR0wUYLxdANK9VZnx0SselcFToHUJ43TiEWl54QC/5aH0LznOx5hPFsbdUGng',
    'x-client-uuid': '089d796a-50ee-4e30-a9ee-e06452004b4c',
    'x-csrf-token': 'a6c4ad6ac22cdafb75c9b5165389533f59a6b0bbe8a4648859036e38eecd108076e15b4b476a8167de9516f0974a95d6e31d436084f790b471b16592d6827a98c6546f7b2b1465d6677eab26eb25d0ed',
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

payload = {
    "variables": json.dumps(variables),
    "features": json.dumps(features),
    "fieldToggles": json.dumps(field_toggles)
}

# Make the request
response = requests.get(url, headers=headers, params=payload)

# Print the response content
print(response.json())

BEARER_TOKEN = 'Bearer ***REMOVED***'
COOKIE = '_ga=GA1.2.880126000.1691779904; lang=en; guest_id=v1%3A169998054129071930; g_state={"i_p":1699987747887,"i_l":1}; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGudvM6LAToMY3NyZl9p%250AZCIlNzQ2Mzg4ZTM5ODYzOTAxY2I3ZWM2YjRjNTRkYWQ1YTE6B2lkIiUyN2Uy%250ANjE3MzIzZmY0OTYzNDNhNDY5MTMwMDdkYTY5MQ%253D%253D--3cf6a17c9d77e47d3bc3731964da5b89ff7de02d; kdt=UANhrHFuDXkxjTcjAOgq9DIF5QLSJdxD1OElHybR; auth_token=5cd2e6077966875d663293e4101b96fbedb5818b; guest_id_ads=v1%3A169998054129071930; guest_id_marketing=v1%3A169998054129071930; twid=u%3D767620711414456320; night_mode=1; _gid=GA1.2.1404017273.1700157076; ct0=012b4da978acb746321d790e49f1833c9cfcd23491669aae749aa99b16afa23f4f57d94680adea1e3b30431994975fd0adae6bb42bc874e4adb80d8b1453336f269dbb8c790ef1aca67ccf69fa23bd63; external_referer=padhuUp37zhfnmMHJBkh90t2l3UgMpRCkfFSbT%2Bt1Mg%3D|0|8e8t2xd8A2w%3D; personalization_id="v1_vX+n6zUTk0qHbYCxD1wQEQ=="'
CLIENT_TX_ID = 'VrLvgL6lnwWRzz7jaJDLFa102s1zYNIcElxKG3eNLljiydfnfPP81gZPpccIlPnbg2yoX1f1JIVPNEf39AWiMaNRNrysVw'
CSRF_TOKEN = '012b4da978acb746321d790e49f1833c9cfcd23491669aae749aa99b16afa23f4f57d94680adea1e3b30431994975fd0adae6bb42bc874e4adb80d8b1453336f269dbb8c790ef1aca67ccf69fa23bd63'

headers = {
    'authority': 'twitter.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'authorization': BEARER_TOKEN,
    'content-type': 'application/json',
    'cookie': COOKIE,
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-client-transaction-id': CLIENT_TX_ID,
    'x-csrf-token': CSRF_TOKEN,
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-client-language': 'en',
}

tweet_features = {
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

user_features = {
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

import requests

# URL and headers based on the curl command
url = 'https://twitter.com/i/api/graphql/8cyc0OKedV_XD62fBjzxUw/Following?variables=%7B%22userId%22%3A%221871166433%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_home_pinned_timelines_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'
headers = {
    'authority': 'twitter.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'authorization': 'Bearer ***REMOVED***',
    'content-type': 'application/json',
    'referer': 'https://twitter.com/1rpwn/following',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Linux',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-client-transaction-id': '4+zIb6KJEs3Sld8lOT5JE2YN+jozR42FIBmwDZb9hmL8txPSLiF2oRfz8RUhy83yCaJG6+I055/bQVFCbLrIHQzAGGjp4g',
    'x-csrf-token': '81ceb1b92b7dda49b66700db193e6ce156703b4093561614d11233aac5bcb7b02ead92918d8a31c05dc5a549090efdf5e7f56f1c03c4e49fc1857ea8cef726e7804bc95a6df9bfc2207b7778c42126fb',
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-client-language': 'en',
}

# Make the GET request
response = requests.get(url, headers=headers)
print(response.text)

# Write the response to a file if the request was successful
if response.status_code == 200:
    with open('response.txt', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print("Response successfully written to 'response.txt'")
else:
    print(f"Request failed with status code: {response.status_code}")


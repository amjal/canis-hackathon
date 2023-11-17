import json

with open('data/following.json', 'r') as file:
    data = json.load(file)

users = []
instructions = data.get('data', {}).get('user', {}).get('result', {}).get('timeline', {}).get('timeline', {}).get('instructions', [])
for instruction in instructions:
    entries = instruction.get('entries', [])
    for entry in entries:
        content = entry.get('content', {})
        item_content = content.get('itemContent', {})
        if 'user_results' in item_content:
            user_data = item_content['user_results']['result']
            user = {
                'user_id': user_data.get('id'),
                'screen_name': user_data.get('legacy', {}).get('screen_name'),
                'name': user_data.get('legacy', {}).get('name'),
                'description': user_data.get('legacy', {}).get('description'),
                'followers_count': user_data.get('legacy', {}).get('followers_count'),
                'friends_count': user_data.get('legacy', {}).get('friends_count'),
                'listed_count': user_data.get('legacy', {}).get('listed_count'),
                'location': user_data.get('legacy', {}).get('location'),
                'profile_image_url': user_data.get('legacy', {}).get('profile_image_url_https'),
                'profile_banner_url': user_data.get('legacy', {}).get('profile_banner_url'),
                'profile_url': user_data.get('legacy', {}).get('url'),
                'verified': user_data.get('legacy', {}).get('verified')
            }
            users.append(user)

# Print user details
for i, user in enumerate(users, start=1):
    print(f"User {i}:")
    print(f"  User ID: {user.get('user_id')}")
    print(f"  Screen Name: {user.get('screen_name')}")
    print(f"  Name: {user.get('name')}")
    print(f"  Description: {user.get('description')}")
    print(f"  Followers Count: {user.get('followers_count')}")
    print(f"  Friends Count: {user.get('friends_count')}")
    print(f"  Listed Count: {user.get('listed_count')}")
    print(f"  Location: {user.get('location')}")
    print(f"  Profile Image URL: {user.get('profile_image_url')}")
    print(f"  Profile Banner URL: {user.get('profile_banner_url')}")
    print(f"  Profile URL: {user.get('profile_url')}")
    print(f"  Verified: {user.get('verified')}")
    print("\n")

import json
import os
import time

import requests

import priorities
import setting

url = 'https://twitter.com/i/api/graphql/G3KGOASz96M-Qu0nwmGXNg/UserByScreenName'

# Variables and payload
variables = {
    "screen_name": "_bubblyabby_",
    "withSafetyModeUserFields": True
}

field_toggles = {
    "withAuxiliaryUserLabels": False
}

rest_map = {}

for index, user in enumerate(priorities.B):
    variables["screen_name"] = user
    payload = {
        "variables": json.dumps(variables),
        "features": json.dumps(setting.user_features),
        "fieldToggles": json.dumps(field_toggles)
    }

    print(f"{index + 1}/{len(priorities.A)} Crawling for {user}")
    try:
        file_name = f"users/{user}.json"
        # if os.path.exists(file_name):
        #     print("\talready existed")
        #     continue
        response = requests.get(url, headers=setting.headers, params=payload)
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

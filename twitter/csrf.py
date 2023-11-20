import requests

import setting

url = 'https://twitter.com/jannatkhah_ir/following'

headers = {
    'authority': 'twitter.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_ga=GA1.2.880126000.1691779904; lang=en; guest_id=v1%3A169998054129071930; g_state={"i_p":1699987747887,"i_l":1}; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGudvM6LAToMY3NyZl9p%250AZCIlNzQ2Mzg4ZTM5ODYzOTAxY2I3ZWM2YjRjNTRkYWQ1YTE6B2lkIiUyN2Uy%250ANjE3MzIzZmY0OTYzNDNhNDY5MTMwMDdkYTY5MQ%253D%253D--3cf6a17c9d77e47d3bc3731964da5b89ff7de02d; kdt=UANhrHFuDXkxjTcjAOgq9DIF5QLSJdxD1OElHybR; auth_token=5cd2e6077966875d663293e4101b96fbedb5818b; guest_id_ads=v1%3A169998054129071930; guest_id_marketing=v1%3A169998054129071930; twid=u%3D767620711414456320; night_mode=1; _gid=GA1.2.1404017273.1700157076; external_referer=8e8t2xd8A2w%3D|0|S38otfNfzYt86Dak8Eqj76tqscUAnK6Lq4vYdCl5zxIvK6QAA8vRkA%3D%3D; personalization_id="v1_RNfcK33XsKXEecyPCIlgXw=="',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


def get_csrf():
    response = requests.get(url, headers=setting.headers)
    response_headers = response.headers
    for header, value in response_headers.items():
        if header == "set-cookie":
            index = value.index("ct0=") + 4
            token = value[index:].split(";")[0]
            print("---------------csrf token updated!---------------")
            print(token)
            return token
    raise Exception("no csrf token found!")

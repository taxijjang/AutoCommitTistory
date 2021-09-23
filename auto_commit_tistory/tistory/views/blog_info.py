import json

import requests

from config.secret import SECRET


def get_blog_info():
    blog_info_url = (
        "https://www.tistory.com/apis/blog/info?"
        f"access_token={SECRET['tistory']['access_token']}"
        f"&output={SECRET['tistory']['output_type']}"
    )

    req = requests.get(blog_info_url)
    blog_info_json = json.loads(req.text)

    return blog_info_json


def get_blog_name():
    blog_info_json = get_blog_info()
    return blog_info_json['tistory']['item']['blogs'][0].get('name')

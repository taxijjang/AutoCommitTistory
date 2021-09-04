import json
from typing import *

import requests

from .blog_info import get_blog_info
from config.secret import SECRET

from tistory.models import Post


def get_post_list(page: int = 1) -> Dict:
    blog_info = get_blog_info()
    blog_name = blog_info['tistory']['item']['blogs'][0].get('name')
    post_list_url = (
        "https://www.tistory.com/apis/post/list?"
        f"access_token={SECRET['tistory']['access_token']}"
        f"&output={SECRET['tistory']['output_type']}"
        f"&blogName={blog_name}"
        f"&page={page}"
    )

    req = requests.get(post_list_url)
    post_list_json = json.loads(req.text)
    return post_list_json


def save_post():
    post_list_json = get_post_list()
    tistory = post_list_json.get('tistory')
    items = tistory.get('item')
    page = items.get('page')
    count = items.get('count')
    total_count = items.get('totalCount')
    posts = items.get('posts')

    print(tistory)
    print(items)
    print(page)
    print(count)
    print(total_count)
    print(posts)

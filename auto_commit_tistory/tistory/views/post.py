import json
from typing import *

import requests

from .blog_info import get_blog_info
from config.secret import SECRET

from tistory.models import Post


def get_post_list(page: int = 1) -> Dict[str, str]:
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


def save_post_object() -> List[int]:
    page_cnt = 1
    post_list_json = get_post_list(page_cnt)
    count = int(post_list_json.get('tistory').get('item').get('count'))
    total_count = int(post_list_json.get('tistory').get('item').get('totalCount'))

    max_page = total_count // count if total_count % count == 0 else total_count // count + 1

    new_post_list = []

    for page_cnt in range(max_page, 0, -1):
        post_list_json = get_post_list(page_cnt)
        items = post_list_json.get('tistory').get('item')
        posts = items.get('posts')

        for post in posts:
            obj, create = Post.objects.get_or_create(**post)
            if create:
                new_post_list.append(obj.pk)
    return new_post_list

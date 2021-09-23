import json
import re
from typing import *
from html.parser import HTMLParser

import requests

from django.utils import html

from .blog_info import get_blog_info
from .blog_info import get_blog_name
from config.secret import SECRET

from tistory.models import Post


def get_post_list(page:int = 1):
    blog_name = get_blog_name()
    post_list_url = (
        "https://www.tistory.com/apis/post/list?"
        f"access_token={SECRET['tistory']['access_token']}"
        f"&output={SECRET['tistory']['output_type']}"
        f"&blogName={blog_name}"
        f"&page={page}"
    )
    req = requests.get(post_list_url)
    return json.loads(req.text)

    # req = requests.get(post_list_url)
    # data = json.loads(req.text)
    # tistory = data.get('tistory')
    # item = tistory.get('item')
    # posts = item.get('posts')
    # return json.loads(posts)


def get_post_max_page():
    post_list_json = get_post_list()
    count = int(post_list_json.get('tistory').get('item').get('count'))
    total_count = int(post_list_json.get('tistory').get('item').get('totalCount'))

    max_page = total_count // count if total_count % count == 0 else total_count // count + 1

    return max_page


def get_post_id_list(page: int = 1) -> Dict[str, str]:
    post_list_json = get_post_list()
    post_id_list = list(map(int, re.findall(r'\d+', ''.join(re.findall(r'"id": "\d+', json.dumps(post_list_json))))))
    return post_id_list


def get_post_content(post_id, blog_name):
    post_content_url = (
        "https://www.tistory.com/apis/post/read?"
        f"access_token={SECRET['tistory']['access_token']}"
        f"&blogName={blog_name}"
        f"&postId={post_id}"
    )

    req = requests.get(post_content_url)
    data = json.loads(req.text)
    return data.get('item')


def save_post_object():
    max_page = get_post_max_page()
    for page_cnt in range(max_page, 0, -1):
        posts = get_post_list(page_cnt).get('tistory').get('item').get('posts')
        for post in posts:
            Post.objects.get_or_create(**post)
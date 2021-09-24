import re
import json
from json import JSONDecodeError
from typing import *

import requests

from environ import environ_data
from blog_info import get_blog_name


def get_post_list(page: int = 1):
    blog_name = get_blog_name()
    post_list_url = (
        "https://www.tistory.com/apis/post/list?"
        f"access_token={environ_data()['ACCESS_TOKEN']}"
        f"&output={environ_data()['OUTPUT_TYPE']}"
        f"&blogName={blog_name}"
        f"&page={page}"
    )
    req = requests.get(post_list_url)
    return json.loads(req.text)


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
        f"access_token={environ_data()['ACCESS_TOKEN']}"
        f"&blogName={blog_name}"
        f"&postId={post_id}"
    )

    req = requests.get(post_content_url)
    data = json.loads(req.text)
    return data.get('item')


def get_all_post_data():
    posts = dict()
    max_page = get_post_max_page()
    for page_cnt in range(max_page, 0, -1):
        now_page_posts = get_post_list(page_cnt).get('tistory').get('item').get('posts')
        for now_page_post in now_page_posts:
            posts[int(now_page_post.get('id'))] = now_page_post
    posts = dict(sorted(posts.items()))
    return posts


def get_check_new_post():
    try:
        with open('posts.json', 'r') as f:
            posts_data = json.load(f)
    except JSONDecodeError:
        posts_data = dict()

    new_posts = dict()
    tistory_posts = get_all_post_data()

    for id, data in tistory_posts.items():
        if not posts_data.get(id):
            new_posts[id]=data
    return new_posts



# def make_post_json_file():
#     posts_data = get_all_post_data()
#     with open('posts.json', 'w') as f:
#         json.dumps(posts_data, f)
#
#     data
# def save_post_object():
#     max_page = get_post_max_page()
#     for page_cnt in range(max_page, 0, -1):
#         posts = get_post_list(page_cnt).get('tistory').get('item').get('posts')
#         for post in posts:
#             Post.objects.get_or_create(**post)
#
#
# def make_post_md():
#     posts = Post.objects.order_by('id').filter(auto_commit=False)
#     filepath = str(Path(__file__).parents[3]) + '/posts'
#
#     for post in posts:
#         try:
#             f = open(f'{filepath}/{post.id}-{post.title}.md', 'w', encoding="UTF8")
#             f.write(f'Bot에 의하여 생성된 파일 입니다. \n')
#             f.write(f'### {post.title} \n')
#             f.write(f'- {post.postUrl} \n')
#             f.write(f'- {post.date} \n')
#             f.close()
#             post.auto_commit = True
#             post.save()
#         except Exception:
#             post.auto_commit = False
#             post.save()

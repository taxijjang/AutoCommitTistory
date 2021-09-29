import os
import json
from json import JSONDecodeError

import requests

from environ import environ_data
from blog_info import Tistory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_post_list(page: int = 1):
    """
    티스토리 open api를 이용하여
    내가 작성한 블로그 글 목록을 가지고 오는 함수
    :param page: 현재 보고자 하는 글 목록의 page 번호
    :return: 현재 글 목록을 가지고 있는 page의 data를 dict로 변환
    """
    blog_name = Tistory.get_blog_name()
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
        with open(os.path.join(BASE_DIR, 'posts.json'), "r") as f:
            posts_data = json.load(f)
    except JSONDecodeError:
        # json file is empty
        posts_data = dict()
    new_posts = dict()
    tistory_posts = get_all_post_data()
    for id, data in tistory_posts.items():
        # post is not visibility
        if not data.get('visibility'):
            continue
        id = str(id)
        if not posts_data.get(id):
            posts_data[id] = data
            new_posts[id] = data

    # make now posts_data in json file
    with open(os.path.join(BASE_DIR, "posts.json"), 'w', encoding='utf-8') as make_file:
        json.dump(posts_data, make_file, ensure_ascii=False, indent="\t")
    return new_posts


def get_issue_body():
    new_posts = get_check_new_post()
    upload_issue_body = ''
    for key, value in new_posts.items():
        id = value.get('id')
        title = value.get('title')
        post_url = value.get('postUrl')
        create_at = value.get('date')

        content = f'{id} - <a href={post_url}>{title}</a>, {create_at} <br/>\n'
        upload_issue_body += content
    return new_posts, upload_issue_body

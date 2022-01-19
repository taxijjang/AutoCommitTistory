import os
import json
from json import JSONDecodeError

import requests

from blog_info import Tistory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Post:
    PRIVATE = 0
    PENDING = 15
    PUBLIC = 20

    def __init__(self, access_token):
        """
        init post class
        :param access_token: tistory에서 발급 받은 access_token
        """
        self._access_token = access_token

    def post_list(self, page=1):
        """
        Tistory open api를 이용하여
        내가 작성한 블로그 글 목록을 가지고 오는 함수
        :param page: 현재 보고자 하는 글 목록의 page 번호
        :return: 현재 글 목록을 가지고 있는 page의 data를 dict로 변환
        """
        blog_name = Tistory.get_blog_name(access_token=self._access_token)
        post_list_url = (
            "https://www.tistory.com/apis/post/list?"
            f"access_token={self._access_token}"
            f"&output=json"
            f"&blogName={blog_name}"
            f"&page={page}"
        )
        req = requests.get(post_list_url)
        return json.loads(req.text)

    def post_max_page(self):
        """
        해당 유저의 access_token을 이용하여 post의 목록 data를 가지고 온 후에
        post 목록 api에서 제공해주는 pagination 최대 page를 구하는 함수
        :return: api에서 제공해주는 pagination의 최대 page
        """
        post_list_json = self.post_list()
        count = int(post_list_json.get('tistory').get('item').get('count'))
        total_count = int(post_list_json.get('tistory').get('item').get('totalCount'))
        return total_count // count if total_count % count == 0 else total_count // count + 1

    def all_post_data(self):
        posts = dict()
        max_page = self.post_max_page()
        for page_cnt in range(max_page, 0, -1):
            now_page_posts = self.post_list(page_cnt).get('tistory').get('item').get('posts')
            for now_page_post in now_page_posts:
                if int(now_page_post.get('visibility')) != self.PUBLIC:
                    continue
                posts[int(now_page_post.get('id'))] = now_page_post
        return dict(sorted(posts.items()))

    def check_new_post(self):
        try:
            with open(os.path.join(BASE_DIR, 'posts.json'), "r") as f:
                json_data = json.load(f)
                if json_data.get('username') != os.environ.get('USERNAME'):
                    # When you are a new author
                    print("기존에 작성된 posts.json의 사용자와 다른 사용자 입니다.")
                    raise FileNotFoundError
        except (FileNotFoundError, JSONDecodeError):
            # json file is empty
            json_data = dict()
            json_data['username'] = os.environ.get('USERNAME')
            json_data['posts'] = dict()

        new_posts = dict()
        tistory_posts = self.all_post_data()
        for post_id, data in tistory_posts.items():
            # post is not visibility
            if int(data.get('visibility')) != self.PUBLIC:
                continue
            post_id = str(post_id)
            if not json_data.get('posts').get(post_id):
                json_data['posts'][post_id] = data
                new_posts[post_id] = data

        # make now posts_data in json file
        print(json_data)
        with open(os.path.join(BASE_DIR,'posts.json'), 'w', encoding='utf-8') as make_file:
            json.dump(json_data, make_file, ensure_ascii=False, indent="\t")
        return new_posts

    def issue_body(self):
        new_posts = self.check_new_post()
        upload_issue_body = ''
        for key, value in new_posts.items():
            if int(value.get('visibility')) != self.PUBLIC:
                continue
            id = value.get('id')
            title = value.get('title')
            post_url = value.get('postUrl')
            create_at = value.get('date')

            content = f'{id} - <a href={post_url}>{title}</a>, {create_at} <br/>\n'
            upload_issue_body += content
        return new_posts, upload_issue_body

import json

import requests


class Tistory:
    @staticmethod
    def get_blog_name(access_token):
        """
        tistory access_token를 이용하여
        해당 유저 블로그의 이름을 반환하는 함수
        :return: 해당 유저 블로그 이름
        """
        blog_info_url = (
            "https://www.tistory.com/apis/blog/info?"
            f"access_token={access_token}"
            f"&output=json"
        )

        req = requests.get(blog_info_url)
        blog_info_json = json.loads(req.text)
        return blog_info_json['tistory']['item']['blogs'][0].get('name')

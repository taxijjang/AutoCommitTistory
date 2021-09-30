import os
from datetime import datetime
from pytz import timezone

from github_utils import GithubUtil
from post import Post

"""
* 환경 변수 * 

- github
MY_GITHUB_ACCESS_TOKEN: settings에서 발급한 access token

- tistory
APP_ID: 발급된 app_id
SECRET_KEY: secret_key
STATE_PARAM: state_param
REDIRECT_URI: 본인 티스토리 주소를 입력합니다 ex) https://taxijjang.tistory.com
ACCESS_TOKEN
USERNAME: 이슈에 남길 이름 ex)USERNAME의 블로그
REPO_NAME: 해당 프로젝트가 포함되어 있는 github repository의 이름
JSON_FILE_NAME: tistory api로 가지고 온 post의 정보가 저장되는 file의 이름 ex) JSON_FILE_NAME.json
"""


def main():
    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime('%Y년 %m월 %d일')
    today_date_eng = today.strftime('%Y/%m/%d')
    issue_title = f'{os.environ.get("USERNAME")} TISTORY 새로운 포스팅 알림({today_date})'

    repository_name = os.environ.get('REPO_NAME')
    path = f'{os.environ.get("REPO_NAME")}/{os.environ.get("JSON_FILE_NAME")}.json'
    access_token = os.environ.get('MY_GITHUB_ACCESS_TOKEN')

    github_util = GithubUtil(access_token=access_token)

    # set my repository
    github_util.set_github_repo(repository_name=repository_name)

    # post objects
    post = Post(
        access_token=os.environ.get('ACCESS_TOKEN'),
        json_file_name=os.environ.get('JSON_FILE_NAME')
    )

    # get new_post
    new_posts, upload_issue_body = post.issue_body()

    # no new posts today
    if not upload_issue_body:
        print(f'{today_date} 블로그 포스팅 목록이 없습니다.')
        return None

    # upload new issue
    github_util.upload_github_issue(title=issue_title, body=upload_issue_body, labels=['new_posting'])
    print(f'{today_date} 블로그 포스팅 목록 Issue 등록 성공!')

    # upload new json file push
    github_util.upload_github_push(message=f'Add new posting {today_date_eng}',
                                   content=new_posts, path=path, branch='master')
    print(f'{today_date} {os.environ.get("JSON_FILE_NAME")} push 성공!')
    return None


if __name__ == '__main__':
    main()
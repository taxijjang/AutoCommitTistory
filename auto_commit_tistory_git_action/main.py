import os
from datetime import datetime
from pytz import timezone

from post import get_issue_body
from environ import environ_data
from github_utils_re import GithubUtil


def main():
    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime('%Y년 %m월 %d일')
    today_date_eng = today.strftime('%Y/%m/%d')
    issue_title = f'{environ_data().get("USERNAME")} TISTORY 새로운 포스팅 알림({today_date})'

    repository_name = "AutoCommitTistory"
    path = 'auto_commit_tistory_git_action/posts.json'
    access_token = environ_data().get('MY_GITHUB_ACCESS_TOKEN')

    github_util = GithubUtil(access_token=access_token)

    # set my repository
    github_util.set_github_repo(repository_name=repository_name)

    # get new_post
    new_posts, upload_issue_body = get_issue_body()

    if upload_issue_body:
        # upload new issue
        github_util.upload_github_issue(title=issue_title, body=upload_issue_body, labels=['new_posting'])
        print(f'{today_date} 블로그 포스팅 목록 Issue 등록 성공!')

        # upload new posts.json push
        github_util.upload_github_push(message=f'Add new posting {today_date_eng}',
                                       content=new_posts, path=path, branch='master')
        print(f'{today_date} posts.json push 성공!')
        return None
    print(f'{today_date} 블로그 포스팅 목록이 없습니다.')
    return None


if __name__ == '__main__':
    main()

from datetime import datetime
from pytz import timezone

from post import get_issue_body
from environ import environ_data
from github_utils import get_github_repo
from github_utils import upload_github_issue


def main():
    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime('%Y년 %m월 %d일')
    issue_title = f'택시짱의 TISTORY 새로운 포스팅 알림({today_date})'

    repository_name = "AutoCommitTistory"
    access_token = environ_data().get('MY_GITHUB_ACCESS_TOKEN')

    repo = get_github_repo(access_token=access_token, repository_name=repository_name)

    upload_issue_body = get_issue_body()
    if upload_issue_body:
        upload_github_issue(repo=repo, title=issue_title, body=upload_issue_body)
        print(f'{today_date} 블로그 포스팅 목록 Issue 등록 성공!')
        return None
    print(f'{today_date} 블로그 포스팅 목록이 없습니다.')
    return None


if __name__ == '__main__':
    main()

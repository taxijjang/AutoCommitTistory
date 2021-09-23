import os
from datetime import datetime
from pytz import timezone

if __name__ == '__main__':
    access_token = os.environ['MY_GITHUB_ACCESS_TOKEN']
    app_id = os.environ['APP_ID']
    secret_key = os.environ['SECRET_KEY']
    state_param = os.environ['STATE_PARAM']
    redirect_uri = os.environ['REDIRECT_URI']
    output_type = os.environ['OUTPUT_TYPE']
    access_token = os.environ['ACCESS_TOKEN']

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime('%년 %m월 %d일')
    issue_title = f'택시짱의 TISTORY 새로운 포스팅 알림({today_date})'

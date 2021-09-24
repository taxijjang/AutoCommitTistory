from datetime import datetime
from pytz import timezone

from post import get_all_post_data
from post import get_check_new_post

def main():
    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime('%년 %m월 %d일')
    issue_title = f'택시짱의 TISTORY 새로운 포스팅 알림({today_date})'

    print(get_check_new_post())


if __name__ == '__main__':
    main()

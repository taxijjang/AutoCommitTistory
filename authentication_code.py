import os
import requests


def get_authentication_code():
    auth_url = (
        'https://www.tistory.com/oauth/authorize?'
        f'client_id={os.environ.get("APP_ID")}'
        f'&response_type=code'
        f'&redirect_uri={os.environ.get("REDIRECT_URI")}'
        f'&state={os.environ.get("STATE_PARAM")}'
    )

    req = requests.get(auth_url)

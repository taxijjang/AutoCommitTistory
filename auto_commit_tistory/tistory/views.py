import re
import webbrowser

import requests
from bs4 import BeautifulSoup

from config.secret import SECRET

def authentication_code():
    auth_url = (
        'https://www.tistory.com/oauth/authorize?'
        f'client_id={SECRET["tistory"]["app_id"]}'
        f'&response_type=code'
        f'&redirect_uri={SECRET["tistory"]["redirect_uri"]}'
        f'&state={SECRET["tistory"]["state_param"]}'
    )

    req = requests.get(auth_url)
    webbrowser.open(auth_url)
    print(webbrowser)

def get_access_token():
    code = '67dabfe3d9625b8df63ac0f5ec2544e577690a9e9c08dcef7bd2a587b32f1584e6ed2477'
    access_token_url = (
        'https://www.tistory.com/oauth/access_token?'
        f'client_id={SECRET["tistory"]["app_id"]}'
        f'&client_secret={SECRET["tistory"]["secret_key"]}'
        f'&redirect_uri={SECRET["tistory"]["redirect_uri"]}'
        f'&code=61ffbad0257bcfee3b1af891f314631df286a5434dafc560d93b683c0f337295d4f8acff'
        f'&grant_type=authorization_code'
    )

    req = requests.get(access_token_url)
    print(req)
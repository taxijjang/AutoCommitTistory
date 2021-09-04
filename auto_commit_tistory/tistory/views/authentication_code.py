import re
import json

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from config.secret import SECRET


def get_authentication_code():
    auth_url = (
        'https://www.tistory.com/oauth/authorize?'
        f'client_id={SECRET["tistory"]["app_id"]}'
        f'&response_type=code'
        f'&redirect_uri={SECRET["tistory"]["redirect_uri"]}'
        f'&state={SECRET["tistory"]["state_param"]}'
    )

    req = requests.get(auth_url)

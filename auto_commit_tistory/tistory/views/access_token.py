import requests

from config.secret import SECRET


def get_access_token():
    # access token 획득시 소멸되는 1회용 code
    code = '620834d8ff9baa5020474a4b9e76e6c5b03df56a24dbef0280d51d92b9fc64558ef8ce68'
    access_token_url = (
        'https://www.tistory.com/oauth/access_token?'
        f'client_id={SECRET["tistory"]["app_id"]}'
        f'&client_secret={SECRET["tistory"]["secret_key"]}'
        f'&redirect_uri={SECRET["tistory"]["redirect_uri"]}'
        f'&code={code}'
        f'&grant_type=authorization_code'
    )

    req = requests.get(access_token_url)
    print("abce")

import requests

from config.secret import SECRET


def get_access_token():
    # access token 획득시 소멸되는 1회용 code
    code = 'a348a876bf49b7a9a4e01f2018b7ce008d23e92a621e79b59ecea3829de0b6c7046784dd'
    access_token_url = (
        'https://www.tistory.com/oauth/access_token?'
        f'client_id={SECRET["tistory"]["app_id"]}'
        f'&client_secret={SECRET["tistory"]["secret_key"]}'
        f'&redirect_uri={SECRET["tistory"]["redirect_uri"]}'
        f'&code={code}'
        f'&grant_type=authorization_code'
    )

    print(access_token_url)
    req = requests.get(access_token_url)
    print("ASDF")
    # print)
    # print("abce")

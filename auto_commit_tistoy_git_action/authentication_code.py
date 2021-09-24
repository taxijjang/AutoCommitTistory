from playwright.sync_api import sync_playwright

from environ import environ_data

def get_authentication_code():
    print("ASDF")
    auth_url = (
        'https://www.tistory.com/oauth/authorize?'
        f'client_id={environ_data()["APP_ID"]}'
        f'&response_type=code'
        f'&redirect_uri={environ_data()["REDIRECT_URI"]}'
        f'&state={environ_data()["STATE_PARAM"]}'
    )

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(auth_url)
        print(page)
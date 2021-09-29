import os


def environ_data():
    environ_datas = dict(
        MY_GITHUB_ACCESS_TOKEN=os.environ.get('MY_GITHUB_ACCESS_TOKEN'),
        APP_ID=os.environ.get('APP_ID'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        STATE_PARAM=os.environ.get('STATE_PARAM'),
        REDIRECT_URI=os.environ.get('REDIRECT_URI'),
        OUTPUT_TYPE=os.environ.get('OUTPUT_TYPE'),
        ACCESS_TOKEN=os.environ.get('ACCESS_TOKEN'),
        USERNAME=os.environ.get('USERNAME')
    )

    return environ_datas

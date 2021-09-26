import os


def environ_data():
    environ_data = dict(
        MY_GITHUB_ACCESS_TOKEN=os.environ['MY_GITHUB_ACCESS_TOKEN'],
        APP_ID=os.environ['APP_ID'],
        SECRET_KEY=os.environ['SECRET_KEY'],
        STATE_PARAM=os.environ['STATE_PARAM'],
        REDIRECT_URI=os.environ['REDIRECT_URI'],
        OUTPUT_TYPE=os.environ['OUTPUT_TYPE'],
        ACCESS_TOKEN=os.environ['ACCESS_TOKEN'],
    )

    return environ_data

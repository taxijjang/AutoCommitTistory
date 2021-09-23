from __future__ import absolute_import
from config.celery import app
import time

from tistory.models import Post
from tistory.views import get_post_max_page, get_post_list





@app.task
def longtime_add(x, y):
    print('long time')

    time.sleep(5)
    print('asdf')
    return x + y
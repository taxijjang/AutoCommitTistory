from celery import Celery

app = Celery('config',
             broker='amqp://localhost:15672',
             backend='rpc://',
             include=['tistory.tasks'])

app.conf.update(
    result_expires=3600,
)

if __name__=='__main__':
    app.start()
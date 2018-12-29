from celery import Celery

app = Celery('sns')

@app.task
def add(x, y):
    return x + y
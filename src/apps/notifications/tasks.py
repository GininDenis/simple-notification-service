import requests

from conf.celery_app import app


@app.task
def send_subscription_confirmation(message, endpoint):
    rs = requests.post(endpoint, data=message)
    if rs.status_code == 200:
        return True

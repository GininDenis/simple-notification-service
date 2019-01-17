from conf.celery_app import app


def confirm_subscription(**kwargs):
    instance = kwargs.get('instance')
    app.send_task(
        'apps.notifications.tasks.send_subscription_confirmation',
        args=[instance.id]
    )

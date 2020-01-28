from api.sms import DailySms


def my_scheduled_job():
    DailySms()
    # send_mail('Celery Task Worked!', 'This is proof the task worked!', settings.DEFAULT_FROM_EMAIL, [to])

import time

from celery import Celery

from _15thnight.email_client import send_email
from _15thnight.models import Alert, Category, User
from _15thnight.slack import SlackBot
from _15thnight.twilio_client import send_sms

try:
    from config import (
        CELERY_BROKER, HOST_NAME, SLACKBOT_TOKEN, SLACKUSER_TOKEN)
except:
    from configdist import (
        CELERY_BROKER, HOST_NAME, SLACKBOT_TOKEN, SLACKUSER_TOKEN)


celery = Celery('15thnight', broker=CELERY_BROKER)
slack_bot = SlackBot(SLACKBOT_TOKEN, SLACKUSER_TOKEN)


def init_app(app):
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask


@celery.task
def queue_send_alert(alert_form, user):
    """
    Celery task to send messages out in all forms.
    """
    alert = Alert(
        description=alert_form.description.data,
        gender=alert_form.gender.data,
        age=alert_form.age.data,
        user=user,
        categories=Category.get_by_ids(alert_form.categories.data).all()
    )
    alert.save()
    providers = User.users_in_categories(alert_form.categories.data)
    for user in providers:
        body = ('%s, there is a new 15th night alert.\n'
                'Go to %s/respond_to/%s to respond.') % (
                    user.email, HOST_NAME, str(alert.id))
        send_sms(to_number=user.phone_number, body=body)
        send_email(user.email, '15th Night Alert', body)

    slack_bot.send_alert(alert)


@celery.task()
def start_listening(cls):
    cls.categories.add_existing_channels()

    if cls.sc.rtm_connect():
        while True:
            msgs = cls.sc.rtm_read()
            for msg in msgs:
                if msg.get("type") == "message":
                    msg_burst = msg.get("text").split(" ")
                    # We want only
                    if len(msg_burst) < 2:
                        continue
                    try:
                        if str(int(msg_burst[0])) != msg_burst[0]:
                            continue
                    except:
                        continue

                    alert_id = msg_burst[0]
                    # We are sure it's a properly formatted response, handle it
                    cls.accept_response(msg, alert_id)
                else:
                    print("MSG:\n%s" % msg)

            time.sleep(5)
    else:
        print("RTM Connection Failed!")

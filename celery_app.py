from _15thnight.queue import slack_bot
from _15thnight.queue import celery
from _15thnight.queue import start_listening

start_listening.apply_async([slack_bot], countdown=1)

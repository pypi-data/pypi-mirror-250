from celery import shared_task
from slack_sdk.web.client import WebClient

from dsbot.conf import settings
from dsbot.decorators import api_error

client = WebClient(token=settings.SLACK_TOKEN)


# Wrapped version of Slack API Calll
# We want to make it easy to rate limit our calls to slack by wrapping
# it as a shared_task.
@shared_task(rate_limit=settings.SLACK_RATE_LIMIT)
@api_error
def api_call(*args, **kwargs):
    return client.api_call(*args, json=kwargs).data

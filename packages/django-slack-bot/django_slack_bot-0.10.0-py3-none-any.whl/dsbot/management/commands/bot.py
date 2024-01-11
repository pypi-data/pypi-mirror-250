import logging
import os

from django.core.management.base import BaseCommand
from django.test import override_settings
from slack_sdk.web import WebClient

from dsbot.client import BotClient


class Command(BaseCommand):
    def add_arguments(self, parser):
        slack = parser.add_argument_group("Slack arguments")
        slack.add_argument("--app-token", default=os.environ.get("SLACK_APP_TOKEN"))
        slack.add_argument("--bot-token", default=os.environ.get("SLACK_BOT_TOKEN"))
        slack.add_argument("--timeout", default=30, type=int)
        slack.add_argument("--ping-interval", default=30, type=int)

        celery = parser.add_argument_group("Celery Arguments")
        celery.add_argument("--eager", action="store_true")

    def handle(self, verbosity, eager, **options):
        logging.root.setLevel(
            {
                0: logging.ERROR,
                1: logging.WARNING,
                2: logging.INFO,
                3: logging.DEBUG,
            }.get(verbosity)
        )

        ch = logging.StreamHandler()
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        ch.setFormatter(formatter)

        logging.root.addHandler(ch)

        BotClient.load_plugins()

        with override_settings(CELERY_TASK_ALWAYS_EAGER=eager):
            BotClient(
                app_token=options["app_token"],
                ping_interval=options["ping_interval"],
                web_client=WebClient(
                    token=options["bot_token"],
                    timeout=options["timeout"],
                ),
            ).start()

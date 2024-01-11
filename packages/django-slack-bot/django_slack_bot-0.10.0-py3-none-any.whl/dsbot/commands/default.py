"""
These are the core commands and events that typically require a greater
knowledge about the internals of the bot itself
"""

import logging

from django.template.loader import render_to_string
from slack_sdk.socket_mode.builtin import SocketModeClient

from dsbot.client import BotClient
from dsbot.decorators import ignore_subtype
from dsbot.util import parse_direct_mention

logger = logging.getLogger(__name__)


@BotClient.cmd("^help")
async def cmd_help(client: SocketModeClient, message: dict, **kwargs):
    """
    help - Show list of commands

    The help command loops through all registered dispatch commands and
    formats their help output via django's render_to_string method
    """
    commands = client._SocketAdapter__dispatcher[BotClient.EVENT_COMMAND]
    return client.web_client.chat_postEphemeral(
        channel=message["channel"],
        as_user=True,
        text=render_to_string(
            "slack/response/help.txt",
            # In theory, we shouldn't need to use a comprehension here, but
            # currently something is not rendering right in the django template
            # and it's not worth debugging further for now.
            {"mapping": [{"key": c.key, "help": c.help} for c in commands]},
        ).strip(),
        user=message["user"],
    )


@BotClient.run_on(event="hello")
def lookup_user_id(client: SocketModeClient, **kwargs):
    response = client.web_client.auth_test()
    setattr(client, "user_id", response.data["user_id"])
    logger.info("Bot is %s", client.user_id)


@BotClient.run_on(event="message")
@ignore_subtype
def command_checker(*, client, message, **kwargs):
    """
    Basic command dispatch

    We want our bot to be a good citizen, so in public channels
    we only want it to respond to a direct @-mention

    In the case of direct private messages, we don't want to
    require @-mention, since it's obvious it's a command directly
    to the bot
    """

    # Check to see if this is an @ message
    user_id, command = parse_direct_mention(message["text"])
    if user_id == client.user_id:
        # An @ message directly to the bot should be processed with the mention
        # stripped off.
        return client.dispatch(
            BotClient.EVENT_COMMAND,
            command=command,
            message=message,
            client=client,
            **kwargs,
        )
    # Or a direct message
    if message["channel"].startswith("D"):
        # A direct message to the bot can process the entire message text
        return client.dispatch(
            BotClient.EVENT_COMMAND,
            command=message["text"],
            message=message,
            client=client,
            **kwargs,
        )

    # Otherwise we ignore it to be a good citizen
    logger.debug("Ignoring non @ message in public channel %s", message)

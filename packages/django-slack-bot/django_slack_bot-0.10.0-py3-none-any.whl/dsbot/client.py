"""
Base Bot Class

The base bot class is mostly concerned with maintaining
the connection to Slack, and then dispatching events to
the Dispatcher

A few convenience functions used by commands are also
added to the bot class
"""
import inspect
import logging
import re
from functools import wraps

from asgiref.sync import async_to_sync

from dsbot import decorators
from dsbot.adapter import SocketAdapter

try:
    from importlib_metadata import entry_points
except ImportError:
    from importlib.metadata import entry_points


logger = logging.getLogger(__name__)


class BotClient(SocketAdapter):
    EVENT_COMMAND = "command"

    @classmethod
    def cmd(cls, key):
        """
        A decorator to store and link a callback to an event.

        Commands are wrapped so that they only match on the provided regex and
        then they are put onto the listener for command events.

        We also set attributes for key and help to be used by the `help` command
        """
        regex = re.compile(key)

        def decorator(callback):
            help = callback.__doc__.strip().split("\n")[0]
            if inspect.iscoroutinefunction(callback):
                callback = async_to_sync(callback)
            callback = decorators.command(callback)

            @wraps(callback)
            def command_wrapper(*args, command, **kwargs):
                if match := regex.match(command):
                    return callback(*args, match=match, **kwargs)

            command_wrapper.key = key
            command_wrapper.help = help
            cls.register(cls.EVENT_COMMAND, command_wrapper)
            return command_wrapper

        return decorator

    @classmethod
    def load_plugins(cls, group="dsbot.commands"):
        logger.info("Loading plugins for %s", group)
        for entry in entry_points(group=group):
            try:
                entry.load()
            except ImportError:
                logger.exception("Error loading %s", entry)
            else:
                logger.debug("Loaded %s", entry)

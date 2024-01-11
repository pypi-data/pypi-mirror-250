import inspect
import logging
from collections import defaultdict
from pprint import pformat
from threading import Event

from asgiref.sync import async_to_sync
from slack_sdk.socket_mode.builtin import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse

logger = logging.getLogger(__name__)


class SocketAdapter(SocketModeClient):
    """
    SocketAdapter for SocketModeClient

    The previous RTM Client provided a lot of event dispatch for us by default
    however that is missing in the SocketModeClient. This adapter attempts to
    reimplement a similar design so that other bot clients do not have to be
    as aware of the changes.
    """

    __dispatcher = defaultdict(set)

    def __init__(self, *args, **kwargs):
        # self.client = SocketModeClient(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.message_listeners.append(self.__on_message)
        self.socket_mode_request_listeners.append(self.__on_request)

    def start(self):
        logger.info("Starting bot")
        self.connect()
        try:
            Event().wait()
        except KeyboardInterrupt:
            logger.info("Exiting on KeyboardInterrupt")

    def __on_request(self, *args, **kwargs):
        logger.debug("on_request: %s %s", args, kwargs)

    def __on_message(self, client, message: dict, raw_message: str):
        logger.debug("on_message:\n%s", raw_message)
        self.dispatch(
            message["type"],
            client=client,
            req=SocketModeRequest.from_dict(message),
        )

    def dispatch(self, event, **kwargs):
        logger.debug("Dispatching '%s': \n%s", event, kwargs)
        for listener in self.__dispatcher[event]:
            try:
                if inspect.iscoroutinefunction(listener):
                    async_to_sync(listener(**kwargs))
                else:
                    listener(**kwargs)
            except TypeError:
                logger.exception("Error dispatching to %s", listener)

    @classmethod
    def register(cls, event, callback):
        """
        Register a given callback on a specific event queue
        """
        cls.__dispatcher[event].add(callback)
        return callback

    @classmethod
    def run_on(cls, *, event: str):
        """A decorator to store and link a callback to an event."""

        def decorator(callback):
            return cls.register(event, callback)

        return decorator


# https://slack.dev/python-slack-sdk/socket-mode/index.html
@SocketAdapter.run_on(event="events_api")
def events_api(*, client=SocketModeClient, req: SocketModeRequest, **kwargs):
    """
    Process events_api events

    This is part of the glue that lets our new SocketModeAdapter mimic the
    general flow of the RTMClient. Process incoming events and convert them
    into an equivilant of the previous RTMClient message type.
    """
    if req.type == "events_api":
        # Acknowledge the request anyway
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)
        if req.payload["event"]["type"] == "message":
            # Compatibility mode for RTM Client
            # these extra values are needed for compatibility mode but will
            # be removed in a future update
            kwargs["data"] = req.payload["event"]
            kwargs["web_client"] = client.web_client
            kwargs["rtm_client"] = client
            client.dispatch(
                "message",
                client=client,
                message=req.payload["event"],
                req=req,
                **kwargs,
            )
    else:
        client.dispatch(req.type, client=client, req=req, **kwargs)


@SocketAdapter.run_on(event="hello")
def debug(client, **kwargs):
    """
    Dispatch Debug Hook

    Show what is currently registered in our dispatcher once the bot loads.
    This can help us debug what commands we expect to be enabled.
    """
    logger.debug("Dispatch %s", pformat(client._SocketAdapter__dispatcher))

#from viberio import types
#from viberio.api.client import ViberBot
from .events import Event, SkipHandler
#from viberio.types import requests, messages
#from viberio.types.requests import EventType
from .utils.mixins import DataMixin, ContextInstanceMixin
from .types import WebsocketEvent

import asyncio
from loguru import logger

class Dispatcher(DataMixin, ContextInstanceMixin):
    def __init__(self, websocket_controller):
        self.websocket_controller = websocket_controller

        self.loop = asyncio.get_event_loop()

        self.update_handlers = Event()
        self.event_handler = Event()
        '''
        self.url_messages_handler = Event()  # URLMessage
        self.location_messages_handler = Event()  # LocationMessage
        self.picture_messages_handler = Event()  # PictureMessage
        self.contact_messages_handler = Event()  # ContactMessage
        self.file_messages_handler = Event()  # FileMessage
        self.text_messages_handler = Event()  # TextMessage
        self.video_messages_handler = Event()  # VideoMessage
        self.sticker_messages_handler = Event()  # StickerMessage
        self.rich_media_messages_handler = Event()  # RichMediaMessage
        self.keyboard_messages_handler = Event()  # KeyboardMessage
        self.failed_handler = Event()  # ViberFailedRequest
        self.conversation_started_handler = Event()  # ViberConversationStartedRequest
        self.delivered_handler = Event()  # ViberDeliveredRequest
        self.seen_handler = Event()  # ViberSeenRequest
        self.subscribed_handler = Event()  # ViberSubscribedRequest
        self.unsubscribed_handler = Event()  # ViberUnsubscribedRequest
        self.request_handler = Event()  # ViberRequest
        self.webhook_handler = Event()  # ViberRequest
        '''

        self._register_default_handlers()

    def _register_default_handlers(self):
        self.update_handlers.subscribe(self._process_event, [])
        #self.messages_handler.subscribe(self._process_message, [])

    @staticmethod
    def parse_request(data: dict):
        return WebsocketEvent(**data)

    def feed_request(self, request):
        return self.loop.create_task(self.update_handlers.notify(request))

    async def _process_event(self, request, data: dict):
        logger.debug(f"processing event {request}")
        if request:
            result = await self.event_handler.notify(request, data)
        else:
            raise SkipHandler()
        if result:
            return result
        raise SkipHandler()

    '''
    #doesnt need
    async def _process_message(self, message_request, data: dict):
        logger.debug(f"processing message {message_request}")
        if message_request:
            result = await self.text_messages_handler.notify(message_request, data)
        else:
            raise SkipHandler()
        if result:
            return result
        raise SkipHandler()
    '''

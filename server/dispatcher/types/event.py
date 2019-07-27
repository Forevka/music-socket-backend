import attr

from ..utils import DataMixin, ContextInstanceMixin

@attr.s
class WebsocketBaseObject(DataMixin, ContextInstanceMixin):
    pass

@attr.s
class WebsocketRequestEvent(WebsocketBaseObject):
    def __init__(self, **entries):
        super(WebsocketRequestEvent, self).__init__()
        self.__dict__.update(entries)
    event: str = attr.ib()
    timestamp: int = attr.ib()
    body: int = attr.ib()

@attr.s
class WebsocketEvent(WebsocketRequestEvent):
    event: str = attr.ib()
    timestamp: int = attr.ib()
    body: int = attr.ib()

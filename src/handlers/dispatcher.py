from dtos.events import Event
from handlers.basic_handler import BasicHandler


class Dispatcher:
    handlers: dict[str, list[BasicHandler]]

    def __init__(self, handlers: dict[str, list[BasicHandler]] = {}) -> None:
        self.handlers = handlers

    def dispatch(self, event_type: str, event: Event) -> None:
        event_handlers = self.handlers.get(event_type)

        if event_handlers:
            for event_handler in event_handlers:
                event_handler.process_event(event)

    def get_events_to_subscribe(self) -> list[str]:
        return list(self.handlers.keys())

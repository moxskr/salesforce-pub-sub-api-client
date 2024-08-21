import typing

from dtos import Event

class BasicHandler(typing.Protocol):
    def process_event(self, event: Event) -> None:
        pass
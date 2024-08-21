from handlers import BasicHandler
from dtos import Event


class PrintHandler(BasicHandler):
    def process_event(self, event: Event) -> None:
        print(event)
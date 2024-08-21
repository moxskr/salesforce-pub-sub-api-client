from dataclasses import dataclass


@dataclass
class Notification:
    to_send_message: bool
    message_type: str | None
    message: str | None
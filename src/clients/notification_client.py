import logging
import typing

from dtos.notifications import Notification


class NotificationClient(typing.Protocol):
    def send_notification(self, notification: Notification) -> None:
        pass


class NotificationClientImpl:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def send_notification(self, notification: Notification) -> None:
        self.logger.info(f'Send message "{notification.message}" using {
            notification.message_type} channel')

import logging
import typing

from dtos.notifications import Notification

logger = logging.getLogger(__name__)


class NotificationClient(typing.Protocol):
    def send_notification(self, notification: Notification) -> None:
        pass


class NotificationClientImpl:
    def send_notification(self, notification: Notification) -> None:
        logger.info(f'Send message "{notification.message}" using {
                    notification.message_type} channel')

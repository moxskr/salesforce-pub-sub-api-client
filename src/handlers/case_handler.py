from dtos import Event
from services import CaseService
from handlers import BasicHandler
from clients.notification_client import NotificationClient
from utils.constants import STATUS_FIELD


class CaseHandler(BasicHandler):
    case_service: CaseService
    notification_client: NotificationClient
    
    def __init__(self, case_service: CaseService, notification_client: NotificationClient) -> None:
        self.case_service = case_service
        self.notification_client = notification_client

    def process_event(self, event: Event) -> None:
        if STATUS_FIELD in event.changed_fields:  
            notification = self.case_service.get_notification(event)
            
            if notification.to_send_message:
                self.notification_client.send_notification(notification)
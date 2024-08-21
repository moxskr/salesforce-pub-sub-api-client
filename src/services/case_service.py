import typing

from dtos import Event
from dtos import Notification
from entities import Case
from utils import constants

messages_by_status = {
    constants.STATUS_NEW: constants.NEW_STATUS_MESSAGE,
    constants.STATUS_WORKING: constants.WORKING_STATUS_MESSAGE,
    constants.STATUS_ESCALATED: constants.ESCALATED_STATUS_MESSAGE,
    constants.STATUS_CLOSED: constants.CLOSED_STATUS_MESSAGE
}


class CaseService(typing.Protocol):
    def get_notification(self, event: Event) -> Notification:
        pass


class CaseServiceImpl(CaseService):
    def get_notification(self, event: Event) -> Notification:
        notification = Notification(
            to_send_message=False, message=None, message_type=None)

        case = Case(
            subject=event.fields.get(constants.SUBJECT_FIELD),
            status=event.fields.get(constants.STATUS_FIELD),
            origin=event.fields.get(constants.ORIGIN_FIELD),
            contact_email=event.fields.get(constants.EMAIL_FIELD),
            contact_phone=event.fields.get(constants.PHONE_FIELD),
        )

        message_type = case.get_message_type()

        if message_type:
            message_template = messages_by_status.get(case.status)

            if message_template:
                notification = Notification(
                    to_send_message=True,
                    message_type=message_type,
                    message=message_template.format(subject=case.subject)
                )

        return notification

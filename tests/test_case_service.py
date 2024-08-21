import pytest

from src.services import CaseServiceImpl
from src.dtos import Event
from src.utils import constants

test_subject = 'Test Subject'


@pytest.fixture
def case_service():
    return CaseServiceImpl()


def create_test_event(change_type, changed_fields, fields):
    return Event(
        change_type=change_type,
        changed_fields=changed_fields,
        fields=fields
    )


def test_case_service_get_notification_message_origin_web(case_service):
    test_event_email_not_blank = create_test_event(
        'Create',
        ['Status'],
        {
            constants.SUBJECT_FIELD: test_subject,
            constants.ORIGIN_FIELD: constants.WEB,
            constants.STATUS_FIELD: constants.STATUS_NEW,
            constants.EMAIL_FIELD: 'test@mail.com'
        }
    )

    test_event_email_blank = create_test_event(
        'Create',
        ['Status'],
        {
            constants.SUBJECT_FIELD: test_subject,
            constants.ORIGIN_FIELD: constants.WEB,
            constants.STATUS_FIELD: constants.STATUS_NEW
        }
    )

    non_empty_notification = case_service.get_notification(
        test_event_email_not_blank)
    empty_notification = case_service.get_notification(test_event_email_blank)

    assert non_empty_notification.to_send_message
    assert non_empty_notification.message_type == constants.EMAIL
    assert non_empty_notification.message == constants.NEW_STATUS_MESSAGE.format(
        subject=test_subject)
    assert not empty_notification.to_send_message


def test_case_service_get_notification_message_origin_email(case_service):
    test_event_email_not_blank = create_test_event(
        'Update',
        ['Status'],
        {
            constants.SUBJECT_FIELD: test_subject,
            constants.ORIGIN_FIELD: constants.EMAIL,
            constants.STATUS_FIELD: constants.STATUS_ESCALATED,
            constants.EMAIL_FIELD: 'test@mail.com'
        }
    )

    test_event_email_blank = create_test_event(
        'Update',
        ['Status'],
        {
            constants.SUBJECT_FIELD: test_subject,
            constants.ORIGIN_FIELD: constants.EMAIL,
            constants.STATUS_FIELD: constants.STATUS_ESCALATED
        }
    )

    non_empty_notification = case_service.get_notification(
        test_event_email_not_blank)
    empty_notification = case_service.get_notification(test_event_email_blank)

    assert non_empty_notification.to_send_message
    assert non_empty_notification.message_type == constants.EMAIL
    assert non_empty_notification.message == constants.ESCALATED_STATUS_MESSAGE.format(
        subject=test_subject)
    assert not empty_notification.to_send_message


def test_case_service_get_notification_message_origin_phone(case_service):
    test_event_phone_not_blank = create_test_event(
        'Update',
        ['Status'],
        {
            constants.SUBJECT_FIELD: test_subject,
            constants.ORIGIN_FIELD: constants.PHONE,
            constants.STATUS_FIELD: constants.STATUS_WORKING,
            constants.PHONE_FIELD: '12345'
        }
    )

    test_event_email_not_blank = create_test_event(
        'Update',
        ['Status'],
        {
            constants.SUBJECT_FIELD: test_subject,
            constants.ORIGIN_FIELD: constants.PHONE,
            constants.STATUS_FIELD: constants.STATUS_WORKING,
            constants.EMAIL_FIELD: 'test@mail.com'
        }
    )

    test_event_phone_blank = create_test_event(
        'Update',
        ['Status'],
        {
            constants.SUBJECT_FIELD: test_subject,
            constants.ORIGIN_FIELD: constants.PHONE,
            constants.STATUS_FIELD: constants.STATUS_WORKING
        }
    )

    non_empty_notification_phone = case_service.get_notification(
        test_event_phone_not_blank
    )
    non_empty_notification_email = case_service.get_notification(
        test_event_email_not_blank
    )
    empty_notification = case_service.get_notification(
        test_event_phone_blank
    )

    assert non_empty_notification_phone.to_send_message
    assert non_empty_notification_phone.message_type == constants.PHONE
    assert non_empty_notification_phone.message == constants.WORKING_STATUS_MESSAGE.format(
        subject=test_subject)
    assert non_empty_notification_email.to_send_message
    assert non_empty_notification_email.message_type == constants.EMAIL
    assert non_empty_notification_email.message == constants.WORKING_STATUS_MESSAGE.format(
        subject=test_subject)
    assert not empty_notification.to_send_message

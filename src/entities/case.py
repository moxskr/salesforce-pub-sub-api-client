from utils import constants


class Case:
    subject: str
    origin: str
    status: str
    contact_email: str | None
    contact_phone: str | None
    
    def __init__(self, subject, origin, status, contact_email=None, contact_phone=None) -> None:
        self.subject = subject
        self.origin = origin
        self.status = status
        self.contact_email = contact_email
        self.contact_phone = contact_phone

    def get_message_type(self) -> str | None:
        message_type = None
        
        if self.origin == constants.PHONE:
            if self.contact_phone:
                message_type = constants.PHONE
            elif self.contact_email:
                message_type = constants.EMAIL
        
        if self.origin == constants.EMAIL or self.origin == constants.WEB:
            if self.contact_email:
                message_type = constants.EMAIL
                
        return message_type
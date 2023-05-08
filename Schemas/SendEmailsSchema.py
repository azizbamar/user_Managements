from pydantic import BaseModel

class SendEmails(BaseModel):
    recipients: list
    subject: str
    body: str
    
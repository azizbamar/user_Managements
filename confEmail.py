from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType



conf = ConnectionConfig(
    MAIL_USERNAME ="azizbenamar",
    MAIL_PASSWORD = "1Skmatadortorkida*",
    MAIL_FROM = "aziz.ben.amar@outlook.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "mail server",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
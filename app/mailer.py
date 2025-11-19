from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from typing import Annotated, Literal

from aiosmtplib import SMTP
from fastapi import Depends
from pydantic import BaseModel

from app.settings import settings


class MailMessage(BaseModel):
    to: str
    subject: str
    body: str
    content_type: Literal["html", "plain"] = "plain"


class Mailer(ABC):
    @abstractmethod
    async def send(self, message: MailMessage) -> None:
        raise NotImplementedError


class SMTPMailerConfig(BaseModel):
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str


class SMTPMailer(Mailer):
    def __init__(self, config: SMTPMailerConfig) -> None:
        self.config = config

    async def send(self, message_config: MailMessage) -> None:
        message = MIMEText(message_config.body, message_config.content_type)
        message["Subject"] = message_config.subject
        message["From"] = self.config.smtp_username
        message["To"] = message_config.to

        async with SMTP(
            hostname=self.config.smtp_server, port=self.config.smtp_port, use_tls=False
        ) as smtp:
            await smtp.login(self.config.smtp_username, self.config.smtp_password)
            await smtp.send_message(message)


def get_mailer() -> Mailer:
    return SMTPMailer(
        SMTPMailerConfig(
            smtp_server=settings.smtp_server,
            smtp_port=settings.smtp_port,
            smtp_username=settings.smtp_username,
            smtp_password=settings.smtp_password,
        )
    )


MailerDep = Annotated[Mailer, Depends(get_mailer)]

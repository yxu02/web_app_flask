from requests import post
import os

FAILED_LOADING_MAILGUN = "Mailgun service configuration failed"
MAILGUN_RESPONSE_FAILED = "Mailgun failed to respond"

class MailgunException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Mailgun:
    DOMAIN_NAME = os.environ.get("DOMAIN_NAME")
    API_KEY = os.environ.get("API_KEY")
    FROM_TITLE = os.environ.get("MAILGUN_TITLE_FROM")
    FROM_EMAIL = os.environ.get("MAILGUN_EMAIL_FROM")


    @classmethod
    def send_email(cls, email, subject, text, html):
        if cls.DOMAIN_NAME is None or cls.API_KEY is None:
            raise MailgunException(FAILED_LOADING_MAILGUN)

        response = post(
            f"https://api.mailgun.net/v3/{cls.DOMAIN_NAME}/messages",
            auth=("api", cls.API_KEY),
            data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html
                  }
        )
        if response.status_code != 200:
            raise MailgunException(MAILGUN_RESPONSE_FAILED)

        return response


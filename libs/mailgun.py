import os
from typing import List
from requests import Response, post


class MailgunException(Exception):
    def __init__(self, message):
        self.message = message


class Mailgun:
    FROM_TITLE = "Pricing Service"
    FROM_EMAIL = "do-not-reply@sandboxde9545dd4e6d41baa8de60197b407192.mailgun.org"


    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)
        if api_key is None:
            raise MailgunException("Failed to load mailgun api key !")
        if domain is None:
            raise MailgunException("Failed to load mailgun domain !")
        response = post(
            f"{domain}/messages",
            auth=("api", api_key),
            data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html})
        if response.status_code != 200:
            raise MailgunException("An error occured while sending a mail")
        return response





# def send_simple_message():
#     return post(
#         "https://api.mailgun.net/v3/sandboxde9545dd4e6d41baa8de60197b407192.mailgun.org/messages",
#         auth=("api", "b4ee11eeb6ed0ffb7f1d6287b80f97c4-fd0269a6-d7f17bde"),
#         data={"from": "Pricing Service <do-not-reply@sandboxde9545dd4e6d41baa8de60197b407192.mailgun.org>",
#               "to": ["amalmajeed7@gmail.com"],
#               "subject": "Hello",
#               "text": "Testing some Mailgun awesomness!"})
# print(send_simple_message())
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate
from jose import jwt
from core.config import settings

import boto3
from botocore.exceptions import ClientError
import os


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def send_ses(email_to: str,username: str,password: str,email_token: str)-> None:
    SENDER = settings.EMAILS_FROM_EMAIL
    RECIPIENT = email_to
    AWS_REGION = settings.AWS_REGION
    SUBJECT = "Your account for DESS.WORK has been created"
    project_name = settings.PROJECT_NAME
    link = settings.SERVER_HOST

    BODY_TEXT = (f""" Dear user,\r\n

                We have received a request to authorize this email address for use with DESS.WORK. 
                If you requested this verification, please go to the following URL URL: {email_token}  to confirm that you are authorized to use this email address.

                User: {username}
                Password: {password}
                """
                )
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h3>Your account for DESS.WORK has been created</h3>
    Dear user,\r\n

                We have received a request to authorize this email address for use with DESS.WORK. 
                If you requested this verification, please go to the following URL: {email_token} to confirm that you are authorized to use this email address.

                User: {username}
                Password: {password}
    </body>
    </html>
                """            
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION,  
       aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
       aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"])

    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        logging.info(f"Email Send. MessageId: {response['MessageId']}")

def send_email_ses(email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
    ) -> None:

    SENDER = settings.EMAILS_FROM_EMAIL
    RECIPIENT = email_to
    AWS_REGION = settings.AWS_REGION
    SUBJECT = subject_template
    project_name = settings.PROJECT_NAME
    link = settings.SERVER_HOST
    BODY_HTML = environment['BODY_HTML']
    

    # The email body for recipients with non-HTML email clients.
        
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION,  
       aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
       aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"])

    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        logging.info(f"Email Send. MessageId: {response['MessageId']}")




def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    print("entro al mail")
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    "mail enviado"
    logging.info(f"send email result: {response}")

def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email_ses(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
            "BODY_HTML": f"""<html>
                            <head></head>
                            <body>
                            <h3>Password Recovery</h3>
                            Dear user,\r\n

                                        We have received a request to recover your password for your account {email} in with DESS.WORK. 
                                        If you requested this verification, please go to the following URL: {token} to recover your password.
                            </body>
                            </html>
                        """
        },
    )



def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt




def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(   token, settings.SECRET_KEY, algorithms=["HS256"],options={"verify_signature": False})
        return decoded_token['sub']
    except jwt.JWTError as e:
        print(e)
        return None

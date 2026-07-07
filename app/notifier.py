# This is a lightweight implementation of a notifier that sends automated emails with the newly found tech events

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_tech_event_email(subject, html_content):
    # Load credentials strictly from environment
    sender = os.environ.get("SENDER_EMAIL")
    receiver = os.environ.get("RECEIVER_EMAIL")
    pwd = os.environ.get("EMAIL_APP_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        # Secure TLS connection
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, pwd)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

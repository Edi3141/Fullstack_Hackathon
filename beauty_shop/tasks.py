from django.core.mail import send_mail
from .celery import app
from account.send_email import send_confirmation_email, send_notification


@app.task
def send_confirm_email_task(user, code):
    send_confirmation_email(user, code)


@app.task
def send_notification_task(user_email, order_id, price):
    send_notification(user_email, order_id, price)



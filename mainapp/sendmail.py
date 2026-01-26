from django.core.mail import EmailMessage, get_connection
from django.conf import settings

def sendemail(name, email, event,claimurl, passcode):
    subject = "Your Rekord Event Details"

    body = f"""
Hello {name},

Your event has been created successfully!

Event: {event.eventname}
Claim URL: {claimurl}
Secret Code: {passcode}

Do not share this code.

– Rekord Team
"""

    # 🔥 REUSE SMTP CONNECTION
    with get_connection() as connection:
        msg = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
            connection=connection
        )
        msg.send()


if __name__ == "__main__":
    sendemail("asasdd","sreeramvg100@gmail.com","asdads","asdasdd")
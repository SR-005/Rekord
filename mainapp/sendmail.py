from django.core.mail import EmailMessage, get_connection
from django.conf import settings

def sendemail(name, email, event,claimurl, passcode):
    subject = f"You have a Rekord to Claim - from {event.organizationid}"

    body = f"""
Hello {name},

You have become eligible to claim an NFT of {event.eventname} from {event.organizationid}. The NFT details are given below, DO NOT under any circumstamces share your PASSCODE with anyone.
It is vital to entire the Passcode at the time of claiming to ensure safety.

EVENT NAME: {event.eventname}
EVENT ID: {event.eventid}
EVENT CREATOR: {event.organizationid}
DATE OF HOSTING: {event.eventdate}
CITY: {event.city}

To Claim this NFT, visit the link provided and enter the PASSCODE to verify yourself.
URL : {claimurl}
PASSCODE: {passcode}
Do not share this code with anyone.

– With best regards,
  Rekord Team
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
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

def sendemail(name, email, event,claimurl, passcode):
    subject = f"You have a Rekord to Claim - from {event.organizationid}"

    body = f"""
        Hello {name},

        You have become eligible to claim an NFT of the event '{event.eventname}' organized by {event.organizationid}. The NFT details are given below, DO NOT under any circumstamces share your PASSCODE with anyone.
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

def sendreciept(tokenobject,blockexplorer):
    subject = f"{tokenobject.eventid} NFT Claim Completed!"

    body = f"""
        Hello {tokenobject.name},

        Your recent claim of NFT of {tokenobject.eventid} event was success. The details of the transaction will be reflected in the given URL.
        Transaction Details: {blockexplorer}

        To Import your claimed NFT you'll need to follow certain steps:

        STEP 1: Open your Wallet and Add AMOY Network using the provided details.
                Network Name: Polygon Amoy Testnet
                RPC URL: https://rpc-amoy.polygon.technology/
                Chain ID: 80002
                Currency Symbol: POL
                Block Explorer: https://amoy.polygonscan.com/

        STEP 2: View the Transaction in Block Explorer. To do that Visit the link given above, then.
                 -copy the Address from 'Interacted With (To)' section 
                 -note the Token ID from 'ERC-721 Tokens Transferred' section 

        STEP 3: In your Wallet, open the NFT section and Click on IMPORT NFT. 
                -Switch the network to AMOY
                -Paste the Address you copied
                -Enter the TokenID
            
        Voila, Your NFT will be loaded after a few minutes


        – With best regards,
        Rekord Team
        """

    # 🔥 REUSE SMTP CONNECTION
    with get_connection() as connection:
        msg = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[tokenobject.email],
            connection=connection
        )
        msg.send()



if __name__ == "__main__":
    sendemail("asasdd","sreeramvg100@gmail.com","asdads","asdasdd")
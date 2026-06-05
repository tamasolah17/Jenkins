# email_service.py

import boto3

ses = boto3.client(
    "ses",
    region_name="us-east-1"
)

def send_welcome_email(email):

    response = ses.send_email(
        Source="nnavocs@gmail.com",

        Destination={
            "ToAddresses": [email]
        },

        Message={
            "Subject": {
                "Data": "Welcome to Premium Access"
            },

            "Body": {
                "Text": {
                    "Data":
                    """
                    Thank you for your payment.

                    Your account has been activated.

                    Please complete your 2FA setup.
                    """
                }
            }
        }
    )

    return response
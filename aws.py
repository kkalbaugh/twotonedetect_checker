import boto3
from botocore.exceptions import ClientError
import logging
import config

logger = logging.getLogger('zmchecker.smtp')

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = config.email_from

# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENT = config.email_to

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the
# ConfigurationSetName=CONFIGURATION_SET argument below.
#CONFIGURATION_SET = "ConfigSet"

AWS_ACCESS_KEY = config.aws_access_key
AWS_SECRET_KEY = config.aws_secret_key

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = config.aws_region

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
try:
    client = boto3.client('ses',region_name=AWS_REGION,aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)
except Exception as e:
    logger.error("Database Exception occurred", exc_info=True)

# Try to send the email.
def sendemail(text,subject):
    SUBJECT = subject         # The subject line for the email.

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("%s"
                ) % text

    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
      %s
    </body>
    </html>
                """ % text
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
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
        logger.error(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        logger.debug(response['MessageId'])

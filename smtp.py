import smtplib
import config
import logging

# Import the email modules we'll need
from email.mime.text import MIMEText

logger = logging.getLogger('zmchecker.smtp')

def sendemail(text,subject):
  msg = MIMEText(text)
  msg['From'] = config.email_from
  msg['To'] = config.email_to
  msg['Subject'] = subject

  try:
    if config.smtp_password == 587:
        server = smtplib.SMTP(config.smtp_server, config.smtp_port)
        server.starttls()
    else:
        server = smtplib.SMTP(config.smtp_server)

    if config.smtp_password != "":
        server.login(config.email_login, config.smtp_password)

    server.send_message(msg)
    server.quit()
    print("Email Sent! %s" % text)
    logger.info("Sent email %s" % text)

  except:
    logger.error("Couldn't send email %s" % msg)

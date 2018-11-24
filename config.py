#TTD Status File
statusfile = '/home/XXX/ftp/files/CommonStatusFile.txt' 

# Email Config
email_resend = 24 # Number of hours before resending email about problem
email_from=""  # "ZoneMinder <email@domain.com>"
email_to=""   # someone@email.com

# Email Type SMTP or Use AWS
email_type="smtp"  # stmp or aws

# SMTP Settings
smtp_server=""
smtp_port=587
smtp_login="" # SMTP Username
smtp_password="" # SMTP Password

# AWS Region
aws_region = "us-east-1"
aws_access_key = ""
aws_secret_key = ""

# Logging
logging_level = 'ERROR'
logFile = '/var/log/ttd_checker.log'
lastsentfile = '/var/local/ttd_checker/lastsent.txt.'

import csv
import smtplib
from datetime import timedelta, datetime, timezone
import time
import os.path
import logging
from logging.handlers import RotatingFileHandler
import config

# Check what email system to use
if config.email_type == "aws":
    import aws as email
if config.email_type == "smtp":
    import smtp as email

try:
    logLevel = config.logLevel
except:
    logLevel = 'DEBUG'

# Create Logging Object
logger = logging.getLogger('ttdchecker')
log_level = logging.getLevelName(logLevel)
logger.setLevel(log_level)

# Setup Logging Handlers & Level
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
ttd_handler = RotatingFileHandler(config.logFile, mode='a', maxBytes=5*1024*1024,backupCount=2, encoding=None, delay=0)
ttd_handler.setFormatter(log_formatter)

logger.addHandler(ttd_handler)


now = datetime.now().timestamp()
hourago = int(now)- 60 * 60
#hourago = int(now)
eighthoursago = int(now) - 60 * 60 * 8

times = []

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def sendagain():
    if not os.path.isfile(config.lastsentfile):
        print("Need to create file")
        logger.info("%s doesn't exist.  Need to create file" % config.lastsendfile)
        return 1
    else:
        try:
            with open(config.lastsentfile) as fp:  
                line = fp.readline()
                lastemail = int(line)
                fp.close()
                if lastemail > eighthoursago:
                    print("Already sent less than 8 hours ago")
                    lastsend_obj = datetime.fromtimestamp(int(line))
                    lastsend_str = lastsend_obj.strftime("%Y-%m-%d %I:%M:%S %p")
                    return lastemail
                elif lastemail == 0:
                    print("TTD Wasn't In Alarm")
                    return 1
                else:
                    print("Ready to send again")
                    return 1
        except:
            logger.error("Unable to open %s" % config.lastsentfile)
            
def openStatusFile():
     with open(config.statusfile) as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
            times.append(float(line[1]));
    
if __name__ == "__main__":
    logger.info("Started Program")
   
    try:
        openStatusFile()
    except:
        logger.error("Couldn't Open Status File")
    print("Times listed in file: %s" % times)
    lastrecv = max(times)
    #print(type(lastrecv))
    lastrecv_obj = datetime.fromtimestamp(lastrecv)
    lastrecv_str = lastrecv_obj.strftime("%Y-%m-%d %I:%M:%S %p")
    print("Last Send: %s " % lastrecv_str)
    
    if any(x > hourago for x in times):        
        print("Status is OK")
        ready = sendagain();
        if ready > 2:
            text = "TwoToneDetect is Working Again!"            
            print(text)
            aws.sendawsemail(text,config.email_subject)
            ts = open(config.lastsentfile, 'w')
            ts.write("0")
            ts.close()       
        else:
            print("Not ready to send")

    else:
        print("Status is NOT Ok")
        ready = sendagain();
        print(ready)
        if ready == 1:
            text = "TTD last received update at "
            text += lastrecv_str            
            print(text)
            aws.sendawsemail(text,config.email_subject+" Error")
            ts = open(config.lastsentfile, 'w')
            ts.write(str(int(now)))
            ts.close()       
        else:
            print("Not ready to send.  Sent Already")
    exit()

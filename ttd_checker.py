import csv
import smtplib
from datetime import timedelta, datetime, timezone
import time
import os.path
import ttd_aws
import logging
from logging.handlers import RotatingFileHandler

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

logFile = 'ftp/files/ttd.log'

ttd_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
ttd_handler.setFormatter(log_formatter)
ttd_handler.setLevel(logging.INFO)

app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)

app_log.addHandler(ttd_handler)

statusfile = 'ftp/files/CommonStatusFile.txt' 
lastsentfile = 'ftp/files/lastsent.txt'

subject = ''
text = ''


now = datetime.now().timestamp()
hourago = int(now)- 60 * 60
#hourago = int(now)
eighthoursago = int(now) - 60 * 60 * 8

times = []

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def sendagain():
    if not os.path.isfile(lastsentfile):
        print("Need to create file")
        app_log.info("%s doesn't exist.  Need to create file" % lastsendfile)
        return 1
    else:
        try:
            with open(lastsentfile) as fp:  
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
            app_log.error("Unable to open %s" % lastsentfile)
            
def openStatusFile():
     with open(statusfile) as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
            times.append(float(line[1]));
    
if __name__ == "__main__":
    app_log.info("Started Program")
    subject = "BDFD TwoToneDetect "
    try:
        openStatusFile()
    except:
        app_log.error("Couldn't Open Status File")
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
            subject = "TwoToneDectect Back Online"
            print(text)
            aws.sendawsemail(text,subject)
            ts = open(lastsentfile, 'w')
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
            subject = "TTD Not Working!"
            print(text)
            aws.sendawsemail(text,subject)
            ts = open(lastsentfile, 'w')
            ts.write(str(int(now)))
            ts.close()       
        else:
            print("Not ready to send.  Sent Already")
    exit()

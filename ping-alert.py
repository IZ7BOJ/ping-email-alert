#!/usr/bin/env python

import sys
import os
import time
import numpy as np
import smtplib
from email.mime.text import MIMEText

hostname = ["192.168.1.1","192.168.1.2"] #put hosts to be pinged separated by comma
state_array = np.ones(len(hostname),dtype=int) #count the hosts to be monitored and create the state array (all 1)
wait=1800 #seconds between checks

s = smtplib.SMTP('smtp.gmail.com:587') #put smtp server. gmail is just an example
s.set_debuglevel(0)
sender = 'xxxx@gmail.com' #put user email
recipients = ['yyyyy@email.it'] #put recipient address
password = 'zzzz' #put email password

try:
        while True:
            i=0
            while i < len(hostname):
                response = os.system("ping -c 3 " + hostname[i] + " >/dev/null")
                # Alive->Dead
                if state_array[i]==1:
                        if response !=0:
                                  try:
                                        msg_down = MIMEText(hostname[i]+" is down!")
                                        msg_down['Subject'] = "Network Monitor notification"
                                        msg_down['From'] = sender
                                        msg_down['To'] = ", ".join(recipients)
                                        s.ehlo()
                                        s.starttls()
                                        s.login(sender,password)
                                        s.sendmail(sender, recipients, msg_down.as_string())
                                        s.quit()
                                        #print "Successfully sent email"
                                  except Exception:
                                        print "Error: unable to send email"
#                                 print hostname[i], 'is down!'
                                  state_array[i]=0
                #Dead->Alive
                else:
                         if response == 0:
                                  try:
                                        msg_up = MIMEText(hostname[i]+" is up!")
                                        msg_up['Subject'] = "Network Monitor notification"
                                        msg_up['From'] = sender
                                        msg_up['To'] = ", ".join(recipients)
                                        s.ehlo()
                                        s.starttls()
                                        s.login(sender,password)
                                        s.sendmail(sender, recipients, msg_up.as_string())
                                        s.quit()
                                        #print "Successfully sent email"
                                  except Exception:
                                        print "Error: unable to send email"
#                                 print hostname[i], 'is up!'
                                  state_array[i]=1
                i=i+1
            time.sleep(wait)
except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    print("keyboard exception occurred")
    sys.exit()

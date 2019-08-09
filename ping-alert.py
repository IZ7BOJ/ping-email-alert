#!/usr/bin/env python

#Email notifications are sent every time a network host changes state (Responsive to Unresponsive and Unresponsive to Responsive)
#Assign execution permission to the file and execute it as root in background.
#A log file can be used to trace state change.
#Before using the script, parameters in config section must be declared.
#This script may have a lot of bugs, problems and it's written in very non-efficient way without a lot of good programming rules. But it works for me.
#Author: Alfredo IZ7BOJ iz7boj[--at--]gmail.com
#You can modify this program, but please give a credit to original author. Program is free for non-commercial use only.
#(C) Alfredo IZ7BOJ 2019

#Version 0.1beta
#*******************************************************************************************/

import sys
import os
import time
import numpy as np
import smtplib
from email.mime.text import MIMEText
import logging

##############################################################################################
# CONFIGURATION SECTION
# DECLARE EVERY PARAMETER BEFORE USING THIS SCRIPT

hostname = ["10.93.9.1","10.93.2.254","10.93.2.253","10.93.3.51","10.93.8.1","10.93.8.2"] #hostnames or IP numbers of hosts to be monitored. Keep commas and quotation marks for every host
wait=1800 #seconds between check
logfile = '/var/log/ping-alert.log' #file to be written for the log (with the path)
debug=1 #1=log enable , 0=log disabled

s = smtplib.SMTP('smtp.gmail.com:587') #put smtp server. gmail is just an example
s.set_debuglevel(0) #Set the debug output level. 1 for debug messages for connection and for all messages sent to and received. 2 for add timestamps.
sender = 'xxxx@gmail.com' #put user email
recipients = ['yyyyyy@yahoo.it'] #put recipient address separated by commas
password = 'zzzzzz' #password for server autentication

# END OF CONFIGURATION SECTION
############################################################################################

#start from "all hosts active"

state_array = np.ones(len(hostname),dtype=int) #count the hosts to be monitored and create the state array (all 1)
logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s %(message)s') #initialize the log

if debug:
        logging.debug("daemon started")

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
                                        if debug:
                                                logging.debug(hostname[i]+" is down!")
                                  except Exception:
                                        if debug:
                                                logging.debug("Error: unable to send email")
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
                                        if debug:
                                                logging.debug(hostname[i]+" is up!")
                                  except Exception:
                                        if debug:
                                                logging.debug("Error: unable to send email")
                                  state_array[i]=1
                i=i+1
            time.sleep(wait)
except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    if debug:
       logging.debug("keyboard exception occurred")
    print("keyboard exception occurred")
    sys.exit()

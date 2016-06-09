#!/usr/bin/python
# script to check remote hosts for disk usage and report
# Stolen from http://www.infomagnet.com/checking-mirror-disk-usage-and-file-timestamp-ssh-using-python
#
import time
import sys
import smtplib
from subprocess import *
# Import email modules
from email.mime.text import MIMEText

# Had to add the .strip() at the end of this to remove a new line.
user = Popen(["whoami"], stdout=PIPE, universal_newlines=False).communicate()[0].strip()
domain = "sitesuite.net"
hostname = "vm-puppet"
myCommand = "df /"
check_timestamp = 2*24*60*60
check_percentage = 10

#print user
#print domain
#print hostname
#print myCommand
#print __name__

if __name__ == "__main__":
    host = "smtp.sitesuite.com.au"
    s = smtplib.SMTP(host, 225)
    df_output = Popen(["ssh", user +"@" + hostname, myCommand], stdout=PIPE).communicate()[0].split()
    #print df_output
    percentage = int(df_output.split("\n")[1].split()[4].strip("%"))
    if percentage > check_percentage:
        msg = MIMEText(df_output)
        msg['Subject'] = "[IMPORTANT] Disk usage over %d%%" % (percentage)
        msg['From'] = 'support@sitesuite.com.au'
        for mail in sys.argv[1].split(','):
            msg['To'] = mail
            s.sendmail('benc@sitesuite.com.au', mail, msg.as_string())

        print "Host " + hostname + " has "+ str(percentage) + "% used disk"
        print "And needs your urgent attention"
        print

    print "Host " + hostname + " has " + str(percentage) + "% used disk"
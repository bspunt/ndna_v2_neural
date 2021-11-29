#!/usr/bin/env python

## 
## ------------------------------------------------------------------
##     NDNA: The Network Discovery N Automation Program
##     Copyright (C) 2017  Brett M Spunt, CCIE No. 12745 (US Copyright No. Txu002053026)
## 
##     This file is part of NDNA.
##
##     NDNA is free software: you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation, either version 3 of the License, or
##     (at your option) any later version.
## 
##     NDNA is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.
##
##     This program comes with ABSOLUTELY NO WARRANTY.
##     This is free software, and you are welcome to redistribute it
##
##     You should have received a copy of the GNU General Public License
##     along with NDNA.  If not, see <https://www.gnu.org/licenses/>.
## ------------------------------------------------------------------
## 


import os.path
import subprocess
import time
import sys
import re
import os
import threading
import datetime
import base64

print "        " 
print "             WELCOME TO THE "  
print "------------------------------------------"                           
print "(`|\ ||\/||)| | | /|| |/__|) /||\__||)S _"
print "_)| \||  ||  \|\|/-||_|\  |)/-||/  || _"
print "------------------------------------------" 
print "               PROGRAM   "    
print "        " 

#############################################

# Start to write standard errors to log file
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("/usr/DCDP/logs/SNMPWALK-Bad-IPs-sysname-sysdescr.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    


sys.stdout = Logger()
#sys.stdout = open('/usr/DCDP/logs/dcdp.log', 'w')
# for future use
# Current_time = time.ctime()

sys.stderr = open("/usr/DCDP/logs/SNMPWALK-Bad-IPs-sysname-sysdescr-ERR.log", 'w')
print ""
print "------------------------------------------------------------------"
print "    NDNA: The Network Discovery N Automation Program"
print "    Copyright (C) 2017  Brett M Spunt, CCIE No. 12745 (US Copyright No. Txu002053026)"
print ""
print "    NDNA is free software: you can redistribute it and/or modify"
print "    it under the terms of the GNU General Public License as published by"
print "    the Free Software Foundation, either version 3 of the License, or"
print "    (at your option) any later version."
print ""
print "    NDNA is distributed in the hope that it will be useful,"
print "    but WITHOUT ANY WARRANTY; without even the implied warranty of"
print "    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
print "    GNU General Public License for more details."
print ""
print "    This program comes with ABSOLUTELY NO WARRANTY."
print "    This is free software, and you are welcome to redistribute it"
print ""
print "    You should have received a copy of the GNU General Public License"
print "    along with NDNA.  If not, see <https://www.gnu.org/licenses/>."
print "------------------------------------------------------------------"
print ""
print "###############################################################################################" 
print "------------------------------------------"                           
print "(`|\ ||\/||)| | | /|| |/__|) /||\__||)S _"
print "_)| \||  ||  \|\|/-||_|\  |)/-||/  || _"
print "------------------------------------------" 
print "        PROGRAM IS STARTING......" 
print "        " 
print "###############################################################################################" 
print "                        Enter The DataCenter Information Below:" 
print ""  
print "           This DataCenter Must Exist From Previously Running The NDNA Program" 
print ""  
print "   This Will Write the snmpwalk output to /usr/DataCenters/<your DC directory>/DCDP/snmpwalk"
print ""  
print "           The Name Must Match The Name Of The Directory That Already Exists!"
print "" 
print "###############################################################################################" 
print ""
print "" 

DataCenter = raw_input( "Enter Data_Center String Here e.g. ACM:New-York-DC: " )

SNMP_COM = raw_input( "Enter SNMP Community String: " )

print "        " 

if os.path.exists('/usr/DataCenters/%s' % DataCenter) == True:                     
    print "DataCenter Exists..."
else:
    print "DataCenter does not exist...Program exiting. Goodbye..."
    sys.exit()

iplist = open('/usr/DataCenters/%s/DCDP/bad-IPs/Bad-IPs.txt' % DataCenter).readlines()
## remove /n from list elements
iplist = map(lambda s: s.strip(), iplist)

########################################################
def snmpwalk_bad_IPs(ip):
    build_snmp_var = "snmpwalk -Os -c {0} -v 2c {1} iso.3.6.1.2.1.1.1"
    build_snmp_var.format(SNMP_COM, ip)
    ## to get sysdecr
    SNMPWALK_VAR = subprocess.Popen('%s' % build_snmp_var.format(SNMP_COM, ip), shell=True, stdout=subprocess.PIPE)

    # GRAB STDOUT - Return to write to files
    output = SNMPWALK_VAR.stdout.read()
    #print output
    return output

def write_files(ip):
    file_name = '/usr/DataCenters/%s/DCDP/snmpwalk/' % DataCenter + ip + '_snmpwalk.txt'
    fo = open(file_name, "w")
    #Calling the snmpwalk function
    fo.write(snmpwalk_bad_IPs(ip))
    fo.close()
    
#Creating threads function
def create_threads():
    threads = []
    for ip in iplist: 
        th = threading.Thread(target = write_files, args = (ip,))   #args is a tuple with a single element     
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function which then calls the open ssh function
create_threads()


def snmpwalk_bad_IPs2(ip):
    build_snmp_var = "snmpwalk -Os -c {0} -v 2c {1} iso.3.6.1.2.1.1.5"
    build_snmp_var.format(SNMP_COM, ip)
    ## to get sysname
    SNMPWALK_VAR = subprocess.Popen('%s' % build_snmp_var.format(SNMP_COM, ip), shell=True, stdout=subprocess.PIPE)

    # GRAB STDOUT - Return to write to files
    output = SNMPWALK_VAR.stdout.read()
    #print output
    return output

def write_files2(ip):
    file_name = '/usr/DataCenters/%s/DCDP/snmpwalk/' % DataCenter + ip + '_snmpwalk.txt'
    fo = open(file_name, "a")
    #Calling the snmpwalk function
    fo.write(snmpwalk_bad_IPs2(ip))
    fo.close()
    
#Creating threads function
def create_threads2():
    threads = []
    for ip in iplist: 
        th = threading.Thread(target = write_files2, args = (ip,))   #args is a tuple with a single element     
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function which then calls the open ssh function
print "\n* Output files will be written to /usr/DataCenters/%s/DCDP/snmpwalk for all device(s)...\n" % DataCenter

create_threads2()
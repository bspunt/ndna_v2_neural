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


""" 
Purpose: To automate Cisco Data Center Discovery and Network Discovery. 

Uses a seed device and automatically discovers the network using CDP.

Application also enables programming the network, with the ability to 
use Python to perform customized discovery and/or program the network

Version 17.02

"""



import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
import paramiko
import os.path
import subprocess
import time
import sys
import re
import os
import threading
import datetime
import getpass
import base64

print "  _   _   _   _   _   _   _   _   _     _   _   _   _   _   _   _    "
print "  _   _   _   _   _   _   _   _   _     _   _   _   _   _   _   _    "
print "                                                                     "
print "     Welcome to the The Network Discovery N Automation Program       "
print "                          (NDNA) v17.02                              "
print "    _   _   _   _   _   _   _     _   _   _   _   _   _   _   _   _  "
print "   / \ / \ / \ / \ / \ / \ / \   / \ / \ / \ / \ / \ / \ / \ / \ / \ "
print "  ( N | e | t | w | o | r | k ) ( D | i | s | c | o | v | e | r | y )"
print "   \_/ \_/ \_/ \_/ \_/ \_/ \_/   \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ "
print "                                                                     "
print "            US Copyright: Automate-The-Network 2017                 "
print "              http://www.automate-the-network.com                    "  
print "  _   _   _   _   _   _   _   _   _     _   _   _   _   _   _   _    "
print " / \ / \ / \ / \ / \ / \ / \ / \ / \ / \   / \ / \ / \ / \ / \ / \ / \ " 
print "( A | u | t | o | m | a | t | i | o | n ) ( P | r | o | g | r | a | m )"
print " \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/   \_/ \_/ \_/ \_/ \_/ \_/ \_/ "
print "                                                                       "
print "            Hit Ctrl Z or Ctrl C to exit the program                "
print "  _   _   _   _   _   _   _   _   _     _   _   _   _   _   _   _   "
print "  _   _   _   _   _   _   _   _   _     _   _   _   _   _   _   _   "
print "                                                                    "
print "                                                                    "
print "                                                                    "
print "                                                                    "
print "                                                                    "
print "                                                                    "
print "                                                                    "
print "                                                                    "
print "                                                                    "
print "                                                                    "
print "                                                                    "
print "                                                                    "
print "                                                                    "
pause = raw_input( "                   Hit Enter To Continue" )
print "                                                                    "

# Build Program Directories
def mk_dir():
    if os.path.exists('/usr/DCDP/tmp'):
        print "*** DCDP sub-directories exist...Bypassing directory creation"
        print "*** "
        print "***"
        print "***"
        print "*** All log files will be written to /usr/DCDP/logs/"
        print "***"
        print "***"
        subprocess.Popen("mkdir /usr/DCDP/configs/sh-ip-inter-brief-sh-ver", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("rm -r /usr/DCDP/snmpwalk", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/snmpwalk", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("rm -r /usr/DCDP/logs", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/logs", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("touch /usr/DCDP/logs/dcdp.log", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
    else:
        print "*** Creating program sub-directories....."
        print "***"
        print "***"
        print "*** All log files will be written to /usr/DCDP/logs/"
        print "***"
        print "***"
        subprocess.Popen("mkdir /usr/DCDP/tmp", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/cdp_files", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/good-IPs", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/bad-IPs", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/configs", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/configs/sh-ip-inter-brief-sh-ver", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/Full-IP-List", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/hostname-to-IPs", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/configs/NXOS", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/configs/IOS", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/stats/", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        subprocess.Popen("mkdir /usr/DCDP/stats/tmp", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
mk_dir()

# Start to write standard errors to log file
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("/usr/DCDP/logs/dcdp.log", "w")

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
sys.stderr = open('/etc/scalpel/bin/manuals/legacy/post/pre/game/php/dcdp-error.log', 'w')
# for future use
# Current_time = time.ctime()
print "#### You will be asked to enter your username and password numerous times during the discovery process"
print ""
print "#### This process usually takes about 12 to 15 minutes to complete all discovery scripts. Please Do Not Stop Monitoring the discovery"
print "#### Or you will miss when it prompts you multiple times for your username and password!! Keep your password copied to your clipboard"
print ""
print "####         Do this via an encrypted database like KeepPass or an unsaved text file, e.g. not written to disk"
print "______________________________________________" 
print "   "
username = raw_input( "Enter username: " )
print "   "
print "   "
print "______________________________________________" 
print "   "
print "   "
print "______________________________________________" 
print "   "
print "####    ////////// Password will be hidden ///////////"
print "#### Please copy and input your password from an unsaved text file, e.g. not written to disk, a or secure database like KeepPass"
print "   "
password = getpass.getpass()
print "   "
print "______________________________________________" 
print "   "
print "   "

WRITE_USERNAME = open("/usr/DCDP/tmp/username.txt", "w")
time.sleep(1)
WRITE_USERNAME.write(username)
time.sleep(1)
WRITE_USERNAME.close()

WRITE_PASSWORD = open("/usr/DCDP/tmp/password.txt", "w")
time.sleep(1)
WRITE_PASSWORD.write(password)
time.sleep(1)
WRITE_PASSWORD.close()

Seed_IP = raw_input( "Enter Seed IP: " )
print "   "
print "______________________________________________" 
print "   "
print "*** Program is running....."
print "   "
print "*** Be patient and wait for the program to complete"
print "   "
print "*** This might take a long time, depending on the size of the network....."
print "   "
print "*** This usually takes about 10 to 15 minutes....."
print "   "
print "*** Starting on Seed Device....."
print "   "
print "*** Progress feedback will be provided at each level....."
print "______________________________________________" 
print "   "
Seedfilename = '/usr/DCDP/cdp_files/seed_ip_address.txt'
seedfileopen = open(Seedfilename, "w")
seedfileopen.write(Seed_IP)
seedfileopen.close()

#setup max number of threads for Semaphore method to use. create sema variable for open ssh function to use
maxthreads = 10
sema = threading.BoundedSemaphore(value=maxthreads)


#Open SSHv2 connection to seed device
def seed_network_connection(ip):
    try:
        paramiko.util.log_to_file("/usr/DCDP/logs/paramiko.log")        
        #Logging into device
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Passing the necessary parameters
        session.connect(ip, username = username, password = password, look_for_keys=False)
        
    #Start an interactive shell session on the router
        connection = session.invoke_shell() 
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        print "   "
        print ".... "
        time.sleep(8)
        connection.send("sh cdp nei detail | i IP\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief vrf all\n")
        time.sleep(8)
        connection.send("sh version\n")
        print ".... Seed Device Almost Complete...."
        time.sleep(8)

#############################################################
        # Get around the 64K bytes (65536). paramiko limitation
        interval = 0.1
        maxseconds = 15
        maxcount = maxseconds / interval
        bufsize = 65535

        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        router_output = ''

        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode('ascii')
                router_output += data

            if connection.exit_status_ready():
                break

            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())

            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break

            rbuffer = router_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            router_output += data.decode('ascii')
#############################################################
        
        if re.search(r"% Invalid input detected at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"% Invalid command at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"Incorrect usage", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"Cisco Controller", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"User:", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"% Authorization failed", router_output):
            print "   "
            print "** Authorization failed for %s Looks Like a TACACS issue." % ip
            
        else:
            print "   "
            print "** Completed device %s" % ip
        
        return router_output
    
    #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        print "   "
        print "* Authentication Error for %s" % ip
        print "   "
        print "* Closing program...\n"
    except paramiko.SSHException:
        print "   "
        print "* Incompatible SSH version. Paramiko requires compatible SSH and kex on device %s" % ip
    #An except clause may name multiple exceptions as a parenthesized tuple, for example
    #except (IDontLikeYouException, YouAreBeingMeanException) as e:
        #pass

iplist = open('/usr/DCDP/cdp_files/seed_ip_address.txt').readlines()
# remove /n from list to preserve file names
iplist = map(lambda s: s.strip(), iplist)

def write_files1(ip):
    sema.acquire()
    file_name = '/usr/DCDP/tmp/' + ip + '_seed.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    fo.write(seed_network_connection(ip))
    fo.close()
    time.sleep(2)
    sema.release()
    
#Creating threads function
def create_threads1():
    threads = []
    for ip in iplist: 
        th = threading.Thread(target = write_files1, args = (ip,))   #args is a tuple with a single element     
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function which then calls the open ssh function
create_threads1()

########################################################
# Build 2nd level IP files from seed device/s. Run egrep to grep NX-OS and IOS output, e.g. match multiple patterns
subprocess.Popen("cat /usr/DCDP/tmp/*seed.txt | egrep 'IP address|IPv4' | sed -e 's/IP address://' | sed -e 's/IPv4 Address://' | grep -v 0.0.0.0 > /usr/DCDP/tmp/2nd_level_IPs.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# Remove empty spaces in file
subprocess.Popen("tr -d ' ' < /usr/DCDP/tmp/2nd_level_IPs.txt > /usr/DCDP/tmp/cdp_second_level-pre.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# grab IPs to exclude from next level IPs.txt
subprocess.Popen("cat /usr/DCDP/tmp/*seed.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' > /usr/DCDP/tmp/first_level_IPs_SIIB.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

########################################################

#Open SSHv2 connection to 2nd level devices
def second_level_network_connection(ip):
    try:
        paramiko.util.log_to_file("/usr/DCDP/logs/paramiko.log")
        #Logging into device
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Passing the necessary parameters
        session.connect(ip, username = username, password = password, look_for_keys=False)
        
    #Start an interactive shell session on the router
        connection = session.invoke_shell() 
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        print ".... "
        time.sleep(8)
        connection.send("sh cdp nei detail | i IP\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief vrf all\n")
        time.sleep(8)
        connection.send("sh version\n")
        time.sleep(8)

#############################################################
        # Get around the 64K bytes (65536). paramiko limitation
        interval = 0.1
        maxseconds = 15
        maxcount = maxseconds / interval
        bufsize = 65535

        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        router_output = ''

        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode('ascii')
                router_output += data

            if connection.exit_status_ready():
                break

            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())

            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break

            rbuffer = router_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            router_output += data.decode('ascii')
#############################################################

        if re.search(r"% Invalid input detected at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"% Invalid command at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"Incorrect usage", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"Cisco Controller", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"User:", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"% Authorization failed", router_output):
            print "   "
            print "** Authorization failed for %s Looks Like a TACACS issue." % ip
            
        else:
            print "   "
            print "** Completed device %s" % ip

        return router_output
    
    #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        pass
        print "   "
        print "* Authentication Error for %s" % ip
        print "   "
        #print "* Closing program...\n"
    except paramiko.SSHException:
        print "   "
        pass
        print "* Incompatible SSH version. Paramiko requires compatible SSH and kex on device %s" % ip


# build list of cdp neighbors from seed level to 2nd level
iplist_second_level = open('/usr/DCDP/tmp/cdp_second_level-pre.txt').readlines()
## remove /n from list elements
iplist_second_level = map(lambda s: s.strip(), iplist_second_level)

# build list of 2nd level sh ip interface brief
first_level_local_IPs = open('/usr/DCDP/tmp/first_level_IPs_SIIB.txt').readlines()
## remove /n from list elements
first_level_local_IPs = map(lambda s: s.strip(), first_level_local_IPs)




########################################################
def second_level_CDP():
    # Remove lower and same level CDP Neighbors from list using set and write to next level cdp file
    # And remove duplicate cdp entries (if any exist) for running the "for loop".......
    # Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries, e.g. nexus connections to itself
    # e.g. below is actually removing entries from first level, even tho it's first level to second level. this is needed. tested in Nexus Data Centers
    # due to OOB management, where Nexus see's itself.
    cdp_second_level = set(iplist_second_level) - set(first_level_local_IPs)
    cdp_second_level_file = open('/usr/DCDP/cdp_files/cdp_second_level.txt', 'w')

    for ip in cdp_second_level:
        cdp_second_level_file.write("%s\n" % ip)
        ## Must have continue here or loop ends and only the first IP is written to the file!
        continue
    # close file once loop completes
    cdp_second_level_file.close()

    # create variable to check if file is zero bytes or NOT....    
    check_second_level_cdp=os.stat("/usr/DCDP/cdp_files/cdp_second_level.txt").st_size == 0

    if check_second_level_cdp == True:
        print "   "
        print "** No more cdp neighbors..."  
        print "   "
        print "   "
        print "** The Network Discovery N Automation Program (NDNA) Has Finished"
        sys.exit()

    else:
        print "______________________________________________" 
        print "   "
        print "** Second level has cdp neighbors. Standby while connecting to Second level devices....."
        print "_____________________________________________" 
        print " __  __            _               _        "
        print "|  \/  |          (_)             | |       "
        print "| \  / | _____   ___ _ __   __ _  | |_ ___  "
        print "| |\/| |/ _ \ \ / / | '_ \ / _` | | __/ _ \ "
        print "| |  | | (_) \ V /| | | | | (_| | | || (_) |"
        print "|_|  |_|\___/ \_/ |_|_| |_|\__, |  \__\___/ "
        print "                            __/ |           "
        print "                           |___/            "
        print " _   _           _     _                    _" 
        print "| \ | |         | |   | |                  | |"
        print "|  \| | _____  _| |_  | |     _____   _____| |"
        print "| . ` |/ _ \ \/ / __| | |    / _ \ \ / / _ \ |"
        print "| |\  |  __/>  <| |_  | |___|  __/\ V /  __/ |"
        print "|_| \_|\___/_/\_ \__| |______\___| \_/ \___|_|"
        print "______________________________________________" 

print "   " 
# call the function
second_level_CDP()
########################################################

iplist_second_level_file_open = open('/usr/DCDP/cdp_files/cdp_second_level.txt').readlines()

## remove /n from list elements
iplist_second_level_file_open = map(lambda s: s.strip(), iplist_second_level_file_open)

def write_files2(ip):
    sema.acquire()
    file_name = '/usr/DCDP/tmp/' + ip + '_2nd_level.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    fo.write(second_level_network_connection(ip))
    fo.close()
    time.sleep(2)
    sema.release()
    
#Creating threads function
def create_threads2():
    threads = []
    for ip in iplist_second_level_file_open: 
        th = threading.Thread(target = write_files2, args = (ip,))   #args is a tuple with a single element     
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function which then calls the open ssh function
create_threads2()

# Build 3rd level CDP IP files from 2nd level device. Run egrep to grep NX-OS and IOS output, e.g. match multiple patterns
subprocess.Popen("cat /usr/DCDP/tmp/*2nd_level.txt | egrep 'IP address|IPv4' | sed -e 's/IP address://' | sed -e 's/IPv4 Address://' | grep -v 0.0.0.0 > /usr/DCDP/tmp/3rd_level_IPs.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# Remove empty spaces
subprocess.Popen("tr -d ' ' < /usr/DCDP/tmp/3rd_level_IPs.txt > /usr/DCDP/tmp/3rd_level_IPs-final.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# grab IPs to exclude from current and next level IPs, e.g. to remove first level IPs from third level
#subprocess.Popen("cat *seed.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' > /usr/DCDP/tmp/first_level_IPs_SIIB.txt", shell=True, stdout=subprocess.PIPE)
#time.sleep(1)

########################################################
# build list of cdp neighbors from 2nd level to 3rd level
iplist_third_level_pre = open('/usr/DCDP/tmp/3rd_level_IPs-final.txt').readlines()
## remove /n from list elements
iplist_third_level_pre = map(lambda s: s.strip(), iplist_third_level_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
# Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
# Commented out line below, as not needed here. Doing it under CDP function below within the variable "cdp_third_level"
# list(set(iplist_third_level))
iplist_third_level = set(iplist_third_level_pre)

subprocess.Popen("cp /usr/DCDP/tmp/first_level_IPs_SIIB.txt /usr/DCDP/tmp/first_second_level_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# append to new siib file (first and second levels) to accommodate current and lower levels
subprocess.Popen("cat /usr/DCDP/tmp/*2nd_level.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' >> /usr/DCDP/tmp/first_second_level_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

subprocess.Popen("cat /usr/DCDP/cdp_files/cdp_second_level.txt >> /usr/DCDP/tmp/first_second_level_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# build list of 1st and 2nd level sh ip interface brief to create new variable
first_second_level_local_IPs_pre = open('/usr/DCDP/tmp/first_second_level_siib.txt').readlines()
## remove /n from list elements
first_second_level_local_IPs_pre = map(lambda s: s.strip(), first_second_level_local_IPs_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
first_second_level_local_IPs = set(first_second_level_local_IPs_pre)
########################################################

########################################################
def third_level_CDP():
    # Remove lower and same level CDP Neighbors from list using set and write to next level cdp file
    # And remove duplicate cdp entries (if any exist) for running the "for loop".......
    # Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
    cdp_third_level = set(iplist_third_level) - set(first_second_level_local_IPs)
    cdp_third_level_file = open('/usr/DCDP/cdp_files/cdp_third_level.txt', 'w')

    for ip in cdp_third_level:
        cdp_third_level_file.write("%s\n" % ip)
        ## Must have continue here or loop ends and only the first IP is written to the file!
        continue
    # close file once loop completes
    cdp_third_level_file.close()

    # create variable to check if file is zero bytes or NOT....    
    check_third_level_cdp=os.stat("/usr/DCDP/cdp_files/cdp_third_level.txt").st_size == 0

    if check_third_level_cdp == True:
        print "   "
        print "** No more cdp neighbors..."
        print "   "
        print "** Preparing final files to use in custom discovery and/or programming"
        # cdp line below must be before seed file
        subprocess.Popen("cat /usr/DCDP/cdp_files/cdp*level.txt > /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        # Seed IP address file MUST be specified last here due to NO carriage return within file. IP or IPs must be last in the file
        # Append to create final version of ip file
        subprocess.Popen("cat /usr/DCDP/cdp_files/seed*address.txt >> /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        print "   "
        print "** The Network Discovery N Automation Program (NDNA) Has Finished"
        sys.exit()

    else:
        print "   "
        print "** Third level has cdp neighbors. Standby while connecting to third level devices....."
        print "   "

print "   "
print "*** Wrapping Up Second Level Devices...Preparing Third Level Connections....."
print "______________________________________________"
print " __  __            _               _        "
print "|  \/  |          (_)             | |       "
print "| \  / | _____   ___ _ __   __ _  | |_ ___  "
print "| |\/| |/ _ \ \ / / | '_ \ / _` | | __/ _ \ "
print "| |  | | (_) \ V /| | | | | (_| | | || (_) |"
print "|_|  |_|\___/ \_/ |_|_| |_|\__, |  \__\___/ "
print "                            __/ |           "
print "                           |___/            "
print " _   _           _     _                    _" 
print "| \ | |         | |   | |                  | |"
print "|  \| | _____  _| |_  | |     _____   _____| |"
print "| . ` |/ _ \ \/ / __| | |    / _ \ \ / / _ \ |"
print "| |\  |  __/>  <| |_  | |___|  __/\ V /  __/ |"
print "|_| \_|\___/_/\_ \__| |______\___| \_/ \___|_|"
print "______________________________________________"                                            
# call the function
third_level_CDP()
########################################################

#Open SSHv2 connection to 3rd level devices
def third_level_network_connection(ip):
    try:
        paramiko.util.log_to_file("/usr/DCDP/logs/paramiko.log")
        #Logging into device
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Passing the necessary parameters
        session.connect(ip, username = username, password = password, look_for_keys=False)
        
    #Start an interactive shell session on the router
        connection = session.invoke_shell() 
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        print ".... "
        time.sleep(8)
        connection.send("sh cdp nei detail | i IP\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief vrf all\n")
        time.sleep(8)
        connection.send("sh version\n")
        time.sleep(8)

#############################################################
        # Get around the 64K bytes (65536). paramiko limitation
        interval = 0.1
        maxseconds = 15
        maxcount = maxseconds / interval
        bufsize = 65535

        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        router_output = ''

        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode('ascii')
                router_output += data

            if connection.exit_status_ready():
                break

            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())

            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break

            rbuffer = router_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            router_output += data.decode('ascii')
#############################################################

        if re.search(r"% Invalid input detected at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"% Invalid command at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"Incorrect usage", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"Cisco Controller", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"User:", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"% Authorization failed", router_output):
            print "   "
            print "** Authorization failed for %s Looks Like a TACACS issue." % ip
            
        else:
            print "   "
            print "** Completed device %s" % ip

        return router_output
    
    #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        pass
        print "   "
        print "* Authentication Error for %s" % ip
        print "   "
        #print "* Closing program...\n"
    except paramiko.SSHException:
        pass
        print "   "
        print "* Incompatible SSH version. Paramiko requires compatible SSH and kex on device %s" % ip


cdp_list_third_level = open('/usr/DCDP/cdp_files/cdp_third_level.txt').readlines()
## remove /n from list elements
cdp_list_third_level = map(lambda s: s.strip(), cdp_list_third_level)

def write_files3(ip):
    sema.acquire()
    file_name = '/usr/DCDP/tmp/' + ip + '_3rd_level.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    fo.write(third_level_network_connection(ip))
    fo.close()
    time.sleep(2)
    sema.release()

#Creating threads function
def create_threads3():
    threads = []
    for ip in cdp_list_third_level: 
        th = threading.Thread(target = write_files3, args = (ip,))   #args is a tuple with a single element     
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function which then calls the open ssh function
create_threads3()
##########################
##########################
##########################
##########################
# Build 4th level CDP IP files from 3rd level device. Run egrep to grep NX-OS and IOS output, e.g. match multiple patterns
subprocess.Popen("cat /usr/DCDP/tmp/*3rd_level.txt | egrep 'IP address|IPv4' | sed -e 's/IP address://' | sed -e 's/IPv4 Address://' | grep -v 0.0.0.0 > /usr/DCDP/tmp/4th_level_IPs.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# Remove empty spaces
subprocess.Popen("tr -d ' ' < /usr/DCDP/tmp/4th_level_IPs.txt > /usr/DCDP/tmp/4th_level_IPs-final.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# grab IPs to exclude from current and next level IPs, e.g. to remove first level IPs from fourth level
#subprocess.Popen("cat *seed.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' > /usr/DCDP/tmp/first_level_IPs_SIIB.txt", shell=True, stdout=subprocess.PIPE)
#time.sleep(1)

########################################################
# build list of cdp neighbors from 3rd level to 4th level
iplist_fourth_level_pre = open('/usr/DCDP/tmp/4th_level_IPs-final.txt').readlines()
## remove /n from list elements
iplist_fourth_level_pre = map(lambda s: s.strip(), iplist_fourth_level_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
# Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
# Commented out line below, as not needed here. Doing it under CDP function below within the variable "cdp_fourth_level"
# list(set(iplist_fourth_level))
iplist_fourth_level = set(iplist_fourth_level_pre)

subprocess.Popen("cp /usr/DCDP/tmp/first_second_level_siib.txt /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# append to new siib file (all previous levels) to accommodate current and lower levels - includes cdp neighbors and local IPs
subprocess.Popen("cat /usr/DCDP/tmp/*3rd_level.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

subprocess.Popen("cat /usr/DCDP/cdp_files/cdp_third_level.txt >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# build list of current and all previous levels sh ip interface brief and cdp nei IPs to create new variable
all_previous_levels_local_IPs_pre = open('/usr/DCDP/tmp/all_previous_levels_siib.txt').readlines()
## remove /n from list elements
all_previous_levels_local_IPs_pre = map(lambda s: s.strip(), all_previous_levels_local_IPs_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
all_previous_levels_local_IPs = set(all_previous_levels_local_IPs_pre)
########################################################

########################################################
def fourth_level_CDP():
    # Remove lower and same level CDP Neighbors from list using set and write to next level cdp file
    # And remove duplicate cdp entries (if any exist) for running the "for loop".......
    # Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
    cdp_fourth_level = set(iplist_fourth_level) - set(all_previous_levels_local_IPs)
    cdp_fourth_level_file = open('/usr/DCDP/cdp_files/cdp_fourth_level.txt', 'w')

    for ip in cdp_fourth_level:
        cdp_fourth_level_file.write("%s\n" % ip)
        ## Must have continue here or loop ends and only the first IP is written to the file!
        continue
    # close file once loop completes
    cdp_fourth_level_file.close()

    # create variable to check if file is zero bytes or NOT....    
    check_fourth_level_cdp=os.stat("/usr/DCDP/cdp_files/cdp_fourth_level.txt").st_size == 0

    if check_fourth_level_cdp == True:
        print "   "
        print "** No more cdp neighbors..."
        print "   "
        print "** Preparing final files to use in custom discovery and/or programming"
        # cdp line below must be before seed file
        subprocess.Popen("cat /usr/DCDP/cdp_files/cdp*level.txt > /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        # Seed IP address file MUST be specified last here due to NO carriage return within file. IP or IPs must be last in the file
        # Append to create final version of ip file
        subprocess.Popen("cat /usr/DCDP/cdp_files/seed*address.txt >> /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)

        print "   "
        print "** The Network Discovery N Automation Program (NDNA) Has Finished"
        sys.exit()

    else:
        print "   "
        print "** fourth level has cdp neighbors. Standby while connecting to fourth level devices....."
        print "   "

print "   "
print "*** Wrapping Up Third Level Devices...Preparing Fourth Level Connections....."
print "______________________________________________"
print " __  __            _               _        "
print "|  \/  |          (_)             | |       "
print "| \  / | _____   ___ _ __   __ _  | |_ ___  "
print "| |\/| |/ _ \ \ / / | '_ \ / _` | | __/ _ \ "
print "| |  | | (_) \ V /| | | | | (_| | | || (_) |"
print "|_|  |_|\___/ \_/ |_|_| |_|\__, |  \__\___/ "
print "                            __/ |           "
print "                           |___/            "
print " _   _           _     _                    _" 
print "| \ | |         | |   | |                  | |"
print "|  \| | _____  _| |_  | |     _____   _____| |"
print "| . ` |/ _ \ \/ / __| | |    / _ \ \ / / _ \ |"
print "| |\  |  __/>  <| |_  | |___|  __/\ V /  __/ |"
print "|_| \_|\___/_/\_ \__| |______\___| \_/ \___|_|"
print "______________________________________________"   
# call the function
fourth_level_CDP()
########################################################

#Open SSHv2 connection to 4th level devices
def fourth_level_network_connection(ip):
    try:
        paramiko.util.log_to_file("/usr/DCDP/logs/paramiko.log")
        #Logging into device
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Passing the necessary parameters
        session.connect(ip, username = username, password = password, look_for_keys=False)
        
    #Start an interactive shell session on the router
        connection = session.invoke_shell() 
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        print ".... "
        time.sleep(8)
        connection.send("sh cdp nei detail | i IP\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief vrf all\n")
        time.sleep(8)
        connection.send("sh version\n")
        time.sleep(8)

#############################################################
        # Get around the 64K bytes (65536). paramiko limitation
        interval = 0.1
        maxseconds = 15
        maxcount = maxseconds / interval
        bufsize = 65535

        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        router_output = ''

        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode('ascii')
                router_output += data

            if connection.exit_status_ready():
                break

            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())

            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break

            rbuffer = router_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            router_output += data.decode('ascii')
#############################################################
        
        if re.search(r"% Invalid input detected at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"% Invalid command at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"Incorrect usage", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"Cisco Controller", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"User:", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"% Authorization failed", router_output):
            print "   "
            print "** Authorization failed for %s Looks Like a TACACS issue." % ip
            
        else:
            print "   "
            print "** Completed device %s" % ip

        return router_output
    
    #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        pass
        print "   "
        print "* Authentication Error for %s" % ip
        print "   "
        #print "* Closing program...\n"
    except paramiko.SSHException:
        pass
        print "   "
        print "* Incompatible SSH version. Paramiko requires compatible SSH and kex on device %s" % ip


cdp_list_fourth_level = open('/usr/DCDP/cdp_files/cdp_fourth_level.txt').readlines()
## remove /n from list elements
cdp_list_fourth_level = map(lambda s: s.strip(), cdp_list_fourth_level)

def write_files4(ip):
    sema.acquire()
    file_name = '/usr/DCDP/tmp/' + ip + '_4th_level.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    fo.write(fourth_level_network_connection(ip))
    fo.close()
    time.sleep(2)
    sema.release()

#Creating threads function
def create_threads4():
    threads = []
    for ip in cdp_list_fourth_level: 
        th = threading.Thread(target = write_files4, args = (ip,))   #args is a tuple with a single element     
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function which then calls the open ssh function
create_threads4()
##########################

##########################
##########################
# Build 5th level CDP IP files from 4th level device. Run egrep to grep NX-OS and IOS output, e.g. match multiple patterns
subprocess.Popen("cat /usr/DCDP/tmp/*4th_level.txt | egrep 'IP address|IPv4' | sed -e 's/IP address://' | sed -e 's/IPv4 Address://' | grep -v 0.0.0.0 > /usr/DCDP/tmp/5th_level_IPs.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# Remove empty spaces
subprocess.Popen("tr -d ' ' < /usr/DCDP/tmp/5th_level_IPs.txt > /usr/DCDP/tmp/5th_level_IPs-final.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# grab IPs to exclude from current and next level IPs, e.g. to remove first level IPs from fourth level
#subprocess.Popen("cat *seed.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' > /usr/DCDP/tmp/first_level_IPs_SIIB.txt", shell=True, stdout=subprocess.PIPE)
#time.sleep(1)

########################################################
# build list of cdp neighbors from 4th level to 5th level
iplist_fifth_level_pre = open('/usr/DCDP/tmp/5th_level_IPs-final.txt').readlines()
## remove /n from list elements
iplist_fifth_level_pre = map(lambda s: s.strip(), iplist_fifth_level_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
# Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
# Commented out line below, as not needed here. Doing it under CDP function below within the variable "cdp_fourth_level"
# list(set(iplist_fourth_level))
iplist_fifth_level = set(iplist_fifth_level_pre)


# append to new siib file (all previous levels) to accommodate current and lower levels - includes cdp neighbors and local IPs
subprocess.Popen("cat /usr/DCDP/tmp/*4th_level.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

subprocess.Popen("cat /usr/DCDP/cdp_files/cdp_fourth_level.txt >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# build list of current and all previous levels sh ip interface brief and cdp nei IPs to create new variable
all_previous_levels_local_IPs_pre = open('/usr/DCDP/tmp/all_previous_levels_siib.txt').readlines()
## remove /n from list elements
all_previous_levels_local_IPs_pre = map(lambda s: s.strip(), all_previous_levels_local_IPs_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
all_previous_levels_local_IPs = set(all_previous_levels_local_IPs_pre)
########################################################

########################################################
def fifth_level_CDP():
    # Remove lower and same level CDP Neighbors from list using set and write to next level cdp file
    # And remove duplicate cdp entries (if any exist) for running the "for loop".......
    # Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
    cdp_fifth_level = set(iplist_fifth_level) - set(all_previous_levels_local_IPs)
    cdp_fifth_level_file = open('/usr/DCDP/cdp_files/cdp_fifth_level.txt', 'w')

    for ip in cdp_fifth_level:
        cdp_fifth_level_file.write("%s\n" % ip)
        ## Must have continue here or loop ends and only the first IP is written to the file!
        continue
    # close file once loop completes
    cdp_fifth_level_file.close()

    # create variable to check if file is zero bytes or NOT....    
    check_fifth_level_cdp=os.stat("/usr/DCDP/cdp_files/cdp_fifth_level.txt").st_size == 0

    if check_fifth_level_cdp == True:
        print "   "
        print "** No more cdp neighbors..."
        print "   "
        print "** Preparing final files to use in custom discovery and/or programming"
        # cdp line below must be before seed file
        subprocess.Popen("cat /usr/DCDP/cdp_files/cdp*level.txt > /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        # Seed IP address file MUST be specified last here due to NO carriage return within file. IP or IPs must be last in the file
        # Append to create final version of ip file
        subprocess.Popen("cat /usr/DCDP/cdp_files/seed*address.txt >> /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)

        print "   "
        print "** The Network Discovery N Automation Program (NDNA) Has Finished"
        sys.exit()

    else:
        print "   "
        print "** fifth level has cdp neighbors. Standby while connecting to fifth level devices....."
        print "   "

print "   "
print "*** Wrapping Up Fourth Level Devices...Preparing Fifth Level Connections....."
print "______________________________________________"
print " __  __            _               _        "
print "|  \/  |          (_)             | |       "
print "| \  / | _____   ___ _ __   __ _  | |_ ___  "
print "| |\/| |/ _ \ \ / / | '_ \ / _` | | __/ _ \ "
print "| |  | | (_) \ V /| | | | | (_| | | || (_) |"
print "|_|  |_|\___/ \_/ |_|_| |_|\__, |  \__\___/ "
print "                            __/ |           "
print "                           |___/            "
print " _   _           _     _                    _" 
print "| \ | |         | |   | |                  | |"
print "|  \| | _____  _| |_  | |     _____   _____| |"
print "| . ` |/ _ \ \/ / __| | |    / _ \ \ / / _ \ |"
print "| |\  |  __/>  <| |_  | |___|  __/\ V /  __/ |"
print "|_| \_|\___/_/\_ \__| |______\___| \_/ \___|_|"
print "______________________________________________"   
# call the function
fifth_level_CDP()
########################################################

#Open SSHv2 connection to 5th level devices
def fifth_level_network_connection(ip):
    try:
        paramiko.util.log_to_file("/usr/DCDP/logs/paramiko.log")
        #Logging into device
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Passing the necessary parameters
        session.connect(ip, username = username, password = password, look_for_keys=False)
        
    #Start an interactive shell session on the router
        connection = session.invoke_shell() 
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        print ".... "
        time.sleep(8)
        connection.send("sh cdp nei detail | i IP\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief vrf all\n")
        time.sleep(8)
        connection.send("sh version\n")
        time.sleep(8)

#############################################################
        # Get around the 64K bytes (65536). paramiko limitation
        interval = 0.1
        maxseconds = 15
        maxcount = maxseconds / interval
        bufsize = 65535

        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        router_output = ''

        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode('ascii')
                router_output += data

            if connection.exit_status_ready():
                break

            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())

            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break

            rbuffer = router_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            router_output += data.decode('ascii')
#############################################################
        
        if re.search(r"% Invalid input detected at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"% Invalid command at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"Incorrect usage", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"Cisco Controller", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"User:", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"% Authorization failed", router_output):
            print "   "
            print "** Authorization failed for %s Looks Like a TACACS issue." % ip
            
        else:
            print "   "
            print "** Completed device %s" % ip

        return router_output
    
    #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        pass
        print "   "
        print "* Authentication Error for %s" % ip
        print "   "
        #print "* Closing program...\n"
    except paramiko.SSHException:
        pass
        print "   "
        print "* Incompatible SSH version. Paramiko requires compatible SSH and kex on device %s" % ip


cdp_list_fifth_level = open('/usr/DCDP/cdp_files/cdp_fifth_level.txt').readlines()
## remove /n from list elements
cdp_list_fifth_level = map(lambda s: s.strip(), cdp_list_fifth_level)

def write_files5(ip):
    sema.acquire()
    file_name = '/usr/DCDP/tmp/' + ip + '_5th_level.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    fo.write(fifth_level_network_connection(ip))
    fo.close()
    time.sleep(2)
    sema.release()

#Creating threads function
def create_threads5():
    threads = []
    for ip in cdp_list_fifth_level: 
        th = threading.Thread(target = write_files5, args = (ip,))   #args is a tuple with a single element     
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function which then calls the open ssh function
create_threads5()
##########################


##########################
##########################
# Build 6th level CDP IP files from 5th level device. Run egrep to grep NX-OS and IOS output, e.g. match multiple patterns
subprocess.Popen("cat /usr/DCDP/tmp/*5th_level.txt | egrep 'IP address|IPv4' | sed -e 's/IP address://' | sed -e 's/IPv4 Address://' | grep -v 0.0.0.0 > /usr/DCDP/tmp/6th_level_IPs.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# Remove empty spaces
subprocess.Popen("tr -d ' ' < /usr/DCDP/tmp/6th_level_IPs.txt > /usr/DCDP/tmp/6th_level_IPs-final.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# grab IPs to exclude from current and next level IPs, e.g. to remove first level IPs from fourth level
#subprocess.Popen("cat *seed.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' > /usr/DCDP/tmp/first_level_IPs_SIIB.txt", shell=True, stdout=subprocess.PIPE)
#time.sleep(1)

########################################################
# build list of cdp neighbors from 5th level to 6th level
iplist_sixth_level_pre = open('/usr/DCDP/tmp/6th_level_IPs-final.txt').readlines()
## remove /n from list elements
iplist_sixth_level_pre = map(lambda s: s.strip(), iplist_sixth_level_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
# Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
# Commented out line below, as not needed here. Doing it under CDP function below within the variable "cdp_fourth_level"
# list(set(iplist_fourth_level))
iplist_sixth_level = set(iplist_sixth_level_pre)


# append to new siib file (all previous levels) to accommodate current and lower levels - includes cdp neighbors and local IPs
subprocess.Popen("cat /usr/DCDP/tmp/*5th_level.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

subprocess.Popen("cat /usr/DCDP/cdp_files/cdp_fifth_level.txt >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# build list of current and all previous levels sh ip interface brief and cdp nei IPs to create new variable
all_previous_levels_local_IPs_pre = open('/usr/DCDP/tmp/all_previous_levels_siib.txt').readlines()
## remove /n from list elements
all_previous_levels_local_IPs_pre = map(lambda s: s.strip(), all_previous_levels_local_IPs_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
all_previous_levels_local_IPs = set(all_previous_levels_local_IPs_pre)
########################################################

########################################################
def sixth_level_CDP():
    # Remove lower and same level CDP Neighbors from list using set and write to next level cdp file
    # And remove duplicate cdp entries (if any exist) for running the "for loop".......
    # Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
    cdp_sixth_level = set(iplist_sixth_level) - set(all_previous_levels_local_IPs)
    cdp_sixth_level_file = open('/usr/DCDP/cdp_files/cdp_sixth_level.txt', 'w')

    for ip in cdp_sixth_level:
        cdp_sixth_level_file.write("%s\n" % ip)
        ## Must have continue here or loop ends and only the first IP is written to the file!
        continue
    # close file once loop completes
    cdp_sixth_level_file.close()

    # create variable to check if file is zero bytes or NOT....    
    check_sixth_level_cdp=os.stat("/usr/DCDP/cdp_files/cdp_sixth_level.txt").st_size == 0

    if check_sixth_level_cdp == True:
        print "   "
        print "** No more cdp neighbors..."
        print "   "
        print "** Preparing final files to use in custom discovery and/or programming"
        # cdp line below must be before seed file
        subprocess.Popen("cat /usr/DCDP/cdp_files/cdp*level.txt > /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        # Seed IP address file MUST be specified last here due to NO carriage return within file. IP or IPs must be last in the file
        # Append to create final version of ip file
        subprocess.Popen("cat /usr/DCDP/cdp_files/seed*address.txt >> /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)

        print "   "
        print "** The Network Discovery N Automation Program (NDNA) Has Finished"
        sys.exit()

    else:
        print "   "
        print "** sixth level has cdp neighbors. Standby while connecting to sixth level devices....."
        print "   "

print "   "
print "*** Wrapping Up Fifth Level Devices...Preparing Sixth Level Connections....."
print "______________________________________________"
print " __  __            _               _        "
print "|  \/  |          (_)             | |       "
print "| \  / | _____   ___ _ __   __ _  | |_ ___  "
print "| |\/| |/ _ \ \ / / | '_ \ / _` | | __/ _ \ "
print "| |  | | (_) \ V /| | | | | (_| | | || (_) |"
print "|_|  |_|\___/ \_/ |_|_| |_|\__, |  \__\___/ "
print "                            __/ |           "
print "                           |___/            "
print " _   _           _     _                    _" 
print "| \ | |         | |   | |                  | |"
print "|  \| | _____  _| |_  | |     _____   _____| |"
print "| . ` |/ _ \ \/ / __| | |    / _ \ \ / / _ \ |"
print "| |\  |  __/>  <| |_  | |___|  __/\ V /  __/ |"
print "|_| \_|\___/_/\_ \__| |______\___| \_/ \___|_|"
print "______________________________________________"   
# call the function
sixth_level_CDP()
########################################################

#Open SSHv2 connection to 5th level devices
def sixth_level_network_connection(ip):
    try:
        paramiko.util.log_to_file("/usr/DCDP/logs/paramiko.log")
        #Logging into device
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Passing the necessary parameters
        session.connect(ip, username = username, password = password, look_for_keys=False)
        
    #Start an interactive shell session on the router
        connection = session.invoke_shell() 
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        print ".... "
        time.sleep(8)
        connection.send("sh cdp nei detail | i IP\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief vrf all\n")
        time.sleep(8)
        connection.send("sh version\n")
        time.sleep(8)

#############################################################
        # Get around the 64K bytes (65536). paramiko limitation
        interval = 0.1
        maxseconds = 15
        maxcount = maxseconds / interval
        bufsize = 65535

        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        router_output = ''

        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode('ascii')
                router_output += data

            if connection.exit_status_ready():
                break

            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())

            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break

            rbuffer = router_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            router_output += data.decode('ascii')
#############################################################
        
        if re.search(r"% Invalid input detected at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"% Invalid command at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"Incorrect usage", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"Cisco Controller", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"User:", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"% Authorization failed", router_output):
            print "   "
            print "** Authorization failed for %s Looks Like a TACACS issue." % ip
            
        else:
            print "   "
            print "** Completed device %s" % ip

        return router_output
    
    #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        pass
        print "   "
        print "* Authentication Error for %s" % ip
        print "   "
        #print "* Closing program...\n"
    except paramiko.SSHException:
        pass
        print "   "
        print "* Incompatible SSH version. Paramiko requires compatible SSH and kex on device %s" % ip


cdp_list_sixth_level = open('/usr/DCDP/cdp_files/cdp_sixth_level.txt').readlines()
## remove /n from list elements
cdp_list_sixth_level = map(lambda s: s.strip(), cdp_list_sixth_level)

def write_files6(ip):
    sema.acquire()
    file_name = '/usr/DCDP/tmp/' + ip + '_6th_level.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    fo.write(sixth_level_network_connection(ip))
    fo.close()
    time.sleep(2)
    sema.release()
    
#Creating threads function
def create_threads6():
    threads = []
    for ip in cdp_list_sixth_level: 
        th = threading.Thread(target = write_files6, args = (ip,))   #args is a tuple with a single element     
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function which then calls the open ssh function
create_threads6()
##########################

##########################
##########################
# Build 7th level CDP IP files from 6th level device. Run egrep to grep NX-OS and IOS output, e.g. match multiple patterns
subprocess.Popen("cat /usr/DCDP/tmp/*6th_level.txt | egrep 'IP address|IPv4' | sed -e 's/IP address://' | sed -e 's/IPv4 Address://' | grep -v 0.0.0.0 > /usr/DCDP/tmp/7th_level_IPs.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# Remove empty spaces
subprocess.Popen("tr -d ' ' < /usr/DCDP/tmp/7th_level_IPs.txt > /usr/DCDP/tmp/7th_level_IPs-final.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# grab IPs to exclude from current and next level IPs, e.g. to remove first level IPs from fourth level
#subprocess.Popen("cat *seed.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' > /usr/DCDP/tmp/first_level_IPs_SIIB.txt", shell=True, stdout=subprocess.PIPE)
#time.sleep(1)

########################################################
# build list of cdp neighbors from 6th level to 7th level
iplist_seventh_level_pre = open('/usr/DCDP/tmp/7th_level_IPs-final.txt').readlines()
## remove /n from list elements
iplist_seventh_level_pre = map(lambda s: s.strip(), iplist_seventh_level_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
# Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
# Commented out line below, as not needed here. Doing it under CDP function below within the variable "cdp_fourth_level"
# list(set(iplist_fourth_level))
iplist_seventh_level = set(iplist_seventh_level_pre)


# append to new siib file (all previous levels) to accommodate current and lower levels - includes cdp neighbors and local IPs
subprocess.Popen("cat /usr/DCDP/tmp/*6th_level.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

subprocess.Popen("cat /usr/DCDP/cdp_files/cdp_sixth_level.txt >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# build list of current and all previous levels sh ip interface brief and cdp nei IPs to create new variable
all_previous_levels_local_IPs_pre = open('/usr/DCDP/tmp/all_previous_levels_siib.txt').readlines()
## remove /n from list elements
all_previous_levels_local_IPs_pre = map(lambda s: s.strip(), all_previous_levels_local_IPs_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
all_previous_levels_local_IPs = set(all_previous_levels_local_IPs_pre)
########################################################

########################################################
def seventh_level_CDP():
    # Remove lower and same level CDP Neighbors from list using set and write to next level cdp file
    # And remove duplicate cdp entries (if any exist) for running the "for loop".......
    # Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
    cdp_seventh_level = set(iplist_seventh_level) - set(all_previous_levels_local_IPs)
    cdp_seventh_level_file = open('/usr/DCDP/cdp_files/cdp_seventh_level.txt', 'w')

    for ip in cdp_seventh_level:
        cdp_seventh_level_file.write("%s\n" % ip)
        ## Must have continue here or loop ends and only the first IP is written to the file!
        continue
    # close file once loop completes
    cdp_seventh_level_file.close()

    # create variable to check if file is zero bytes or NOT....    
    check_seventh_level_cdp=os.stat("/usr/DCDP/cdp_files/cdp_seventh_level.txt").st_size == 0

    if check_seventh_level_cdp == True:
        print "   "
        print "** No more cdp neighbors..."
        print "   "
        print "** Preparing final files to use in custom discovery and/or programming"
        # cdp line below must be before seed file
        subprocess.Popen("cat /usr/DCDP/cdp_files/cdp*level.txt > /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        # Seed IP address file MUST be specified last here due to NO carriage return within file. IP or IPs must be last in the file
        # Append to create final version of ip file
        subprocess.Popen("cat /usr/DCDP/cdp_files/seed*address.txt >> /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)

        print "   "
        print "** The Network Discovery N Automation Program (NDNA) Has Finished"
        sys.exit()

    else:
        print "   "
        print "** seventh level has cdp neighbors. Standby while connecting to seventh level devices....."
        print "   "

print "   "
print "*** Wrapping Up Sixth Level Devices...Preparing Seventh Level Connections....."
print "______________________________________________"
print " __  __            _               _        "
print "|  \/  |          (_)             | |       "
print "| \  / | _____   ___ _ __   __ _  | |_ ___  "
print "| |\/| |/ _ \ \ / / | '_ \ / _` | | __/ _ \ "
print "| |  | | (_) \ V /| | | | | (_| | | || (_) |"
print "|_|  |_|\___/ \_/ |_|_| |_|\__, |  \__\___/ "
print "                            __/ |           "
print "                           |___/            "
print " _   _           _     _                    _" 
print "| \ | |         | |   | |                  | |"
print "|  \| | _____  _| |_  | |     _____   _____| |"
print "| . ` |/ _ \ \/ / __| | |    / _ \ \ / / _ \ |"
print "| |\  |  __/>  <| |_  | |___|  __/\ V /  __/ |"
print "|_| \_|\___/_/\_ \__| |______\___| \_/ \___|_|"
print "______________________________________________"   
# call the function
seventh_level_CDP()
########################################################

#Open SSHv2 connection to 7th level devices
def seventh_level_network_connection(ip):
    try:
        paramiko.util.log_to_file("/usr/DCDP/logs/paramiko.log")
        #Logging into device
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Passing the necessary parameters
        session.connect(ip, username = username, password = password, look_for_keys=False)
        
    #Start an interactive shell session on the router
        connection = session.invoke_shell() 
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        print ".... "
        time.sleep(8)
        connection.send("sh cdp nei detail | i IP\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief vrf all\n")
        time.sleep(8)
        connection.send("sh version\n")
        time.sleep(8)

#############################################################
        # Get around the 64K bytes (65536). paramiko limitation
        interval = 0.1
        maxseconds = 15
        maxcount = maxseconds / interval
        bufsize = 65535

        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        router_output = ''

        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode('ascii')
                router_output += data

            if connection.exit_status_ready():
                break

            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())

            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break

            rbuffer = router_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            router_output += data.decode('ascii')
#############################################################
        
        if re.search(r"% Invalid input detected at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"% Invalid command at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"Incorrect usage", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"Cisco Controller", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"User:", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"% Authorization failed", router_output):
            print "   "
            print "** Authorization failed for %s Looks Like a TACACS issue." % ip
            
        else:
            print "   "
            print "** Completed device %s" % ip

        return router_output
    
    #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        pass
        print "   "
        print "* Authentication Error for %s" % ip
        print "   "
        #print "* Closing program...\n"
    except paramiko.SSHException:
        pass
        print "   "
        print "* Incompatible SSH version. Paramiko requires compatible SSH and kex on device %s" % ip


cdp_list_seventh_level = open('/usr/DCDP/cdp_files/cdp_seventh_level.txt').readlines()              
## remove /n from list elements
cdp_list_seventh_level = map(lambda s: s.strip(), cdp_list_seventh_level)

def write_files7(ip):
    sema.acquire()
    file_name = '/usr/DCDP/tmp/' + ip + '_7th_level.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    fo.write(seventh_level_network_connection(ip))
    fo.close()
    time.sleep(2)
    sema.release()

#Creating threads function
def create_threads7():
    threads = []
    for ip in cdp_list_seventh_level: 
        th = threading.Thread(target = write_files7, args = (ip,))   #args is a tuple with a single element     
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function which then calls the open ssh function
create_threads7()

##########################
##########################
# Build 8th level CDP IP files from 7th level device. Run egrep to grep NX-OS and IOS output, e.g. match multiple patterns
subprocess.Popen("cat /usr/DCDP/tmp/*7th_level.txt | egrep 'IP address|IPv4' | sed -e 's/IP address://' | sed -e 's/IPv4 Address://' | grep -v 0.0.0.0 > /usr/DCDP/tmp/8th_level_IPs.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# Remove empty spaces
subprocess.Popen("tr -d ' ' < /usr/DCDP/tmp/8th_level_IPs.txt > /usr/DCDP/tmp/8th_level_IPs-final.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# grab IPs to exclude from current and next level IPs, e.g. to remove first level IPs from fourth level
#subprocess.Popen("cat *seed.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' > /usr/DCDP/tmp/first_level_IPs_SIIB.txt", shell=True, stdout=subprocess.PIPE)
#time.sleep(1)

########################################################
# build list of cdp neighbors from 7th level to 8th level
iplist_eighth_level_pre = open('/usr/DCDP/tmp/8th_level_IPs-final.txt').readlines()
## remove /n from list elements
iplist_eighth_level_pre = map(lambda s: s.strip(), iplist_eighth_level_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
# Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
# Commented out line below, as not needed here. Doing it under CDP function below within the variable "cdp_fourth_level"
# list(set(iplist_fourth_level))
iplist_eighth_level = set(iplist_eighth_level_pre)


# append to new siib file (all previous levels) to accommodate current and lower levels - includes cdp neighbors and local IPs
subprocess.Popen("cat /usr/DCDP/tmp/*7th_level.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

subprocess.Popen("cat /usr/DCDP/cdp_files/cdp_seventh_level.txt >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# build list of current and all previous levels sh ip interface brief and cdp nei IPs to create new variable
all_previous_levels_local_IPs_pre = open('/usr/DCDP/tmp/all_previous_levels_siib.txt').readlines()
## remove /n from list elements
all_previous_levels_local_IPs_pre = map(lambda s: s.strip(), all_previous_levels_local_IPs_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
all_previous_levels_local_IPs = set(all_previous_levels_local_IPs_pre)
########################################################

########################################################
def eighth_level_CDP():
    # Remove lower and same level CDP Neighbors from list using set and write to next level cdp file
    # And remove duplicate cdp entries (if any exist) for running the "for loop".......
    # Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
    cdp_eighth_level = set(iplist_eighth_level) - set(all_previous_levels_local_IPs)
    cdp_eighth_level_file = open('/usr/DCDP/cdp_files/cdp_eighth_level.txt', 'w')

    for ip in cdp_eighth_level:
        cdp_eighth_level_file.write("%s\n" % ip)
        ## Must have continue here or loop ends and only the first IP is written to the file!
        continue
    # close file once loop completes
    cdp_eighth_level_file.close()

    # create variable to check if file is zero bytes or NOT....    
    check_eighth_level_cdp=os.stat("/usr/DCDP/cdp_files/cdp_eighth_level.txt").st_size == 0

    if check_eighth_level_cdp == True:
        print "   "
        print "** No more cdp neighbors..."
        print "   "
        print "** Preparing final files to use in custom discovery and/or programming"
        # cdp line below must be before seed file
        subprocess.Popen("cat /usr/DCDP/cdp_files/cdp*level.txt > /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        # Seed IP address file MUST be specified last here due to NO carriage return within file. IP or IPs must be last in the file
        # Append to create final version of ip file
        subprocess.Popen("cat /usr/DCDP/cdp_files/seed*address.txt >> /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)

        print "   "
        print "** The Network Discovery N Automation Program (NDNA) Has Finished"
        sys.exit()

    else:
        print "   "
        print "** eighth level has cdp neighbors. Standby while connecting to eighth level devices....."
        print "   "

print "   "
print "*** Wrapping Up Seventh Level Devices...Preparing Eighth Level Connections....."
print "______________________________________________"
print " __  __            _               _        "
print "|  \/  |          (_)             | |       "
print "| \  / | _____   ___ _ __   __ _  | |_ ___  "
print "| |\/| |/ _ \ \ / / | '_ \ / _` | | __/ _ \ "
print "| |  | | (_) \ V /| | | | | (_| | | || (_) |"
print "|_|  |_|\___/ \_/ |_|_| |_|\__, |  \__\___/ "
print "                            __/ |           "
print "                           |___/            "
print " _   _           _     _                    _" 
print "| \ | |         | |   | |                  | |"
print "|  \| | _____  _| |_  | |     _____   _____| |"
print "| . ` |/ _ \ \/ / __| | |    / _ \ \ / / _ \ |"
print "| |\  |  __/>  <| |_  | |___|  __/\ V /  __/ |"
print "|_| \_|\___/_/\_ \__| |______\___| \_/ \___|_|"
print "______________________________________________"   
# call the function
eighth_level_CDP()
########################################################

#Open SSHv2 connection to 8th level devices
def eighth_level_network_connection(ip):
    try:
        paramiko.util.log_to_file("/usr/DCDP/logs/paramiko.log")
        #Logging into device
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Passing the necessary parameters
        session.connect(ip, username = username, password = password, look_for_keys=False)
        
    #Start an interactive shell session on the router
        connection = session.invoke_shell() 
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        print ".... "
        time.sleep(8)
        connection.send("sh cdp nei detail | i IP\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief vrf all\n")
        time.sleep(8)
        connection.send("sh version\n")
        time.sleep(8)


#############################################################
        # Get around the 64K bytes (65536). paramiko limitation
        interval = 0.1
        maxseconds = 15
        maxcount = maxseconds / interval
        bufsize = 65535

        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        router_output = ''

        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode('ascii')
                router_output += data

            if connection.exit_status_ready():
                break

            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())

            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break

            rbuffer = router_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            router_output += data.decode('ascii')
#############################################################
        
        if re.search(r"% Invalid input detected at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"% Invalid command at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"Incorrect usage", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"Cisco Controller", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"User:", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"% Authorization failed", router_output):
            print "   "
            print "** Authorization failed for %s Looks Like a TACACS issue." % ip
            
        else:
            print "   "
            print "** Completed device %s" % ip

        return router_output
    
    #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        pass
        print "   "
        print "* Authentication Error for %s" % ip
        print "   "
        #print "* Closing program...\n"
    except paramiko.SSHException:
        pass
        print "   "
        print "* Incompatible SSH version. Paramiko requires compatible SSH and kex on device %s" % ip


cdp_list_eighth_level = open('/usr/DCDP/cdp_files/cdp_eighth_level.txt').readlines()
## remove /n from list elements
cdp_list_eighth_level = map(lambda s: s.strip(), cdp_list_eighth_level)

def write_files8(ip):
    sema.acquire()
    file_name = '/usr/DCDP/tmp/' + ip + '_8th_level.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    fo.write(eighth_level_network_connection(ip))
    fo.close()
    time.sleep(2)
    sema.release()

#Creating threads function
def create_threads8():
    threads = []
    for ip in cdp_list_eighth_level: 
        th = threading.Thread(target = write_files8, args = (ip,))   #args is a tuple with a single element     
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function which then calls the open ssh function
create_threads8()


##########################
##########################
# Build 9th level CDP IP files from 8th level device. Run egrep to grep NX-OS and IOS output, e.g. match multiple patterns
subprocess.Popen("cat /usr/DCDP/tmp/*8th_level.txt | egrep 'IP address|IPv4' | sed -e 's/IP address://' | sed -e 's/IPv4 Address://' | grep -v 0.0.0.0 > /usr/DCDP/tmp/9th_level_IPs.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# Remove empty spaces
subprocess.Popen("tr -d ' ' < /usr/DCDP/tmp/9th_level_IPs.txt > /usr/DCDP/tmp/9th_level_IPs-final.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# grab IPs to exclude from current and next level IPs, e.g. to remove first level IPs from fourth level
#subprocess.Popen("cat *seed.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' > /usr/DCDP/tmp/first_level_IPs_SIIB.txt", shell=True, stdout=subprocess.PIPE)
#time.sleep(1)

########################################################
# build list of cdp neighbors from 8th level to 9th level
iplist_ninth_level_pre = open('/usr/DCDP/tmp/9th_level_IPs-final.txt').readlines()
## remove /n from list elements
iplist_ninth_level_pre = map(lambda s: s.strip(), iplist_ninth_level_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
# Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
# Commented out line below, as not needed here. Doing it under CDP function below within the variable "cdp_fourth_level"
# list(set(iplist_fourth_level))
iplist_ninth_level = set(iplist_ninth_level_pre)


# append to new siib file (all previous levels) to accommodate current and lower levels - includes cdp neighbors and local IPs
subprocess.Popen("cat /usr/DCDP/tmp/*8th_level.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

subprocess.Popen("cat /usr/DCDP/cdp_files/cdp_eighth_level.txt >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# build list of current and all previous levels sh ip interface brief and cdp nei IPs to create new variable
all_previous_levels_local_IPs_pre = open('/usr/DCDP/tmp/all_previous_levels_siib.txt').readlines()
## remove /n from list elements
all_previous_levels_local_IPs_pre = map(lambda s: s.strip(), all_previous_levels_local_IPs_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
all_previous_levels_local_IPs = set(all_previous_levels_local_IPs_pre)
########################################################

########################################################
def ninth_level_CDP():
    # Remove lower and same level CDP Neighbors from list using set and write to next level cdp file
    # And remove duplicate cdp entries (if any exist) for running the "for loop".......
    # Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
    cdp_ninth_level = set(iplist_ninth_level) - set(all_previous_levels_local_IPs)
    cdp_ninth_level_file = open('/usr/DCDP/cdp_files/cdp_ninth_level.txt', 'w')

    for ip in cdp_ninth_level:
        cdp_ninth_level_file.write("%s\n" % ip)
        ## Must have continue here or loop ends and only the first IP is written to the file!
        continue
    # close file once loop completes
    cdp_ninth_level_file.close()

    # create variable to check if file is zero bytes or NOT....    
    check_ninth_level_cdp=os.stat("/usr/DCDP/cdp_files/cdp_ninth_level.txt").st_size == 0

    if check_ninth_level_cdp == True:
        print "   "
        print "** No more cdp neighbors..."
        print "   "
        print "** Preparing final files to use in custom discovery and/or programming"
        # cdp line below must be before seed file
        subprocess.Popen("cat /usr/DCDP/cdp_files/cdp*level.txt > /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        # Seed IP address file MUST be specified last here due to NO carriage return within file. IP or IPs must be last in the file
        # Append to create final version of ip file
        subprocess.Popen("cat /usr/DCDP/cdp_files/seed*address.txt >> /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)

        print "   "
        print "** The Network Discovery N Automation Program (NDNA) Has Finished"
        sys.exit()

    else:
        print "   "
        print "** ninth level has cdp neighbors. Standby while connecting to ninth level devices....."
        print "   "

print "   "
print "*** Wrapping Up eighth Level Devices...Preparing ninth Level Connections....."
print "______________________________________________"
print " __  __            _               _        "
print "|  \/  |          (_)             | |       "
print "| \  / | _____   ___ _ __   __ _  | |_ ___  "
print "| |\/| |/ _ \ \ / / | '_ \ / _` | | __/ _ \ "
print "| |  | | (_) \ V /| | | | | (_| | | || (_) |"
print "|_|  |_|\___/ \_/ |_|_| |_|\__, |  \__\___/ "
print "                            __/ |           "
print "                           |___/            "
print " _   _           _     _                    _" 
print "| \ | |         | |   | |                  | |"
print "|  \| | _____  _| |_  | |     _____   _____| |"
print "| . ` |/ _ \ \/ / __| | |    / _ \ \ / / _ \ |"
print "| |\  |  __/>  <| |_  | |___|  __/\ V /  __/ |"
print "|_| \_|\___/_/\_ \__| |______\___| \_/ \___|_|"
print "______________________________________________"   
# call the function
ninth_level_CDP()
########################################################

#Open SSHv2 connection to 9th level devices
def ninth_level_network_connection(ip):
    try:
        paramiko.util.log_to_file("/usr/DCDP/logs/paramiko.log")
        #Logging into device
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Passing the necessary parameters
        session.connect(ip, username = username, password = password, look_for_keys=False)
        
    #Start an interactive shell session on the router
        connection = session.invoke_shell() 
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        print ".... "
        time.sleep(8)
        connection.send("sh cdp nei detail | i IP\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief vrf all\n")
        time.sleep(8)
        connection.send("sh version\n")
        time.sleep(8)
#############################################################
        # Get around the 64K bytes (65536). paramiko limitation
        interval = 0.1
        maxseconds = 15
        maxcount = maxseconds / interval
        bufsize = 65535

        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        router_output = ''

        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode('ascii')
                router_output += data

            if connection.exit_status_ready():
                break

            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())

            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break

            rbuffer = router_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            router_output += data.decode('ascii')
#############################################################
        
        if re.search(r"% Invalid input detected at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"% Invalid command at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"Incorrect usage", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"Cisco Controller", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"User:", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"% Authorization failed", router_output):
            print "   "
            print "** Authorization failed for %s Looks Like a TACACS issue." % ip
            
        else:
            print "   "
            print "** Completed device %s" % ip

        return router_output
    
    #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        pass
        print "   "
        print "* Authentication Error for %s" % ip
        print "   "
        #print "* Closing program...\n"
    except paramiko.SSHException:
        pass
        print "   "
        print "* Incompatible SSH version. Paramiko requires compatible SSH and kex on device %s" % ip


cdp_list_ninth_level = open('/usr/DCDP/cdp_files/cdp_ninth_level.txt').readlines()
## remove /n from list elements
cdp_list_ninth_level = map(lambda s: s.strip(), cdp_list_ninth_level)

def write_files9(ip):
    sema.acquire()
    file_name = '/usr/DCDP/tmp/' + ip + '_9th_level.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    fo.write(ninth_level_network_connection(ip))
    fo.close()
    time.sleep(2)
    sema.release()
    
#Creating threads function
def create_threads9():
    threads = []
    for ip in cdp_list_ninth_level: 
        th = threading.Thread(target = write_files9, args = (ip,))   #args is a tuple with a single element     
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function which then calls the open ssh function
create_threads9()


##########################
##########################
# Build 10th level CDP IP files from 9th level device. Run egrep to grep NX-OS and IOS output, e.g. match multiple patterns
subprocess.Popen("cat /usr/DCDP/tmp/*9th_level.txt | egrep 'IP address|IPv4' | sed -e 's/IP address://' | sed -e 's/IPv4 Address://' | grep -v 0.0.0.0 > /usr/DCDP/tmp/10th_level_IPs.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# Remove empty spaces
subprocess.Popen("tr -d ' ' < /usr/DCDP/tmp/10th_level_IPs.txt > /usr/DCDP/tmp/10th_level_IPs-final.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# grab IPs to exclude from current and next level IPs, e.g. to remove first level IPs from fourth level
#subprocess.Popen("cat *seed.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' > /usr/DCDP/tmp/first_level_IPs_SIIB.txt", shell=True, stdout=subprocess.PIPE)
#time.sleep(1)

########################################################
# build list of cdp neighbors from 9th level to 10th level
iplist_tenth_level_pre = open('/usr/DCDP/tmp/10th_level_IPs-final.txt').readlines()
## remove /n from list elements
iplist_tenth_level_pre = map(lambda s: s.strip(), iplist_tenth_level_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
# Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
# Commented out line below, as not needed here. Doing it under CDP function below within the variable "cdp_fourth_level"
# list(set(iplist_fourth_level))
iplist_tenth_level = set(iplist_tenth_level_pre)


# append to new siib file (all previous levels) to accommodate current and lower levels - includes cdp neighbors and local IPs
subprocess.Popen("cat /usr/DCDP/tmp/*9th_level.txt | awk {'print $2'} | egrep '^[1-9][0-9][0-9]\\.|[1-9][0-9]\.|[1-9]\.' >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

subprocess.Popen("cat /usr/DCDP/cdp_files/cdp_ninth_level.txt >> /usr/DCDP/tmp/all_previous_levels_siib.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

# build list of current and all previous levels sh ip interface brief and cdp nei IPs to create new variable
all_previous_levels_local_IPs_pre = open('/usr/DCDP/tmp/all_previous_levels_siib.txt').readlines()
## remove /n from list elements
all_previous_levels_local_IPs_pre = map(lambda s: s.strip(), all_previous_levels_local_IPs_pre)

# remove duplicate cdp entries (if any exist) for running the "for loop".......
all_previous_levels_local_IPs = set(all_previous_levels_local_IPs_pre)
########################################################

########################################################
def tenth_level_CDP():
    # Remove lower and same level CDP Neighbors from list using set and write to next level cdp file
    # And remove duplicate cdp entries (if any exist) for running the "for loop".......
    # Might need this when fanning out from redundant cores and/or other reasons for duplicate cdp entries
    cdp_tenth_level = set(iplist_tenth_level) - set(all_previous_levels_local_IPs)
    cdp_tenth_level_file = open('/usr/DCDP/cdp_files/cdp_tenth_level.txt', 'w')

    for ip in cdp_tenth_level:
        cdp_tenth_level_file.write("%s\n" % ip)
        ## Must have continue here or loop ends and only the first IP is written to the file!
        continue
    # close file once loop completes
    cdp_tenth_level_file.close()

    # create variable to check if file is zero bytes or NOT....    
    check_tenth_level_cdp=os.stat("/usr/DCDP/cdp_files/cdp_tenth_level.txt").st_size == 0

    if check_tenth_level_cdp == True:
        print "   "
        print "** No more cdp neighbors..."
        print "   "
        print "** Preparing final files to use in custom discovery and/or programming"
        # cdp line below must be before seed file
        subprocess.Popen("cat /usr/DCDP/cdp_files/cdp*level.txt > /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        # Seed IP address file MUST be specified last here due to NO carriage return within file. IP or IPs must be last in the file
        # Append to create final version of ip file
        subprocess.Popen("cat /usr/DCDP/cdp_files/seed*address.txt >> /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
        time.sleep(1)

        print "   "
        print "** The Network Discovery N Automation Program (NDNA) Has Finished"
        sys.exit()

    else:
        print "   "
        print "** tenth level has cdp neighbors. Standby while connecting to tenth level devices....."
        print "   "

print "   "
print "*** Wrapping Up ninth Level Devices...Preparing tenth Level Connections....."
print "______________________________________________"
print " __  __            _               _        "
print "|  \/  |          (_)             | |       "
print "| \  / | _____   ___ _ __   __ _  | |_ ___  "
print "| |\/| |/ _ \ \ / / | '_ \ / _` | | __/ _ \ "
print "| |  | | (_) \ V /| | | | | (_| | | || (_) |"
print "|_|  |_|\___/ \_/ |_|_| |_|\__, |  \__\___/ "
print "                            __/ |           "
print "                           |___/            "
print " _   _           _     _                    _" 
print "| \ | |         | |   | |                  | |"
print "|  \| | _____  _| |_  | |     _____   _____| |"
print "| . ` |/ _ \ \/ / __| | |    / _ \ \ / / _ \ |"
print "| |\  |  __/>  <| |_  | |___|  __/\ V /  __/ |"
print "|_| \_|\___/_/\_ \__| |______\___| \_/ \___|_|"
print "______________________________________________"   
# call the function
tenth_level_CDP()
########################################################

#Open SSHv2 connection to 8th level devices
def tenth_level_network_connection(ip):
    try:
        paramiko.util.log_to_file("/usr/DCDP/logs/paramiko.log")
        #Logging into device
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Passing the necessary parameters
        session.connect(ip, username = username, password = password, look_for_keys=False)
        
    #Start an interactive shell session on the router
        connection = session.invoke_shell() 
        
        #Setting terminal length for entire output - no pagination
        connection.send("terminal length 0\n")
        print ".... "
        time.sleep(8)
        connection.send("sh cdp nei detail | i IP\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief\n")
        print ".... "
        time.sleep(8)
        connection.send("sh ip inter brief vrf all\n")
        time.sleep(8)
        connection.send("sh version\n")
        time.sleep(8)

#############################################################
        # Get around the 64K bytes (65536). paramiko limitation
        interval = 0.1
        maxseconds = 15
        maxcount = maxseconds / interval
        bufsize = 65535

        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        router_output = ''

        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode('ascii')
                router_output += data

            if connection.exit_status_ready():
                break

            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())

            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break

            rbuffer = router_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            router_output += data.decode('ascii')
#############################################################
        
        if re.search(r"% Invalid input detected at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"% Invalid command at", router_output):
            print "   "
            print "** Completed device %s" % ip
        elif re.search(r"Incorrect usage", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"Cisco Controller", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"User:", router_output):
            print "   "
            print "** Completed WLC device %s" % ip
        elif re.search(r"% Authorization failed", router_output):
            print "   "
            print "** Authorization failed for %s Looks Like a TACACS issue." % ip
            
        else:
            print "   "
            print "** Completed device %s" % ip

        return router_output
    
    #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        pass
        print "   "
        print "* Authentication Error for %s" % ip
        print "   "
        #print "* Closing program...\n"
    except paramiko.SSHException:
        pass
        print "   "
        print "* Incompatible SSH version. Paramiko requires compatible SSH and kex on device %s" % ip


cdp_list_tenth_level = open('/usr/DCDP/cdp_files/cdp_tenth_level.txt').readlines()
## remove /n from list elements
cdp_list_tenth_level = map(lambda s: s.strip(), cdp_list_tenth_level)

def write_files10(ip):
    sema.acquire()
    file_name = '/usr/DCDP/tmp/' + ip + '_10th_level.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    fo.write(tenth_level_network_connection(ip))
    fo.close()
    time.sleep(2)
    sema.release()

#Creating threads function
def create_threads10():
    threads = []
    for ip in cdp_list_tenth_level: 
        th = threading.Thread(target = write_files10, args = (ip,))   #args is a tuple with a single element     
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function which then calls the open ssh function
create_threads10()

####################################################
print "   "
print "You've reached the end of this program's level of CDP neighbors (x10)." 
print "   "
print "Do a sanity check to make sure there are no higher levels of Cisco network devices available"
print "   "
print "Preparing final files to use in custom discovery and/or programming"
print "   "

# cdp line below must be before seed file
subprocess.Popen("cat /usr/DCDP/cdp_files/cdp*level.txt > /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)
# Seed IP address file MUST be specified last here due to NO carriage return within file. IP or IPs must be last in the file
# Append to create final version of ip file
subprocess.Popen("cat /usr/DCDP/cdp_files/seed*address.txt >> /usr/DCDP/Full-IP-List/DCDP-ip-file.txt", shell=True, stdout=subprocess.PIPE)
time.sleep(1)

print "The Network Discovery N Automation Program (NDNA) Has Finished"
##########################

#End of program
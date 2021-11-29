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



import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
import paramiko
import time
import re
import sys
import threading
import datetime
import getpass
import os.path
import subprocess
import base64

print "###############################################################################################" 
print "   ______           __                       ____        __  __           "   
print "  / ____/_  _______/ /_____  ____ ___       / __ \__  __/ /_/ /_  ____  ____ "
print " / /   / / / / ___/ __/ __ \/ __ `__ \     / /_/ / / / / __/ __ \/ __ \/ __ \ " 
print "/ /___/ /_/ (__  ) /_/ /_/ / / / / / /    / ____/ /_/ / /_/ / / / /_/ / / / /  "
print "\____/\__,_/____/\__/\____/_/ /_/ /_/____/_/    \__, /\__/_/ /_/\____/_/ /_/ "
print "                                   /_____/     /____/                        "
print "                     _____           _       __ "
print "                    / ___/__________(_)___  / /_"
print "                    \__ \/ ___/ ___/ / __ \/ __/"
print "                   ___/ / /__/ /  / / /_/ / /_  "
print "             _____/____/\___/_/  /_/ .___/\__/  "
print "            /_____/   "
print "            "
print "                         For NXOS_Routers"
print ""  
print "###############################################################################################" 
print "                        Enter The DataCenter Information Below:" 
print ""  
print "           This DataCenter Must Exist From Previously Running The NDNA Program" 
print ""  
print "   This Will Write Your Custom Configs to /usr/DataCenters/<your DC directory>/DCDP/configs"
print "###############################################################################################" 
print "" 
DataCenter = raw_input( "Enter Data_Center String Here e.g. New-York-DC: " )

if os.path.exists('/usr/DataCenters/%s' % DataCenter) == True:                     
    print "Data_Center Exists..."
else:
    print "Data_Center does not exist...Program exiting. Goodbye..."
    sys.exit()

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("/usr/DCDP/logs/custom_nxos_routers_python_script.log", "w")

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

sys.stderr = open("/usr/DCDP/logs/custom_nxos_routers_python_script_err.log", "w")

current_time=time.strftime("%Y-%m-%d %H:%M")

username = raw_input( "Enter username: " )
print "   "
print "#### Password will be hidden"
print "#### Please copy and input your password from an unsaved text file, e.g. not written to disk, a or secure database like KeepPass"
print "   "
password = getpass.getpass()
print "   "

def cmd_is_valid():
    global cmd_file
    
    while True:
        cmd_file = "ssh_custom_NXOS_Routers_commands.txt"
        
        #Changing output messages
        if os.path.isfile(cmd_file) == True:
            print "\n* Attempting to connect to device(s)...\n"
            print "\n* Output files will be written to /usr/DataCenters/%s/DCDP/configs for all device(s)...\n" % DataCenter
            print "\n* Log files (stdout and stderr) will be written to /usr/DCDP/logs for all device(s)...\n"
            break
        
        else:
            print "\n* File %s does not exist! Please check and try again!\n" % cmd_file
            continue

try:
    #Calling command file validity function
    cmd_is_valid()
    
except KeyboardInterrupt:
    print "\n\n* Program aborted by user. Exiting...\n"
    sys.exit()

#setup max number of threads for Semaphore method to use. create sema variable for open ssh function to use
maxthreads = 10
sema = threading.BoundedSemaphore(value=maxthreads)

#Open SSHv2 connection to devices
def open_network_connection(ip):

    try:
        paramiko.util.log_to_file("/usr/DCDP/logs/paramiko.log")   
        #Define SSH parameters
        #Logging into device
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        session.connect(ip, username = username, password = password, look_for_keys=False)

        connection = session.invoke_shell()	
        #Open user selected file for reading

        selected_cmd_file = open(cmd_file, 'r')
        #Starting from the beginning of the file

        selected_cmd_file.seek(0)

        #Writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(8)
        
        #Closing the command file
        selected_cmd_file.close()

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

        if re.search(r"% Invalid command at", router_output):
            print "** There was at least one NX-OS syntax error on %s" % ip
        elif re.search(r"% Authorization failed", router_output):
            print "   "
            print "** Authorization failed for %s Looks Like a TACACS issue." % ip
            print "** Try and run the program again."
        else:
            print "\nCompleted device %s" % ip

        return router_output
        session.close()

    except paramiko.AuthenticationException:
        pass
        print "   "
        print "* Authentication Error for %s You might have entered your password incorrectly You might have entered your password incorrectly" % ip
        print "   "
        #print "* Closing program...\n"
    except paramiko.SSHException:
        pass
        print "   "
        print "* Incompatible SSH version. Paramiko requires compatible SSH and kex on device %s" % ip

iplist = open('/usr/DataCenters/%s/DCDP/good-IPs/L3-NX-OS-IPs.txt' % DataCenter).readlines()
# remove return from file names, e.g. remove \n from list
iplist = map(lambda s: s.strip(), iplist)

def write_files(ip):
    sema.acquire()
    file_name = '/usr/DataCenters/%s/DCDP/configs/' % DataCenter + ip + '_' + current_time + '_nxos_L3_custom.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    router_output = open_network_connection(ip)
    fo.write(router_output)
    fo.close()
    time.sleep(2)
    sema.release()

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
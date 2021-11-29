#!/usr/bin/env python

import MySQLdb as mdb


import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
import paramiko
import threading
import datetime
import os.path
import subprocess
import time
import sys
import re    
import base64
import getpass

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
print "                    For IOS Inventory to MySQL DB:    "
print ""   
print "###############################################################################################" 
print "                        Enter The DataCenter Information Below:" 
print ""  
print "           This DataCenter Must Exist From Previously Running The NDNA Program" 
print ""   
print "           The Name Must Match The Name Of The Directory That Already Exists!"
print "###############################################################################################" 
print ""
DataCenter = raw_input( "Enter Data_Center String Here e.g. New-York-DC: " )

if os.path.exists('/usr/DataCenters/%s' % DataCenter) == True:                     
    print "Data_Center Exists..."
else:
    print "Data_Center does not exist...Program exiting. Goodbye..."
    sys.exit()


print ""
username = raw_input( "Enter username: " )
print "   "
print "#### Password will be hidden"
print "#### Please copy and input your password from an unsaved text file, e.g. not written to disk, a or secure database like KeepPass"
print "   "
password = getpass.getpass()
print "   "

#Module for output coloring
from colorama import init, deinit, Fore, Style


# Start to write standard errors to log file
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("/usr/DCDP/logs/IOS_INVENTORY.log", "w")

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

sys.stderr = open("/usr/DCDP/logs/IOS_INVENTORY-ERR.log", 'w')

#Initialize colorama
init()

#Checking number of arguments passed into the script
if len(sys.argv) == 2:
    #ip_file = sys.argv[1]
    sql_file = sys.argv[1]
	
    print Fore.BLUE + Style.BRIGHT + "\n\n* Excecuting IOS Device Inventory Program For Export (xml, json, yaml, etc)\n"

else:
    print Fore.RED + Style.BRIGHT + "\nIncorrect number of arguments (files) passed into the script."
    print Fore.RED + "Please try again.\n"
    sys.exit()


#Checking SQL connection command file validity
def sql_is_valid():
    global sql_file
	
    while True:
        #Changing output messages
        if os.path.isfile(sql_file) == True:
            print "\n* Connection to MySQL has been validated...\n"
            print "\n* Database Errors will be logged to: " + Fore.YELLOW + "SQL_Error_Log.txt\n" + Fore.BLUE
            break
			
        else:
            print Fore.RED + "\n* File %s does not exist! Please check and try again!\n" % sql_file
            sys.exit()
 
try:
    #Calling MySQL file validity function
    sql_is_valid()
    
except KeyboardInterrupt:
    print Fore.RED + "\n\n* Program aborted by user. Exiting...\n"
    sys.exit()
    
    ############# Application #4 - Part #2 #############
	
check_sql = True

def sql_connection(command, values):
    global check_sql
    
    #Define SQL connection parameters
    selected_sql_file = open(sql_file, 'r')
    
    #Starting from the beginning of the file
    selected_sql_file.seek(0)

    sql_host = selected_sql_file.readlines()[0].split(',')[0]
    
    #Starting from the beginning of the file
    selected_sql_file.seek(0)
    
    sql_username = selected_sql_file.readlines()[0].split(',')[1]
    
    #Starting from the beginning of the file
    selected_sql_file.seek(0)
    
    sql_password = selected_sql_file.readlines()[0].split(',')[2]
    
    #Starting from the beginning of the file
    selected_sql_file.seek(0)
    
    sql_database = selected_sql_file.readlines()[0].split(',')[3].rstrip("\n")
    
    #Connecting and writing to database
    try:
        sql_conn = mdb.connect(sql_host, sql_username, sql_password, sql_database)
    
        cursor = sql_conn.cursor()
    
        cursor.execute("USE IOS_INVENTORY")
        
        cursor.execute(command, values)
        
        #Commit changes
        sql_conn.commit()
        
    except mdb.Error, e:
        sql_log_file = open("SQL_Error_Log.txt", "a")
        
        #Print any SQL errors to the error log file
        print >>sql_log_file, str(datetime.datetime.now()) + ": Error %d: %s" % (e.args[0],e.args[1])
        
        #Closing sql log file:    
        sql_log_file.close()
        
        #Setting check_sql flag to False if any sql error occurs
        check_sql = False
                
    #Closing the sql file
    selected_sql_file.close()



#######################################################
def sql_connection_full(command, values):
    
    #Define SQL connection parameters
    sql_host = 'localhost'
    sql_username = 'root'
    sql_password = 'neural123'    
    sql_database = 'djangodb'
    
    #Connecting and writing to database
    try:
        sql_conn = mdb.connect(sql_host, sql_username, sql_password, sql_database)
    
        cursor = sql_conn.cursor()
    
        cursor.execute("USE djangodb")
        
        cursor.execute(command, values)
        
        #Commit changes
        sql_conn.commit()
        
    except mdb.Error, e:
        sql_log_file = open("SQL_Error_Log2.txt", "a")
        
        #Print any SQL errors to the error log file
        print >>sql_log_file, str(datetime.datetime.now()) + ": Error %d: %s" % (e.args[0],e.args[1])
        
        #Closing sql log file:    
        sql_log_file.close()
#######################################################

#setup max number of threads for Semaphore method to use. create sema variable for open ssh function to use
maxthreads = 10
sema = threading.BoundedSemaphore(value=maxthreads)

#Open SSHv2 connection to devices
def open_network_connection(ip):
    global check_sql
    
    #Change exception message
    try:
        sema.acquire()
        paramiko.util.log_to_file("/usr/DCDP/logs/paramiko.log")   
        #Define SSH parameters
        #Logging into device
        session = paramiko.SSHClient()
        
        #For testing purposes, this allows auto-accepting unknown host keys
        #Do not use in production! The default would be RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #Connect to the device using username and password          
        session.connect(ip, username = username, password = password, look_for_keys=False)
        
        #Start an interactive shell session on the router
        connection = session.invoke_shell()	
        
        #Setting terminal length for entire output - disable pagination
        connection.send("terminal length 0\n")
        time.sleep(7)

        #Time length to deal with 37xx and 38xx switch stack bugs
        connection.send("show run | in hostname\n")
        time.sleep(32)
                
        #Reading commands from within the script
        #Using the "\" line continuation character for better readability of the commands to be sent
        selected_cisco_commands = '''show version | include , Version|uptime is|bytes of memory|Hz&\
                                  show inventory&\
                                  dir&\
                                  show ip int brief | include Eth|Fast|Giga|Te|Vlan&'''
                                  
        #Splitting commands by the "&" character
        command_list = selected_cisco_commands.split("&")
        
        #Writing each line in the command string to the device
        for each_line in command_list:
            connection.send(each_line + '\n')
            time.sleep(10)
        

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
        output = ''

        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode('ascii')
                output += data

            if connection.exit_status_ready():
                break

            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())

            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break

            rbuffer = output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            output += data.decode('ascii')
#############################################################
        
        if re.search(r"% Invalid input detected at", output):
            print Fore.RED + "* Inventory Information extracted from %s" % ip
        elif re.search(r"% Authorization failed", output):
            print "   "
            print "** Authorization failed for %s" % ip
            print "** Try and run the program again."
        else:
            print Fore.RED + "* Inventory Information extracted from %s" % ip
                        
        dev_os = re.search(r"\), Version (.+)", output)
        os = dev_os.group(1)

        #dev_vendor = re.search(r"(.+?) (.+) (.+) (.+) bytes of memory", output)
        #platform = dev_vendor.group(2)

        dev_image_name = re.search(r" \((.+)\), Version", output)
        image_name = dev_image_name.group(1)

        local_hostname = re.search(r"hostname (.+)", output)
        hostname = local_hostname.group(1)

        serial_no_group = re.search(r"SN: (.+)", output)
        serial_no = serial_no_group.group(1)
        
        dev_flash = re.search(r"(.+ bytes total)", output)
        flash = dev_flash.group(1)

        Local_IPs = re.findall(r"Ethernet[0-9].+ ([1-9].+[0-9])", output)
        Local_IPs_var = ' | '.join(Local_IPs)

        Local_SVI_IPs = re.findall(r"Vlan[0-9].+ ([1-9].+[0-9])", output)
        Local_SVI_IPs_var = ' | '.join(Local_SVI_IPs)

        #Insert/Update if exists all network devices data into the MySQL database table Cisco_IOS_Inventory. Calling sql_connection function                 
        sql_connection("REPLACE INTO Cisco_IOS_Inventory(Hostname,Local_IPs,Local_SVI_IPs,IOS_Image,IOSVersion,Flash,SerialNo) VALUES(%s, %s, %s, %s, %s, %s, %s)", (hostname, Local_IPs_var, Local_SVI_IPs_var, image_name, os, flash, serial_no))


#######################################################
        #NON-TRUCATED DB - first create if doesn't exist
        sql_connection_full("REPLACE INTO neural_ndnaiosdevice (Hostname,Local_IPs,Local_SVI_IPs,IOS_Image,IOSVersion,Flash,SerialNo) VALUES(%s, %s, %s, %s, %s, %s, %s)", (hostname, Local_IPs_var, Local_SVI_IPs_var, image_name, os, flash, serial_no)) 
#######################################################


        #Closing the SSH connection
        session.close()
        time.sleep(2)
        sema.release()
     
    except paramiko.AuthenticationException:
        pass
        print "   "
        print "* Authentication Error for %s You might have entered your password incorrectly You might have entered your password incorrectly" % ip
        print "   "

    except AttributeError:
        pass
        print Fore.RED + "* Could not pull in information from device %s* This is probably an IOS device that is not yet supported for Certain Database Information import" % ip
        print Fore.RED + "* See Release notes, and if needed, please manually add any missing info to Diagram/s like serial no. code version, etc.\n"


ip_list = open('/usr/DataCenters/%s/DCDP/good-IPs/IOS-IPs.txt' % DataCenter).readlines()

print "\n* Attempting to Connect to the IOS-IPs IN /usr/DataCenters/%s/DCDP/good-IPs ...\n" % DataCenter

#Creating threads
def create_threads():
    threads = []
    for ip in ip_list:
        th = threading.Thread(target = open_network_connection, args = (ip,))   #args is a tuple with a single element
        th.start()
        time.sleep(0.2)
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function
create_threads()

if check_sql == True:
    print "\n* Successfully Built IOS Database Inventory, excluding Devices that reported issues (If any).\n* See /usr/DCDP/logs/IOS_INVENTORY.log for Log File"
    print "* If there were any problem devices, please investigate manually before attempting to run the program again, e.g make sure the device is accessible!"

else:
    print Fore.RED + "\n* There was a problem exporting all the data to the Database.\n* Check the files, database and SQL_Error_Log.txt.\n"

#De-initialize colorama
deinit()

#End of program
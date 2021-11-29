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

import MySQLdb as mdb
import os.path
import subprocess
import time
import sys
import datetime
#Module for output coloring
from colorama import init, deinit, Fore, Style

#Initialize colorama
init()

#Checking number of arguments passed into the script
if len(sys.argv) == 2:
    sql_file = sys.argv[1]
    #print Fore.BLUE + Style.BRIGHT + "\n\n* The script will be executed..."
else:
    print Fore.RED + Style.BRIGHT + "\nIncorrect number of arguments (files) passed into the script."
    print Fore.RED + "Please try again.\n"
    sys.exit()

def sql_is_valid():
    global sql_file
	
    while True:
        #Changing output messages
        if os.path.isfile(sql_file) == True:
            print "\n* Truncating IOS DB Table..."
            break
        else:
            print Fore.RED + "\n* File %s does not exist! Please check and try again!\n" % sql_file
            sys.exit()
#Change exception message
try:
    #Calling MySQL file validity function
    sql_is_valid()
    
except KeyboardInterrupt:
    print Fore.RED + "\n\n* Program aborted by user. Exiting...\n"
    sys.exit()
    
    ############# Application #4 - Part #2 #############
	
check_sql = True
def sql_connection(command):
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
        
        cursor.execute(command)
        
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


def TRUNCATE_DB():
    global check_sql
    
    #Change exception message
    try:               
        sql_connection("TRUNCATE TABLE Cisco_IOS_Inventory;")

    except mdb.Error, e:
        print "script failed. please see error log"

TRUNCATE_DB()

#De-initialize colorama
deinit()

#End of program
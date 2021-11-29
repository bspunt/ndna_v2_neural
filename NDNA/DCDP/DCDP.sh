#!/bin/sh
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


echo ""
echo "------------------------------------------------------------------"
echo "    NDNA: The Network Discovery N Automation Program"
echo "    Copyright (C) 2017  Brett M Spunt, CCIE No. 12745 (US Copyright No. Txu002053026)"
echo ""
echo "    NDNA is free software: you can redistribute it and/or modify"
echo "    it under the terms of the GNU General Public License as published by"
echo "    the Free Software Foundation, either version 3 of the License, or"
echo "    (at your option) any later version."
echo ""
echo "    NDNA is distributed in the hope that it will be useful,"
echo "    but WITHOUT ANY WARRANTY; without even the implied warranty of"
echo "    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
echo "    GNU General Public License for more details."
echo ""
echo "    This program comes with ABSOLUTELY NO WARRANTY."
echo "    This is free software, and you are welcome to redistribute it"
echo ""
echo "    You should have received a copy of the GNU General Public License"
echo "    along with NDNA.  If not, see <https://www.gnu.org/licenses/>."
echo "------------------------------------------------------------------"
echo ""
echo "          The program will continue in 2 seconds"
sleep 2

#find /usr/DCDP/ -type d -exec chmod 755 -R {} \;
#find /usr/enterprise-wide-routers/ -type d -exec chmod 755 -R {} \;
#find /usr/enterprise-wide-switches/ -type d -exec chmod 755 -R {} \;
#find /usr/Restore/ -type d -exec chmod 755 -R {} \;


if (dialog --title "Welcome to the NDNA Program" --yesno "         Choose Yes to Begin, or No to Exit." 10 60) then
    echo "Running the program..."
else
    exit 1
fi

echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
echo "  ------------------------------------------------------------------------------------------------------------------"
cd /usr/DCDP
echo "  ------------------------------------------------------------------------------------------------------------------"
echo ""
echo "                     Enter The Company Code, and Name of Your Site/DataCenter"
echo ""
echo "  ------------------------------------------------------------------------------------------------------------------"
echo ""
echo "  ------------------------------------------------------------------------------------------------------------------"
echo ""
echo "This MUST BE in the following format: <3 character company code>:<Data-Center Name> This must be alpha, NOT numeric"
echo ""
echo "  ------------------------------------------------------------------------------------------------------------------"
echo ""
echo "   It can be lower or upper case A-Z, then a colon, then the Data-Center/Site name (DC name can be any length)"
echo ""
echo "                  e.g. <3 character company code>:<dc/site name> - Example: MIC:LA-DC"
echo ""
echo "  ------------------------------------------------------------------------------------------------------------------"
echo ""
echo "This requirement will allow you complete flexibility in building IP Lists enterprise wide *per-company* and/or *per-region* of a Company"
echo ""
echo "        The Naming convention can also be broken down by region, e.g. if you want to segment DCs/Sites by Region"
echo ""
echo "  ------------------------------------------------------------------------------------------------------------------"
echo ""
echo "   Example:: Using North America/South America, EMEA, and APAC, you could group all DCs that way, using N, E, A followed"
echo "   By a two character company naming convention, e.g. NAX:DC1, EAX:DC1, AAX:DC1 - This is one naming convention example:"
echo "   North America, EMEA and APAC with a two character company code (AX). This would allow you to build IP Lists *per-region*"
echo ""
echo "  ------------------------------------------------------------------------------------------------------------------"
echo ""
echo "A folder structure will be created. The Name Must Not Contain Any Spaces, e.g. use ACC:New-York-DC, Not ACC:New York DC"
echo ""
echo "                                 Names are case sensitive"
echo ""
echo "  This will backup everything at the end of the program to /usr/DataCenters/<your DC directory>"
echo ""
echo "   Document the name of your DC Folders. You will need to reference these as you use the program!!"
echo ""
echo "  ------------------------------------------------------------------------------------------------------------------"
echo ""
echo "                ALL YOUR CUSTOM DISCOVERY AND PROGRAMMING FILES WILL ALSO BE STORED IN YOUR DC FOLDERS"
echo ""
echo "You still need to run any subsequent custom discovery or programming from the /usr/DCDP/* Directories (This is where you run the program)"
echo ""
echo "  ------------------------------------------------------------------------------------------------------------------"
echo ""
read -p "Enter The Company Code/Data_Center String NOW e.g. MIC:LA-DC: " DataCenter
echo ""

if echo $DataCenter | grep -q "^[a-zA-Z][a-zA-Z][a-zA-Z]:"; 
then
  echo "Data-Center Name Meets Requirements... Continuing"
  echo ""
else
    echo "Data-Center Name Doesnt Meet Requirements... Please try again..."
    echo ""
    read -p "Enter Data_Center String Here e.g. MIC:LA-DC: " DataCenter
    echo ""
    if echo $DataCenter | grep -q "^[a-zA-Z][a-zA-Z][a-zA-Z]:"; 
    then 
      echo "Data-Center Name Meets Requirements... Thank you...Continuing"
  else
    echo "Incorrect Naming Scheme Input Again! Program Exiting...You'll have to run the program again...Sorry Charlie..."
    exit 1
  fi
fi


date=$(date +"%b-%d-%y")

##############################
if ls /usr/DCDP/bin/diagram-generation/*.xml 1> /dev/null 2>&1
then
    # if xml file exists remove it for re-population
    rm /usr/DCDP/bin/diagram-generation/*diagram-generation.xml
else
    echo ""
fi
##############################

BACKUPDIR=/usr/Backups
 
if [ -d "$BACKUPDIR" ];
then
   echo ""
else
   echo "** Creating Backups Directory /usr/Backups...."
   echo ""
   mkdir /usr/Backups
fi

echo ""
echo ""

DIR=/usr/DataCenters/$DataCenter
 
if [ -d "$DIR" ];
then
   echo "** DataCenter Directories for $DIR exist....."
   echo ""


else
   echo "** This is a new Data Center....Creating $DataCenter directories...."
   echo ""
   ## Create datacenter folder
   mkdir /usr/DataCenters/$DataCenter
fi

##############################
if ls /usr/DataCenters/$DataCenter/DCDP/configs/*.txt 1> /dev/null 2>&1
then
    # backup datacenter's custom config folder
    zip -r -q $DataCenter-custom-configs-dir-$date.zip /usr/DataCenters/$DataCenter/DCDP/configs/*.txt
    mv *.zip /usr/Backups/
else
    echo ""
fi
##############################

##############################
if [ -s /usr/DataCenters/$DataCenter/* ]
then
    ## Remove everything below datacenter folder to clear it for re-population
    rm -r /usr/DataCenters/$DataCenter/*
else
    echo ""
fi
##############################

python /usr/DCDP/Program-Files/DCDP-v17-0-2.py
sleep 3



##############################
if [ -s /usr/DCDP/tmp/*seed.txt ]
then
    echo ""

else
    echo "  ---------------------------------------------------------"
    echo "***"
    echo "***         There was a problem with the Seed Device."
    echo "***  Check IP Connectivity and the SSH credentials to the seed... "
    echo "***               Nothing to do...exiting......"
    echo "***                      GOODBYE"
    echo "***"
    echo "  ---------------------------------------------------------"
    exit 1

fi
##############################

##############################
#DO DATACENTER SPECIFIC BACKUP TO MAIN BACKUPS FOLDER
#THIS WILL KEEP AN HISTORICAL BACKUP
cd /usr/DCDP/tmp
# will cover any IP range, public or private
zip -q DCDP-configs.zip *level.txt
zip -q DCDP-configs.zip *seed.txt
unzip -q DCDP-configs.zip -d /usr/DCDP/configs/sh-ip-inter-brief-sh-ver/
rm *level.txt
rm *seed.txt
rm DCDP-configs.zip

##############################
#chmod 755 /usr/DCDP/Program-Files/*.sh
cd /usr/DCDP/Program-Files/


dialog --infobox "Discovery Completed....\n\nMoving onto Post Discovery Tasks...." 15 80 ; sleep 4


echo ""
dialog --infobox "Running Post-Program Scripts for $DataCenter. Standby...." 15 80 ; sleep 4
dialog --infobox "Building IOS-NX-OS-CSV Files for $DataCenter. Standby..." 15 80 ; sleep 4

./Build-IOS-NX-OS-CSV-Files-to-identify-duplicates.sh
echo ""
dialog --infobox "Building Good IP Lists Standby..." 15 80 ; sleep 4
echo ""
./Good-IPs.sh
./IOS-IPs.sh
./NX-OS-IPs.sh

dialog --infobox "Building Bad IP List  " 15 80 ; sleep 4
echo ""
python Bad-IPLIST.py
##############################
if [ -s /usr/DCDP/good-IPs/NX-OS-IPs.txt ]
then
    dialog --infobox "Building NXOS L2-L3 IP lists " 15 80 ; sleep 4
    python /usr/DCDP/Program-Files/L2-L3-NXOS.py
    sleep 3
    
    
    # Find auth errors using GRASP (If they exist)
    cat /usr/DCDP/logs/L2-L3-NXOS.log | grep "Authentication Error" | awk {'print $5'} > /usr/DCDP/tmp/L2-L3-NXOS_auth_error_iplist.txt
    if [ -s /usr/DCDP/tmp/L2-L3-NXOS_auth_error_iplist.txt ]
    then
      # call python script
      # try auth errors IPs again - WILL BE SAME AS SCRIPT ABOVE BUT JUST REFERENCES NEW IP LIST
      echo "  ---------------------------------------------------------"
      echo "** Trying IPs with Authentication errors one more time...."
      echo "  ---------------------------------------------------------"
      python /usr/DCDP/Program-Files/L2-L3-NXOS_auth_errors.py
      # remove IP file from tmp dir. CLEANUP!
      rm /usr/DCDP/tmp/L2-L3-NXOS_auth_error_iplist.txt
    fi

    # Change into configs directory of main program. Grep for devices running a routing protocol
    # NOTICE THE SPACE AFTER ROUTER. THIS IS NEEDED
    # grep -v removes the command sh run which includes router, although not really needed due to matching on regex, start of line for router
    cd /usr/DCDP/configs/

    #OLD WAY BELOW - WOULDNT WORK WITH SINGLE NXOS DEVICE
    #ls | grep -v "sh run" | grep ^"router " *NXOS_.txt > NXOS-L3-TEMP.txt 
    #NEW WAY BELOW - WORKS WITH SINGLE NXOS DEVICE
    ls | grep -v "sh run" | grep -H ^"router " *NXOS_.txt > NXOS-L3-TEMP.txt 
    #ls *NXOS_.txt | grep -v "sh run" | grep -r --exclude=NXOS-L3-TEMP.txt ^"router " > NXOS-L3-TEMP.txt
    
    cat NXOS-L3-TEMP.txt | sed -e 's/_NXOS_.txt:.*//' > /usr/DCDP/good-IPs/L3-NX-OS-IPs-pre.txt
    ## THIS WILL REMOVE ALL DUPLICATES IPs
    cat /usr/DCDP/good-IPs/L3-NX-OS-IPs-pre.txt | awk '!seen[$0]++' > /usr/DCDP/good-IPs/L3-NX-OS-IPs.txt
    # REMOVE TEMP FILES USED TO BUILD L3-NX-OS-IPs.txt FILE
    rm /usr/DCDP/good-IPs/L3-NX-OS-IPs-pre.txt
    rm /usr/DCDP/configs/*NXOS*.txt
    # Build L2 IP list file
    python /usr/DCDP/Program-Files/NXOS-L2-IPLIST.py
    dialog --infobox "Completed Building NXOS L2-L3 IP lists" 15 80 ; sleep 4
else
    echo ""
    dialog --infobox "No NXOS Devices. Skipping L2-L3 IP lists for NXOS devices..." 15 80 ; sleep 4
fi
##############################
echo ""
##############################
if [ -s /usr/DCDP/good-IPs/IOS-IPs.txt ]
then
    dialog --infobox "Building IOS L2-L3 IP lists" 15 80 ; sleep 4
    echo "  ---------------------------------------------------------"
    echo "     Note: The L2-L3 IOS scripts will take a few minutes"
    echo " Due to a 32 second delay between commands. This is on purpose"
    echo "        To avoid issues with 3750/3850 switches  "
    echo "           When issuing show run Commands"
    echo "  ---------------------------------------------------------"
    python /usr/DCDP/Program-Files/L2-L3-IOS.py
    sleep 3
    
    
    # Find auth errors using GRASP (If they exist)
    cat /usr/DCDP/logs/L2-L3-IOS.log | grep "Authentication Error" | awk {'print $5'} > /usr/DCDP/tmp/L2-L3-IOS_auth_error_iplist.txt
    if [ -s /usr/DCDP/tmp/L2-L3-IOS_auth_error_iplist.txt ]
    then
      # call python script
      # try auth errors IPs again - WILL BE SAME AS SCRIPT ABOVE BUT JUST REFERENCES NEW IP LIST
      echo ""
      dialog --infobox "Trying IPs with Authentication errors one more time...." 15 80 ; sleep 4
      python /usr/DCDP/Program-Files/L2-L3-IOS_auth_errors.py
      # remove IP file from tmp dir. CLEANUP!
      rm /usr/DCDP/tmp/L2-L3-IOS_auth_error_iplist.txt
    fi
    # Change into configs directory of main program. Grep for devices running a routing protocol
    # NOTICE THE SPACE AFTER ROUTER. THIS IS NEEDED
    # grep -v removes the command sh run which includes router, although not really needed due to matching on regex, start of line for router
    cd /usr/DCDP/configs/

    #OLD WAY BELOW - WOULDNT WORK WITH SINGLE NXOS DEVICE
    #ls | grep -v "sh run" | grep ^"router " *IOS_.txt > IOS-L3-TEMP.txt 
    #NEW WAY BELOW - WORKS WITH SINGLE IOS DEVICE
    ls | grep -v "sh run" | grep -H ^"router " *IOS_.txt > IOS-L3-TEMP.txt 
    #fix is grep -r --exclude=<filename.txt> <pattern>
    #ls *IOS_.txt | grep -v "sh run" | grep -r --exclude=IOS-L3-TEMP.txt ^"router " > IOS-L3-TEMP.txt

    cat IOS-L3-TEMP.txt | sed -e 's/_IOS_.txt:.*//' > /usr/DCDP/good-IPs/L3-IOS-IPs-pre.txt
    ## THIS WILL REMOVE ALL DUPLICATES IPs
    cat /usr/DCDP/good-IPs/L3-IOS-IPs-pre.txt | awk '!seen[$0]++' > /usr/DCDP/good-IPs/L3-IOS-IPs.txt
    # REMOVE TEMP FILES USED TO BUILD L3-IOS-IPs.txt FILE
    rm /usr/DCDP/good-IPs/L3-IOS-IPs-pre.txt
    rm /usr/DCDP/configs/*IOS*.txt
    # Build L2 IP list file
    python /usr/DCDP/Program-Files/IOS-L2-IPLIST.py
    echo ""
    dialog --infobox "Completed Building IOS L2-L3 IP lists" 15 80 ; sleep 4
else
    echo ""
    dialog --infobox "No IOS Devices. Skipping L2-L3 IP lists for IOS devices..." 15 80 ; sleep 4
fi
##############################
# CHANGE INTO THE GOOD-IPs dir
cd /usr/DCDP/good-IPs/

#########################
if [ -s /usr/DCDP/good-IPs/IOS-IPs.txt ]
then
      dialog --infobox "Building cdp-neighbors-IOS File. Standby...." 15 80 ; sleep 4
      echo ""
      cd /usr/DCDP/cdp-neighbors
      ./IOS-CDP-Neighbors.sh
      sleep 3
      
else
      echo ""
      dialog --infobox "No IOS devices..No need to build cdp-neighbors-IOS File" 15 80 ; sleep 4
      echo ""
fi
#########################

#########################
if [ -s /usr/DCDP/good-IPs/NX-OS-IPs.txt ]
then
      echo ""
      dialog --infobox "Building cdp-neighbors-NXOS File. Standby..." 15 80 ; sleep 4
      echo ""
      cd /usr/DCDP/cdp-neighbors
    	./NXOS-CDP-Neighbors.sh
      sleep 3
      
else
      dialog --infobox "No NX-OS devices..No need to build cdp-neighbors-NXOS File" 15 80 ; sleep 4
      echo ""
fi

dialog --infobox "Getting Ready to Run all MySQL Database Inventories..." 15 80 ; sleep 4

#########################
cd /usr/DCDP/Inventory/
echo ""
python Truncate_IOS_DB.py db_ios_connection.txt
python Truncate_NXOS_DB.py db_nxos_connection.txt

#########################
if [ -s /usr/DCDP/good-IPs/IOS-IPs.txt ]
then
      echo ""
      echo "  ---------------------------------------------------------"
      echo "         Calling IOS Inventory Python Script..."
      echo "  ---------------------------------------------------------"
      echo ""
      cd /usr/DCDP/Program-Files/
      python DCDP_xml_IOS_Inventory.py db_ios_connection.txt
      sleep 3
      
      
      echo ""
      echo "  ---------------------------------------------------------"
      echo "     Writing IOS_Inventory to MySQL...Standby..."
      echo "  ---------------------------------------------------------"
      cd /usr/DCDP/Inventory/
      ./ios-db-to-xml.sh
else
      echo ""
      echo "  ---------------------------------------------------------"
      echo " No IOS devices..No need to Run IOS Database related scripts."
      echo "  ---------------------------------------------------------"
      echo ""
fi
#########################

#########################
echo ""
echo ""
if [ -s /usr/DCDP/good-IPs/NX-OS-IPs.txt ]
then
      echo ""
      echo "  ---------------------------------------------------------"
    	echo "        Calling NX-OS Inventory Python Script..."
      echo "  ---------------------------------------------------------"
	    cd /usr/DCDP/Program-Files/
	    python DCDP_xml_NXOS_Inventory.py db_nxos_connection.txt
      sleep 3
      
      
	    echo ""
	    echo "  ---------------------------------------------------------"
	    echo "     Writing NXOS_Inventory to MySQL...Standby..."
      echo "  ---------------------------------------------------------"
	    cd /usr/DCDP/Inventory/
	    ./nxos-db-to-xml.sh
	    echo ""
else
      echo ""
      echo "  ---------------------------------------------------------"
    	echo " No NX-OS devices..No need to Run NX-OS Database related scripts"
    	echo "  ---------------------------------------------------------"
      echo ""
fi
cd /usr/DCDP/Inventory/
echo "  ---------------------------------------------------------"
echo "   Backing up the IOS and NXOS MySQL Databases...Standby..."
echo "  ---------------------------------------------------------"

./IOS-DB-Backup.sh
./NXOS-DB-Backup.sh
#########################
cd /usr/DCDP/CDP-Inventory/
echo ""
echo "  ---------------------------------------------------------"
echo "  Truncating the CDP table from the MySQL database..Standby..."
echo "  ---------------------------------------------------------"
echo ""
python CDP-Truncate-DB.py db_cdp_connection.txt
#########################
cd /usr/DCDP/Program-Files/

python DCDP_xml_cdp_diagrams.py db_cdp_connection.txt
sleep 3



cd /usr/DCDP/CDP-Inventory/
./cdp-db-to-xml.sh
echo ""
echo "  ---------------------------------------------------------"
echo "      Backing up the CDP MySQL Database...Standby..."
echo "  ---------------------------------------------------------"
echo ""
./CDP-DB-Backup.sh
echo "  ---------------------------------------------------------"
echo "          Removing Temporary files...Standby..."
echo "  ---------------------------------------------------------"
echo ""
echo "  ---------------------------------------------------------"
echo "  Creating final xml file for generating diagrams...Standby..."
echo "  ---------------------------------------------------------"

########################################
if [ -f /usr/DCDP/Inventory/Cisco_NXOS_Inventory.xml ] && [ -f /usr/DCDP/Inventory/Cisco_IOS_Inventory.xml ]
then
    cd /usr/DCDP/Inventory
    cp Cisco_NXOS_Inventory.xml /usr/DCDP/bin/diagram-generation/
    cp Cisco_IOS_Inventory.xml /usr/DCDP/bin/diagram-generation/
    cd /usr/DCDP/CDP-Inventory/
    cp CDP_Inventory.xml /usr/DCDP/bin/diagram-generation/
    cd /usr/DCDP/bin/diagram-generation
    python xml-merge.py CDP_Inventory.xml Cisco_IOS_Inventory.xml Cisco_NXOS_Inventory.xml > $DataCenter-diagram-generation.xml
    rm /usr/DCDP/bin/diagram-generation/CDP_Inventory.xml
    rm /usr/DCDP/bin/diagram-generation/Cisco_IOS_Inventory.xml
    rm /usr/DCDP/bin/diagram-generation/Cisco_NXOS_Inventory.xml

elif [ -f /usr/DCDP/Inventory/Cisco_IOS_Inventory.xml ]
then
    cd /usr/DCDP/Inventory/
    cp Cisco_IOS_Inventory.xml /usr/DCDP/bin/diagram-generation/
    cd /usr/DCDP/CDP-Inventory/
    cp CDP_Inventory.xml /usr/DCDP/bin/diagram-generation/
    cd /usr/DCDP/bin/diagram-generation
    python xml-merge.py CDP_Inventory.xml Cisco_IOS_Inventory.xml > $DataCenter-diagram-generation.xml
    rm /usr/DCDP/bin/diagram-generation/CDP_Inventory.xml
    rm /usr/DCDP/bin/diagram-generation/Cisco_IOS_Inventory.xml
else
    cd /usr/DCDP/Inventory/
    cp Cisco_NXOS_Inventory.xml /usr/DCDP/bin/diagram-generation/
    cd /usr/DCDP/CDP-Inventory/
    cp CDP_Inventory.xml /usr/DCDP/bin/diagram-generation/
    cd /usr/DCDP/bin/diagram-generation
    python xml-merge.py CDP_Inventory.xml Cisco_NXOS_Inventory.xml > $DataCenter-diagram-generation.xml
    rm /usr/DCDP/bin/diagram-generation/CDP_Inventory.xml
    rm /usr/DCDP/bin/diagram-generation/Cisco_NXOS_Inventory.xml
fi
########################################
# Get stats and build stats file
cd /usr/DCDP/Program-Files
./dcdp-stats.bash
sleep 10
echo "See the /usr/DataCenters/$DataCenter/DCDP/stats/stats.txt file for a summary of this information"

### MOVE DATA INTO THE DC
cp -r /usr/DCDP /usr/DataCenters/$DataCenter

rm /usr/DataCenters/$DataCenter/DCDP/*.sh
 

cp /usr/DCDP/stats/tmp/ssh-version-errors.txt /usr/DataCenters/$DataCenter/DCDP/stats/ssh-version-errors-IPs.txt
cp /usr/DCDP/stats/tmp/auth-errors.txt /usr/DataCenters/$DataCenter/DCDP/stats/auth-errors-IPs.txt
rm -r /usr/DataCenters/$DataCenter/DCDP/stats/tmp
rm -r /usr/DataCenters/$DataCenter/DCDP/tmp
rm -r /usr/DataCenters/$DataCenter/DCDP/Program-Files

rm /usr/DataCenters/$DataCenter/DCDP/Inventory/*.py
rm /usr/DataCenters/$DataCenter/DCDP/Inventory/*.txt
rm /usr/DataCenters/$DataCenter/DCDP/Inventory/*.sh

rm /usr/DataCenters/$DataCenter/DCDP/hostname-to-IPs/*.txt

rm /usr/DataCenters/$DataCenter/DCDP/cdp-neighbors/*.sh

rm /usr/DataCenters/$DataCenter/DCDP/CDP-Inventory/*.py
rm /usr/DataCenters/$DataCenter/DCDP/CDP-Inventory/*.txt
rm /usr/DataCenters/$DataCenter/DCDP/CDP-Inventory/*.sh

rm -r /usr/DataCenters/$DataCenter/DCDP/bin/snmpwalk_add_on_app-for-bad-IPs
rm -r /usr/DataCenters/$DataCenter/DCDP/bin/python_custom_scripts

rm -r /usr/DataCenters/$DataCenter/DCDP/configs/IOS
rm -r /usr/DataCenters/$DataCenter/DCDP/configs/NXOS
rm -r /usr/DataCenters/$DataCenter/DCDP/configs/sh-ip-inter-brief-sh-ver

#################
rm /usr/DCDP/tmp/*.txt
rm /usr/DCDP/good-IPs/*.txt

rm /usr/DCDP/CDP-Inventory/*.sql
rm /usr/DCDP/CDP-Inventory/*.xml

rm /usr/DCDP/Inventory/*.sql
rm /usr/DCDP/Inventory/*.xml

rm /usr/DCDP/cdp-neighbors/*.txt

rm /usr/DCDP/bad-IPs/*.txt
rm /usr/DCDP/hostname-to-IPs/*
rm /usr/DCDP/Full-IP-List/*
rm /usr/DCDP/cdp_files/*
rm /usr/DCDP/stats/*.txt
rm -r /usr/DCDP/stats/tmp/*.txt
rm /usr/DCDP/bin/diagram-generation/*.xml
rm -r /usr/DCDP/configs/sh-ip-inter-brief-sh-ver

find /usr/DataCenters/ -name "*diagram*xml" -type f -exec cp {} /var/www/django_app/mysite/ndna-diagram-xmls/ \;

cd /usr/DataCenters/$DataCenter/DCDP/
zip -r -q $DataCenter-DCDP-Backup-$date.zip /usr/DataCenters/$DataCenter/DCDP/
mv *.zip /usr/Backups/
echo ""
echo ""
#################



#################
dialog --infobox "                Exiting with final instructions. Thank You!" 15 80 ; sleep 4



echo "############################################################"
echo "  -------------------------------------------------------- "
echo "           Program has completed for $DataCenter           "
echo "                                                           "
echo "              Thank you for being patient                 "
echo "                                                           "
echo "You must now review all logs in /usr/DataCenters/$DataCenter/DCDP/logs "
echo ""
echo "          Follow instructions in the user guide       "
echo "          To ensure the most complete discovery              "  
echo "  -------------------------------------------------------- "
echo "############################################################"
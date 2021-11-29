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

echo "#################################################################"
read -p "Enter Data_Center String Here e.g. New-York-DC: " DataCenter
echo "#################################################################"
echo ""
echo ""
echo "###########################################################################################"
echo "You will be prompted to enter the DataCenter Name Once more when the Python Script Runs...."
echo "###########################################################################################"
echo ""
echo ""


DataCenterdir=/usr/DataCenters/$DataCenter
 
if [ -d "$DataCenterdir" ];
then
   echo "Data_Center Exists...."
else
   echo "Data_Center does not exist...Program exiting. Goodbye..."
   echo ""
   exit 1
fi

##############################
if [ -s /usr/DataCenters/$DataCenter/DCDP/good-IPs/NX-OS-IPs.txt ]
then
    echo "** Building NXOS L2-L3 IP lists"   
    python /usr/DCDP/bin/python_custom_scripts/Manual-Updates/L2-L3-IP-Lists/L2-L3-NXOS-Manual.py
    
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
    # REMOVE TEMP FILES USED TO BUILD L3-NX-OS-IPs.txt FILE  - NOTICE THE Original file name is NXOS and the new one is NX-OS thus doesn't get deleted
    rm /usr/DCDP/good-IPs/L3-NX-OS-IPs-pre.txt
    rm /usr/DCDP/configs/*NXOS*.txt
    
    ## Must first copy the full NXOS IP-LIST from variable datacenter *back* into the /user/DCDP/good-IPs folder before we run the L2-IPLIST.py script
    cp /usr/DataCenters/$DataCenter/DCDP/good-IPs/NX-OS-IPs.txt /usr/DCDP/good-IPs/

    ## Copy the final L3 IPs txt file into the variable Datacenter
    cp /usr/DCDP/good-IPs/L3-NX-OS-IPs.txt /usr/DataCenters/$DataCenter/DCDP/good-IPs/

    # Build L2 IP list file
    python /usr/DCDP/Program-Files/NXOS-L2-IPLIST.py

    ## Copy the final L2 IPs txt file into the variable Datacenter
    cp /usr/DCDP/good-IPs/L2-NX-OS-IPs.txt /usr/DataCenters/$DataCenter/DCDP/good-IPs/
    echo ""
    echo ""
    echo "** Completed Building NXOS L2-L3 IP lists for $DataCenter.....Please review log files for errors"
else
    echo "No NXOS Devices for $DataCenter. Skipping L2-L3 IP lists for NXOS devices..."
fi
##############################
echo ""
echo ""
##############################
if [ -s /usr/DataCenters/$DataCenter/DCDP/good-IPs/IOS-IPs.txt ]
then
    echo "** Building IOS L2-L3 IP lists"
    python /usr/DCDP/bin/python_custom_scripts/Manual-Updates/L2-L3-IP-Lists/L2-L3-IOS-Manual.py
    
    
    # Change into configs directory of main program. Grep for devices running a routing protocol
    # NOTICE THE SPACE AFTER ROUTER. THIS IS NEEDED
    # grep -v removes the command sh run which includes router, although not really needed due to matching on regex, start of line for router
    cd /usr/DCDP/configs/

    #OLD WAY BELOW - WOULDNT WORK WITH SINGLE DEVICE
    #ls | grep -v "sh run" | grep ^"router " *IOS_.txt > IOS-L3-TEMP.txt 
    #NEW WAY BELOW - WORKS WITH SINGLE IOS DEVICE
    ls | grep -v "sh run" | grep -H ^"router " *IOS_.txt > IOS-L3-TEMP.txt 
    #ls *IOS_.txt | grep -v "sh run" | grep -r --exclude=IOS-L3-TEMP.txt ^"router " > IOS-L3-TEMP.txt

    cat IOS-L3-TEMP.txt | sed -e 's/_IOS_.txt:.*//' > /usr/DCDP/good-IPs/L3-IOS-IPs-pre.txt
    ## THIS WILL REMOVE ALL DUPLICATES IPs
    cat /usr/DCDP/good-IPs/L3-IOS-IPs-pre.txt | awk '!seen[$0]++' > /usr/DCDP/good-IPs/L3-IOS-IPs.txt
    # REMOVE TEMP FILES USED TO BUILD L3-IOS-IPs.txt FILE
    rm /usr/DCDP/good-IPs/L3-IOS-IPs-pre.txt
    rm /usr/DCDP/configs/*IOS*.txt


    ## Must first copy the full IOS IP-LIST from variable datacenter *back* into the /user/DCDP/good-IPs folder before we run the L2-IPLIST.py script
    cp /usr/DataCenters/$DataCenter/DCDP/good-IPs/IOS-IPs.txt /usr/DCDP/good-IPs/

    ## Copy the final L3 IPs txt file into the variable Datacenter
    cp /usr/DCDP/good-IPs/L3-IOS-IPs.txt /usr/DataCenters/$DataCenter/DCDP/good-IPs/

    # Build L2 IP list file
    python /usr/DCDP/Program-Files/IOS-L2-IPLIST.py

    ## Copy the final L2 IPs txt file into the variable Datacenter
    cp /usr/DCDP/good-IPs/L2-IOS-IPs.txt /usr/DataCenters/$DataCenter/DCDP/good-IPs/

    echo ""
    echo ""
    echo "** Completed Building IOS L2-L3 IP lists for $DataCenter.....Please review log files for errors"
else
    echo "No IOS Devices for $DataCenter. Skipping L2-L3 IP lists for IOS devices..."
fi
#########################
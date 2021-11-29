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


#chmod 755 *.sh
echo ""
echo "####################################################################"
read -p "Enter Your Data_Center String Here e.g. New-York-DC: " DataCenter
echo ""
echo ""
echo "    You will be asked to Enter It Again One More Time...."
echo "####################################################################"
echo ""
python SNMPWALK-Bad-IPs-sysname-sysdescr.py
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



# build file with keys for dict
echo "IP-Address,Hostname" > /usr/DataCenters/$DataCenter/DCDP/snmpwalk/snmpwalk-BAD-IPs-Hostname-Platform-pre.csv


cd /usr/DataCenters/$DataCenter/DCDP/snmpwalk/
# build temp snmpwalk.txt file to avoid errors on cat if no other real snmpwalk files exist
touch temp-snmpwalk.txt

# Cat *snmpwalk.txt files and redirect output to temp file to evaluate if  there is any size to it or not, e.g. do any snmpwalk.txt files exist
cat *snmpwalk.txt > /usr/DataCenters/$DataCenter/DCDP/snmpwalk/temp.txt

if [ -s temp.txt ]
then
     ls | grep 'iso.3.6.1.2.1.1.5.0' *snmpwalk.txt | awk {'print $1 ","$4'} | sed -e 's/_snmpwalk.txt:iso.3.6.1.2.1.1.5.0//' | sed -e 's/"//' | sed -e 's/"//' | sed -e 's/,/ ,/' >> snmpwalk-BAD-IPs-Hostname-Platform-pre.csv
     cat /usr/DataCenters/$DataCenter/DCDP/snmpwalk/snmpwalk-BAD-IPs-Hostname-Platform-pre.csv | awk '{ if (a[$2]++ ==0) print $0; }' > /usr/DataCenters/$DataCenter/DCDP/snmpwalk/snmpwalk-BAD-IPs-Hostname-Platform.csv
     rm snmpwalk-BAD-IPs-Hostname-Platform-pre.csv
     rm temp.txt
     rm temp-snmpwalk.txt
     echo "The Program has Completed for $DataCenter"
else
	echo "No output files. No devices have responded to SNMP requests for $DataCenter"
	rm temp.txt
    rm temp-snmpwalk.txt
fi
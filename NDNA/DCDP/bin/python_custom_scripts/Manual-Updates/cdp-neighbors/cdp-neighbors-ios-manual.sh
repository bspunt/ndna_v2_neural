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

echo "#################################################################"
read -p "Enter Data_Center String Here e.g. ACM:New-York-DC: " DataCenter
echo "#################################################################"
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

#########################
if [ -s /usr/DataCenters/$DataCenter/DCDP/good-IPs/IOS-IPs.txt ]
then
      echo ""
      echo ""
      cp /usr/DataCenters/$DataCenter/DCDP/good-IPs/IOS-IPs.txt /usr/DCDP/good-IPs/
      echo "** Building cdp-neighbors-IOS File. Standby...."
      echo ""
      echo ""
      python /usr/DCDP/Program-Files/sh-cdp-nei.py
      #############################
      cd /usr/DCDP/tmp
      cat *ios-ips.txt > /usr/DCDP/cdp-neighbors/CDP-File-For-Detailed-Diagrams.txt
      #############################
      # Copy new IOS CDP file into the variable Datacenter
      cp /usr/DCDP/cdp-neighbors/CDP-File-For-Detailed-Diagrams.txt /usr/DataCenters/$DataCenter/DCDP/cdp-neighbors/
      echo "#################################################################"
      echo " ** IOS-CDP-Neighbors file has been updated for $DataCenter...Please review log files for errors"
      echo "#################################################################"
      echo ""
      echo ""
      sleep 3
      rm /usr/DCDP/cdp-neighbors/CDP-File-For-Detailed-Diagrams.txt

else
      echo ""
      echo ""
      echo "** No IOS devices..No need to build cdp-neighbors-IOS File."
      echo ""
      echo ""
fi
#########################
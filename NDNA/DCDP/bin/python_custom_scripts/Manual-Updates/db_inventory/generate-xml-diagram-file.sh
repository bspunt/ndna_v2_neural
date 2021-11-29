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
read -p "Enter Data_Center String Here e.g. New-York-DC: " DataCenter
echo "#################################################################"

DataCenterdir=/usr/DataCenters/$DataCenter
 
if [ -d "$DataCenterdir" ];
then
   echo "Data_Center Exists...."
else
   echo "Data_Center does not exist...Program exiting. Goodbye..."
   echo ""
   exit 1
fi
#########################################################################
echo "** Creating final xml file for generating diagrams!...Standby..."
########################################

########################################
if [ -f /usr/DataCenters/$DataCenter/DCDP/Inventory/Cisco_NXOS_Inventory.xml ] && [ -f /usr/DataCenters/$DataCenter/DCDP/Inventory/Cisco_IOS_Inventory.xml ]
then
    cd /usr/DataCenters/$DataCenter/DCDP/Inventory
    cp Cisco_NXOS_Inventory.xml /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/
    cp Cisco_IOS_Inventory.xml /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/
    cd /usr/DataCenters/$DataCenter/DCDP/CDP-Inventory/
    cp CDP_Inventory.xml /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/
    cd /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation
    python xml-merge.py CDP_Inventory.xml Cisco_IOS_Inventory.xml Cisco_NXOS_Inventory.xml > $DataCenter-diagram-generation.xml
    rm /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/CDP_Inventory.xml
    rm /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/Cisco_IOS_Inventory.xml
    rm /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/Cisco_NXOS_Inventory.xml

elif [ -f /usr/DataCenters/$DataCenter/DCDP/Inventory/Cisco_NXOS_Inventory.xml ]
then
    cd /usr/DataCenters/$DataCenter/DCDP/Inventory
    cp Cisco_NXOS_Inventory.xml /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/
    cd /usr/DataCenters/$DataCenter/DCDP/CDP-Inventory/
    cp CDP_Inventory.xml /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/
    cd /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation
    python xml-merge.py CDP_Inventory.xml Cisco_NXOS_Inventory.xml > $DataCenter-diagram-generation.xml
    rm /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/CDP_Inventory.xml
    rm /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/Cisco_NXOS_Inventory.xml
else
    cd /usr/DataCenters/$DataCenter/DCDP/Inventory
    cp Cisco_IOS_Inventory.xml /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/
    cd /usr/DataCenters/$DataCenter/DCDP/CDP-Inventory/
    cp CDP_Inventory.xml /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/
    cd /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation
    python xml-merge.py CDP_Inventory.xml Cisco_IOS_Inventory.xml > $DataCenter-diagram-generation.xml
    rm /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/CDP_Inventory.xml
    rm /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation/Cisco_IOS_Inventory.xml
fi

echo " ####################################################################"
echo ""
echo "    The Program Has Completed. Please view the $DataCenter folder" 
echo "  Located at /usr/DataCenters/$DataCenter/DCDP/bin/diagram-generation"
echo " Look for the $DataCenter-diagram-generation.xml for use in generating diagrams" 
echo ""
echo " ####################################################################"
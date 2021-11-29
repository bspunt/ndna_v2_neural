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
read -p "Enter The Name of the VNAD LE or DataCenter You Want To Restore: " DataCenter
echo "#################################################################"
#########################################################################

## The following path must still exist 
## /usr/DataCenters/<DC-NAME>

# Below runs on backup DC ZIP that has been copied over to the Restore Folder

# Must FIRST COPY OVER backup ZIP FLE you want to restore to the Restore folder

unzip -q $DataCenter*.zip 



######### Declare global dir variables -->
DIR=/usr/DataCenters/$DataCenter
VNADDIR=/usr/VNAD-LEs/$DataCenter

if [ -d "$DIR" ];
then
   cd /usr/Restore/usr/DataCenters/$DataCenter
   cp -r VNAD/ /usr/DataCenters/$DataCenter
fi

if [ -d "$VNADDIR" ];
then
   cd /usr/Restore/usr/VNAD-LEs/$DataCenter
   cp -r VNAD/ /usr/VNAD-LEs/$DataCenter
fi

# Clean up Restore folder
cd /usr/Restore/
rm $DataCenter*.zip
rm -r /usr/Restore/usr

echo "**  VNAD Data Restore completed for $DataCenter"
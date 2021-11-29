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
echo "Enter the 3 Character Company (or Company region) Code. E.G. if you have DataCenter Folders, Example: You have: MIC:LA-DC, MIC:NY-DC You would enter just MIC"
echo ""
echo "This will allow you to build enterprise wide IP Lists *per company* or *company entity, e.g. by region*"
echo ""
read -p "Enter 3 Character Company Code: " Company
echo ""
date=$(date +"%b-%d-%y")

echo "Building Enterprise Wide IOS IP list (For ALL L3 Devices)"
echo ""
find /usr/DataCenters/$Company*/DCDP/* -name "L3-IOS-IPs.txt" -exec cat {} \; > /usr/enterprise-wide-routers/Created-IP-Lists/$Company-enterprise-wide-ios-routers-$date.txt
#
echo "Enterprise Wide IOS IP list for $Company (For L3 Devices) Has Completed..."
echo ""
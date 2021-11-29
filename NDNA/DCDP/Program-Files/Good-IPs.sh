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


#cat /usr/DCDP/logs/dcdp.log | egrep '** Completed|DONE' | awk '{print $NF}' > /usr/DCDP/good-IPs/Good-IPs.txt
cat /usr/DCDP/hostname-to-IPs/hostname-to-IPs-NX-OS.csv | grep -v cmp | sed -e 's/,/ ,/' | awk {'print $1'} | sed -e 's/IP-Address//' | sed -e 's/_seed.*//' | sed -e 's/_seed//' | sed '/^\s*$/d' > /usr/DCDP/good-IPs/Good-IPs.txt
cat /usr/DCDP/hostname-to-IPs/hostname-to-IPs-IOS.csv | sed -e 's/_seed.*//' | sed -e 's/_seed//' | sed -e 's/,/ ,/' | awk {'print $1'} | sed -e 's/IP-Address//' | sed '/^\s*$/d' >> /usr/DCDP/good-IPs/Good-IPs.txt
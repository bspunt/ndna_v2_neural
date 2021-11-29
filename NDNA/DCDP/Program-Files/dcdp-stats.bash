#!/bin/bash
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

wc -l /usr/DCDP/good-IPs/Good-IPs.txt | awk {'print $1'} > /usr/DCDP/stats/tmp/GOOD-IP-Counts.txt
cd /usr/DCDP/stats/tmp/
GOODIPCounts=$(<GOOD-IP-Counts.txt) 

echo "The total number of Good IP hosts (Total number of successful connections, e.g. Authentication Success) is: $GOODIPCounts" 

############################

wc -l /usr/DCDP/good-IPs/IOS-IPs.txt | awk {'print $1'} > /usr/DCDP/stats/tmp/IOS-IP-Counts.txt
cd /usr/DCDP/stats/tmp/
IOSIPCounts=$(<IOS-IP-Counts.txt) 

echo "The total number of IOS IP hosts discovered is: $IOSIPCounts"

############################

wc -l /usr/DCDP/good-IPs/NX-OS-IPs.txt | awk {'print $1'} > /usr/DCDP/stats/tmp/NXOS-IP-Counts.txt
cd /usr/DCDP/stats/tmp/
NXOSIPCounts=$(<NXOS-IP-Counts.txt) 

echo "The total number of NXOS IP hosts discovered is: $NXOSIPCounts"


############################
cat /usr/DCDP/logs/dcdp.log | grep "* Authentication Error for" | sed -e 's/.* for //' > /usr/DCDP/stats/tmp/auth-errors.txt
cd /usr/DCDP/stats/tmp/
wc -l auth-errors.txt | awk {'print $1'} > /usr/DCDP/stats/tmp/auth-errors-final.txt
AUTHERRORCounts=$(<auth-errors-final.txt) 

echo "The total number of hosts with authentication errors is: $AUTHERRORCounts"

############################
cat /usr/DCDP/logs/dcdp.log | grep "* Incompatible SSH version" | sed -e 's/.* device //' > /usr/DCDP/stats/tmp/ssh-version-errors.txt
cd /usr/DCDP/stats/tmp/
wc -l ssh-version-errors.txt | awk {'print $1'} > /usr/DCDP/stats/tmp/ssh-version-errors-final.txt
cd /usr/DCDP/stats/tmp/
SSHVERERRORCounts=$(<ssh-version-errors-final.txt) 

echo "The total number of Incompatible SSH version hosts is: $SSHVERERRORCounts"
############################


############################
echo "The total number of Good IP hosts (Total number of successful connections, e.g. Authentication Success) is: $GOODIPCounts" > /usr/DCDP/stats/stats.txt
echo "The total number of IOS IP hosts discovered is: $IOSIPCounts" >> /usr/DCDP/stats/stats.txt
echo "The total number of NXOS IP hosts discovered is: $NXOSIPCounts" >> /usr/DCDP/stats/stats.txt


############################

if [ -f /usr/DCDP/good-IPs/L2-IOS-IPs.txt ]
then
	wc -l /usr/DCDP/good-IPs/L2-IOS-IPs.txt | awk {'print $1'} > /usr/DCDP/stats/tmp/L2-IOS-IP-Counts.txt
	cd /usr/DCDP/stats/tmp/
	L2IOSIPCounts=$(<L2-IOS-IP-Counts.txt) 
	echo "The total number of L2-IOS IP hosts discovered is: $L2IOSIPCounts"
	echo "The total number of L2-IOS IP hosts discovered is: $L2IOSIPCounts" >> /usr/DCDP/stats/stats.txt 
else
    :
fi
############################

############################
if [ -f /usr/DCDP/good-IPs/L3-IOS-IPs.txt ]
then
	wc -l /usr/DCDP/good-IPs/L3-IOS-IPs.txt | awk {'print $1'} > /usr/DCDP/stats/tmp/L3-IOS-IP-Counts.txt
	cd /usr/DCDP/stats/tmp/
	L3IOSIPCounts=$(<L3-IOS-IP-Counts.txt) 
	echo "The total number of L3-IOS IP hosts discovered is: $L3IOSIPCounts"
	echo "The total number of L3-IOS IP hosts discovered is: $L3IOSIPCounts" >> /usr/DCDP/stats/stats.txt 
else
    :
fi
############################
############################
if [ -f /usr/DCDP/good-IPs/L2-NX-OS-IPs.txt ]
then
	wc -l /usr/DCDP/good-IPs/L2-NX-OS-IPs.txt | awk {'print $1'} > /usr/DCDP/stats/tmp/L2-NXOS-IP-Counts.txt
	cd /usr/DCDP/stats/tmp/
	L2NXOSIPCounts=$(<L2-NXOS-IP-Counts.txt) 
	echo "The total number of L2-NXOS IP hosts discovered is: $L2NXOSIPCounts"
	echo "The total number of L2-NXOS IP hosts discovered is: $L2NXOSIPCounts" >> /usr/DCDP/stats/stats.txt 
else
    :
fi
############################
############################
if [ -f /usr/DCDP/good-IPs/L3-NX-OS-IPs.txt ]
then
	wc -l /usr/DCDP/good-IPs/L3-NX-OS-IPs.txt | awk {'print $1'} > /usr/DCDP/stats/tmp/L3-NXOS-IP-Counts.txt
	cd /usr/DCDP/stats/tmp/
	L3NXOSIPCounts=$(<L3-NXOS-IP-Counts.txt) 
	echo "The total number of L3-NXOS IP hosts discovered is: $L3NXOSIPCounts"
	echo "The total number of L3-NXOS IP hosts discovered is: $L3NXOSIPCounts" >> /usr/DCDP/stats/stats.txt 
else
    :
fi
############################

echo "The total number of hosts with authentication errors is: $AUTHERRORCounts" >> /usr/DCDP/stats/stats.txt
echo "The total number of Incompatible SSH version hosts is: $SSHVERERRORCounts" >> /usr/DCDP/stats/stats.txt
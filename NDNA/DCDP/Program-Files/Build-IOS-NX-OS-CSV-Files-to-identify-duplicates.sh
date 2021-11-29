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
cd /usr/DCDP/configs/sh-ip-inter-brief-sh-ver

#REMOVE CARRIAGE RETURNS FROM CONFIGS PULLED FROM CURRENT DC PROGRAM RUN...
sed -i 's/[\r\n]//'g *.txt

# build file with keys for dict
#echo "IP-Address,Hostname" > /usr/DCDP/hostname-to-IPs/hostname-to-IPs-IOS.csv
#echo "IP-Address,Hostname" > /usr/DCDP/hostname-to-IPs/hostname-to-IPs-NX-OS.csv
# append to file with values 

# build "pre-final" csv file with key/values (dict)
echo "IP-Address, Hostname" > /usr/DCDP/hostname-to-IPs/hostname-to-IPs-IOS-PRE.csv
echo "IP-Address, Hostname" > /usr/DCDP/hostname-to-IPs/hostname-to-IPs-NX-OS-PRE.csv

touch /usr/DCDP/configs/NXOS/test.txt
touch /usr/DCDP/configs/IOS/test.txt

# Truncate NXOS and IOS directories, then Move CURRENT NXOS and IOS configs from sh-ip-inter-brief dirs into /usr/DCDP/configs/ SUB-directories
rm -r /usr/DCDP/configs/NXOS/*
rm -r /usr/DCDP/configs/IOS/*

# CAT FOR NX-OS STRING - OUTPUT TO TEMP FILE TO RUN CONDITIONAL ON..
cat /usr/DCDP/configs/sh-ip-inter-brief-sh-ver/*.txt | grep NX-OS > /usr/DCDP/configs/NXOS/temp.txt

cd /usr/DCDP/configs/NXOS/
if [ -s temp.txt ]
then
	 #remove temp file
     rm /usr/DCDP/configs/NXOS/temp.txt
     # identify NX-OS string in files in sh-ip-inter-brief dir and move to configs/NXOS directory
     grep -lr 'NX-OS' /usr/DCDP/configs/sh-ip-inter-brief-sh-ver/*.txt | xargs mv -t /usr/DCDP/configs/NXOS
else
	 echo ""

     echo "** No NX-OS DEVICES...Skipping NXOS related CSV file tasks"
fi

# identify NX-OS string in files in sh-ip-inter-brief dir and move to configs/NXOS directory
#grep -lr 'NX-OS' /usr/DCDP/configs/sh-ip-inter-brief-sh-ver/*.txt | xargs mv -t /usr/DCDP/configs/NXOS

# no space from # to terminal length 0 (e.g. just query on terminal length 0) to account for possible future NXOS changes to terminal output
# ONLY NXOS files in this directory
cd /usr/DCDP/configs/NXOS
#ls | grep 'terminal length 0' *.txt > /usr/DCDP/hostname-to-IPs/NXOS-hostname-to-IPs.txt
ls *.txt | grep -r --exclude=NXOS-hostname-to-IPs.txt 'terminal length 0' > /usr/DCDP/hostname-to-IPs/NXOS-hostname-to-IPs.txt

#cat /usr/DCDP/hostname-to-IPs/hostname-to-IPs.txt | grep 'Device name' | awk {'print $1 "," $4'} | sed -e 's/_.*_level.txt://' >> /usr/DCDP/hostname-to-IPs/hostname-to-IPs-NX-OS.csv
cat /usr/DCDP/hostname-to-IPs/NXOS-hostname-to-IPs.txt | grep '# terminal length 0' | awk {'print $1'} | sed -e 's/_.*_level.txt:/, /' | sed -e 's/_.*seed.txt:/, /' | sed -e 's/#//' >> /usr/DCDP/hostname-to-IPs/hostname-to-IPs-NX-OS-PRE.csv

## THIS WILL REMOVE ALL DUPLICATES (Find common string of hostname and remove all other lines with same occurance even tho IPs are unique)
cat /usr/DCDP/hostname-to-IPs/hostname-to-IPs-NX-OS-PRE.csv | awk '{ if (a[$2]++ ==0) print $0; }' > /usr/DCDP/hostname-to-IPs/hostname-to-IPs-NX-OS.csv

#ls | egrep 'uptime is|Device name:' *.txt > /usr/DCDP/hostname-to-IPs/hostname-to-IPs.txt
#ls | egrep 'uptime is|#terminal length 0' *.txt > /usr/DCDP/hostname-to-IPs/hostname-to-IPs.txt




# CAT FOR NX-OS STRING - OUTPUT TO TEMP FILE TO RUN CONDITIONAL ON..
cat /usr/DCDP/configs/sh-ip-inter-brief-sh-ver/*.txt | grep IOS > /usr/DCDP/configs/IOS/temp2.txt

cd /usr/DCDP/configs/IOS/
if [ -s temp2.txt ]
then
	 #remove temp file
     rm /usr/DCDP/configs/IOS/temp2.txt
     # identify IOS string in files in sh-ip-inter-brief dir and move to configs/IOS directory
     grep -lr 'IOS' /usr/DCDP/configs/sh-ip-inter-brief-sh-ver/*.txt | xargs mv -t /usr/DCDP/configs/IOS
else
	 echo ""

     echo "** No IOS DEVICES...Skipping IOS related CSV file tasks"
fi
# identify IOS string in files in sh-ip-inter-brief dir and move to configs/IOS directory
#grep -lr 'IOS' /usr/DCDP/configs/sh-ip-inter-brief-sh-ver/*.txt | xargs mv -t /usr/DCDP/configs/IOS

cd /usr/DCDP/configs/IOS
#ls | grep 'uptime is' *.txt > /usr/DCDP/hostname-to-IPs/IOS-hostname-to-IPs.txt
ls *.txt | grep -r --exclude=IOS-hostname-to-IPs.txt "uptime is" > /usr/DCDP/hostname-to-IPs/IOS-hostname-to-IPs.txt
#cat /usr/DCDP/hostname-to-IPs/hostname-to-IPs.txt | grep -v "Kernel uptime" | grep uptime | sed -e 's/.txt:/,/' | sed -e 's/, /,/' | awk {'print $1'} | sed -e 's/_.*_level//' >> /usr/DCDP/hostname-to-IPs/hostname-to-IPs-IOS.csv

cat /usr/DCDP/hostname-to-IPs/IOS-hostname-to-IPs.txt | grep -v "Kernel uptime" | grep uptime | sed -e 's/.txt: /.txt:/' | sed -e 's/.txt:/,/' | awk {'print $1'} | sed -e 's/,/, /' | sed -e 's/_.*_level//' >> /usr/DCDP/hostname-to-IPs/hostname-to-IPs-IOS-PRE.csv

## THIS WILL REMOVE ALL DUPLICATES (Find common string of hostname and remove all other lines with same occurance even tho IPs are unique)
cat /usr/DCDP/hostname-to-IPs/hostname-to-IPs-IOS-PRE.csv | awk '{ if (a[$2]++ ==0) print $0; }' > /usr/DCDP/hostname-to-IPs/hostname-to-IPs-IOS.csv

# remove temporary CSVs
cd /usr/DCDP/hostname-to-IPs
rm hostname-to-IPs-NX-OS-PRE.csv
rm hostname-to-IPs-IOS-PRE.csv
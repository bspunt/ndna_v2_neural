#!/usr/bin/env python

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


"""

Author:Brett M Spunt

This script will run a calculation on IPs, figuring in all IOS IPs minus the L3 IOS IPs, leaving only
The L2 IPs. 

"""
#import os.path
#import subprocess
#import time
#import sys
#import re
#import os

IOSL3_iplist = open('/usr/DCDP/good-IPs/L3-IOS-IPs.txt').readlines()
## remove /n from list elements
IOSL3_iplist = map(lambda s: s.strip(), IOSL3_iplist)


IOSfull_iplist = open('/usr/DCDP/good-IPs/IOS-IPs.txt').readlines()
## remove /n from list elements
IOSfull_iplist = map(lambda s: s.strip(), IOSfull_iplist)

########################################################
def L2_IPs():
    L2_iplist = set(IOSfull_iplist) - set(IOSL3_iplist)
    L2_iplist_file = open('/usr/DCDP/good-IPs/L2-IOS-IPs.txt', 'w')

    for ip in L2_iplist:
        L2_iplist_file.write("%s\n" % ip)
        ## Must have continue here or loop ends and only the first IP is written to the file!
        continue
    # close file once loop completes
    L2_iplist_file.close()
L2_IPs()
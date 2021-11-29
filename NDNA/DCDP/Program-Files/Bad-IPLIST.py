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

This script will run a calculation on IPs, figuring in all IPs minus the good IPs, leaving only
The bad IPs. It will then run a "for loop" against the bad IPs and write them to a file.

"""
#import os.path
#import subprocess
#import time
#import sys
#import re
#import os

good_iplist = open('/usr/DCDP/good-IPs/Good-IPs.txt').readlines()
## remove /n from list elements
good_iplist = map(lambda s: s.strip(), good_iplist)


full_iplist = open('/usr/DCDP/Full-IP-List/DCDP-ip-file.txt').readlines()
## remove /n from list elements
full_iplist = map(lambda s: s.strip(), full_iplist)

########################################################
def Bad_IPs():
    bad_iplist = set(full_iplist) - set(good_iplist)
    bad_iplist_file = open('/usr/DCDP/bad-IPs/Bad-IPs.txt', 'w')

    for ip in bad_iplist:
        bad_iplist_file.write("%s\n" % ip)
        ## Must have continue here or loop ends and only the first IP is written to the file!
        continue
    # close file once loop completes
    bad_iplist_file.close()
Bad_IPs()
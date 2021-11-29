#!/usr/env python

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


# Take a bunch of XML files on the command line and merge them into
# one big XML document.
#
# The root element will come from the first document; the root elements of
# subsequent documents will be lost, as will anything outside the root
# (comments and whatnot).

import sys
import libxml2

doc = None
root = None

for i in range(1, len(sys.argv)):

    newdoc = libxml2.parseFile(sys.argv[i])
    newroot = newdoc.getRootElement()

    if newroot:
        if not root:
            # first document with a root element
            doc = newdoc
            root = newroot
        else:
            # merge this into previous document
            root.addChildList(newroot.children.copyNodeList())
            newdoc.freeDoc()

if doc:
    print doc
    doc.freeDoc()
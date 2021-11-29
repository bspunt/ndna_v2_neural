

This folder and custom scripts are here to allow you to manually re-run the MySQL database CDP and IOS/NXOS Device information
inventory programs that are used to generate xml files for generating diagrams using the NDNA diagram generator.

A couple of example uses would be:

1. You run the main program, but there are transient network conditions, so a few connections didn't complete on one of the programs, say the CDP-Inventory.
2. You move some bad IPs into the good IPs (Device get's configured with your TACACS credentials, sshv1 is changed to sshv2 on a network device, etc...so you can now SSH to the device)
3. Without having to run the full DCDP.sh program, you can manually run either the CDP Inventory, IOS Inventory or NXOS Inventory to update it.

It will prompt you for the datacenter, so the output xml files will be located in the datacenter you run it against, and it will run on the IPs belonging 
to that datacenter.


4. After you run the script (which will truncate the database, pull live inventory information from the network, repopulate the database, then backup the database, and finally
will generate a new xml file.

5. After that, you can then run the shell script (./generate-xml-diagram-file.sh) 
to combine all xml files into one (which could be any combination of the CDP, IOS and NXOS xml files. This depends on if there are IOS only devices, or NXOS only devices ,etc.).

The NDNA diagram generator needs to have this one file to generate diagrams. This is done automatically when you run the main program DCDP.sh

NOTE:: If your DataCenter IP lists show no NXOS IPs (for example) in the Good-IPs folder, then you do not want to manually run the NXOS specific script in this folder, 
(You would not want to run that or any other script in this folder with the name NXOS in it, since there are no NXOS devices in your DataCenter that you can connect to.


----------------------------------------------------------
So, the simple steps would be:

ONE EXAMPLE:
You need to update CDP information (let's say IOS and NXOS information is fine)


Steps in the following order:
----------------------------


1. Run this script

# change to this directory
cd /usr/DCDP/bin/python_custom_scripts/Manual-Updates/db_inventory


./cdp_db_inventory_update.sh

 (follow the prompts)


2. Run the command just as shown below:

./generate-xml-diagram-file.sh


(Change step 1 as needed to either the ios or nxos update script and follow the prompts)

----------------------------------------------------------
# This will combine all current xml files for this DataCenter into one, e.g. the existing IOS and NXOS xmls (assuming there are both IOS and NXOS devices)
and the newly generated CDP xml file

#(this program will look at all three xml files located in the proper directories in the datacenter you specify and output the single xml 
# to that datacenter's diagram generation folder)

## If you needed to update the IOS or NXOS or any combination of the three (or all three), just run the steps 1 thru 5 as listed above, just
## changing the scripts to whichever you need to update, e.g. IOS, NXOS or CDP...If you need to update
## all three, just do steps 1 thru 4 for all three, then run step 5 as a last step to combine all three "updated" xmls...this way, you'll have 
## an updated current xml file to use in generating diagrams.
----------------------------------------------------------










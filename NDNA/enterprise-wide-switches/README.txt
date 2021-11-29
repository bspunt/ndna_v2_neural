
        ####### README ####### 

Create any type of IP Switch list you'd like, 

For example:

Running the provided scripts you can:

1. Create an enterprise wide IP list of IOS Switches.

2. Create an enterprise wide IP list of NXOS Switches.

3. Create an enterprise wide IP list of Switches. (includes BOTH NXOS and IOS)

4. Create your own list manually and put into the "enterprise-wide-switches-IPs.txt" file

After you've run any above script to create your custom switch IP Lists, you must copy and paste it into the:
"enterprise-wide-switches-IPs.txt" file located in this folder

Then, you can run the enterprise-wide-Switches.py script in the custom scripts folder
(/usr/DCDP/bin/python_custom_scripts/enterprise-wide-switches) which looks for this file (/usr/enterprise-wide-switches/enterprise-wide-switches-IPs.txt)
to determine which switches to connect to.
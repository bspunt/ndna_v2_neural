## N*etwork E*ngineer's U*nified R*ealtime A*utomation L*ibrary ©

### NEURAL Page (Overview, features, extensibility, etc.) 
https://www.automate-the-network.com/neural

NEURAL is the premiere CLI jockey replacement full stack web/app/database network automation application, providing a "no-code" web app for network engineers developed by a network engineer! 

It's built using the Django Web framework

I'll be updating this README in the future with more info, but for now, here's the intial setup instructions, after you've got your Server running, e.g. after you've 
imported the OVA into VM Workstation or got it setup within a vShere environment (or other means using the OVA)

### The OVA should be compatible with the following:

•	Workstation 14.x

•	Workstation 15.x

•	ESXi 6.7 U2

•	ESXi 6.7

•	Fusion 11.x

•	Fusion 10.x

•	VirtualBox

### It has also been setup on ESXi 6.5 and the procedure is available if needed - courtesy of Andrew Butterworth

### You can grab the OVA at:
https://www.automate-the-network.com/download-neural

• I have personally ran it (and it runs perfectly) as a VM inside a VM (and personally prefer running it this way), e.g. having your Server team just provision a Windows Server, say with 16GB of RAM and 100GB disk space on an E: Drive. Then just give the VM 6GB of RAM (which the OVA has by default). From there, I've run it and even while doing a big job, say on a thousand devices, I've never seen the memory go above 1.5GB, disk I/O very low, CPU 1 to 2%, and network I/O very low (Usually under 1Mbps). Then, you can just setup/change the network settings from bridged to NAT for even more security, e.g. to not expose port 80, e.g. don't redirect port 80 or 3306 in your VMware NAT conf file for phpmyadmin and only redirect port 443 to the NEURAL server (and you might need to set it to NAT if running as a VM on a VM inside of ESXi)

### You can watch the initial instructional Videos at (Video Overview Below):
https://www.youtube.com/channel/UCufBSk45AbJiuLWZXZFnRkg

### Inital App Setup (After you've deployed the VM)

•	Watch the instructional Videos. They also go over all of the info below

•	Run the initial setup (FQDN and Email related) from the home page link which points to the URL slug **/setup** (**See the Video for more info**)

•	Configure email relay server settings in settings.py by ssh-ing to the server or by SCP, e.g via using WinSCP using the root account and default 
password neural123 (**See the Video for more info**)

•	Configure the svcacct-netbrains user in your environment. This user must be created in your network’s authentication system, e.g. TACACS/AD and have the full privileged access to the network
The name of the account must be "svcacct-netbrains" (**See the Video for more info**)

•	Change the svcacct-netbrains user password within the django admin interface (**See the Video**). This must match what's configured in your network’s authentication system, 
e.g. TACACS/AD. By default the system comes with the password set to neural123

### To see all of the features and possibilities: 

And to get you up to speed on using the interface for automation in about an hour, please see the following links:

Instructional Videos: https://www.automate-the-network.com/neural-videos

NEURAL Page (Overview, features, extensibility, possibilities, etc.) https://www.automate-the-network.com/neural

Instructional Video Topics Overview
------------

NEURAL Web Interface overview
------------

Initial setup - (This is assuming you've already got the VM up and running...)
------------
  - create dns, run setup (FQDN, EMAIL, and EMAIL relay in settings.py), we'll go over settings.py using WinSCP (or SSH), show certain
	      links won't work till you do so. most will, but allot wont
	      also, django-redis queue will show jobs as failed if smtp relay not setup. we'll show the
	      traceback..it doesnt fail really, just the smtp portion fails and you want notifications, so set it up!
          We'll go over how to create additional users. note LDAP auth can be coded easily into AD etc.

	      go over svcacct-netbrains (default pass = neural123) 
	      MUST be created within TACACS or ldap and/or anywhere the network nodes authenticate

	      go over this account (svcacct-netbrains) is used to authenticate to the node, whereas the logged in user is tied to tracking 
	      who ran the job e.g. for logs, jobresults, etc

Building an inventory (source of truth) -
------------
	      go over inventory setup w/ delete via admin interface or mass delete via CLI


Ad Hoc Automation - (CLI Jocky Replacement, Discovery, Analysis, Programming)
------------
  - we'll go over all types of ad hoc, showing unique is == dynamic multi-task playbooks
	      go over ad hoc freeform, can build from inventory CSV export
		  
	      go over configs and how only you control these, and being able to download one or all, or delete, and open in linux term or git bash
	      
	      only you control your scheduled jobs and config templates (which we'll get to next)

	      go over device selection flexibility to be very precise, and 
	      go over device selection job tasks (dynamic self service program basically specific to your account ==
	      to a single task playbook no-code style - and no one else can use or see them)

	      be aware of browser refresh, esp w/ deleting configs....browse away from page and back to not delete new configs if you refresh browser
	      so, also, refresh using ctrl/shift + R to refresh

	      go over job email notifications and show screenshot

	      go over NAPALM Getters will be a future video

	      go over Compliance and golden configs

              ======================
	      Self Service Programs and NEURAL Notebooks will be a future video
	      Weekly config backups Including diffs and and other scheduled background jobs will be a future video
              ======================

Config templating - 
------------
  - we'll go over building configs from jinja2 templates merging with CSV files, the we'll
	      go over pushing to the network, either scheduled or run now
	      go over how only you control these, and only you control your scheduled jobs and config templates



Reporting/visibility and System Overview (Go over Menus)
------------
  - go over graphs, glances, grafana, charts.js, etc

---
End of first Instructional Video Topics Overview:
---
(Future video) Topics Overview:
---
Self Service - 
	      Custom Self Service Programs and NEURAL Notebooks will be a future video
        
Scheduled Jobs - 
	      Weekly config backups Including diffs and other scheduled background jobs will be a future video

## 
## ------------------------------------------------------------------
##     NDNAv2 codename: neural: 
##     Copyright (C) 2021  Brett M Spunt, CCIE No. 12745 (US Copyright No. Txu002053026)
## 
##     This file is part of NDNAv2.
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

from django_rq import job
from .models import *
from retrying import retry
""" supress paramiko cryptography support warnings """
import warnings 
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
import paramiko # ssh module/library
import time # time module/library
import re # regular expressions module/library
import sys # sys module/library
import threading # threading module/library
import datetime # datetime module/library
import os.path # OS module/library
import subprocess
import csv
import pandas as pd
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import MySQLdb as mdb

""" global variables """ 
#setup max number of threads for Semaphore method to use. create sema variable for open ssh function to use
max_worker_threads = 15
sema = threading.BoundedSemaphore(value=max_worker_threads)

""" import neural net network super and sub classes """
from .neural_connection_classes import *

""" Define Functions """ 
########################################################################################
""" this is related to ad_hoc automation """
#@retry(wait_fixed=2000, stop_max_attempt_number=2) If you use, note, your db writes and progress bar might not be accurate
def write_files_call_net_connect(username, command_sleep, node, command_list, task_name, job_result):
    """ aquire a thread lock """
    sema.acquire()
    timeis = datetime.datetime.now()
    current_time = timeis.strftime("%m-%d-%Y-%H:%M")

    # THIS NEEDS TO BE UPDATED ON ALL WRITE FILES TO BE TAILORED INTO THE USERS DIRECTORY!
    file_name = './configs/' + username + '/' + node + '_' + current_time + '_' + username + '_' + task_name + '.txt'
    fo = open(file_name, "w")

    """ svcacct_username is used to connect to the network """
    svcacct_username = 'svcacct-netbrains'
    svcacct_password = svcacct.objects.filter(username='svcacct-netbrains')
    for p in svcacct_password:
        password = p.password

        """ Call the Network Connection Super Class Method and write the return results to flat files for each node """
        neural_net = neural_network_conn_super_class()
        neural_net_connect_output = neural_net.open_network_connection(username, svcacct_username, password, command_sleep, node, command_list, task_name, job_result)
        fo.write(neural_net_connect_output)
        time.sleep(0.5)
        fo.close()
        
        if job_result.output == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.output = ''
        else:
            pass

        # write ssh func return data to database object called output, appending data each time for each node loop
        job_result.output = job_result.output + '\n\n*****Node Output*****'

        # combine both vars, e.g. keep building dataset of output config files to write to the sql db
        job_result.output += neural_net_connect_output
        job_result.save()

        """ release the thread """
        time.sleep(2)
        sema.release()
        #print(neural_net_connect_output) # This allows viewing to debug in the rqworker terminal during development using the development server
########################################################################################
""" all entry points are called from views.py """
@job('default', timeout=3000) 
def ad_hoc_ssh_entry_point(username, command_sleep, nodes_list, command_list, job_result):
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()
    task_name = 'ad_hoc_or_ndna'

    for node in nodes_list:
        th = threading.Thread(target = write_files_call_net_connect, args = (username, command_sleep, node, command_list, task_name, job_result))
        th.start()

    """ Threading related """
    current_thread = threading.currentThread()
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()

    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()

    job_count = job_result.total_device_count
    job_id = job_result.job_id

    job_pk = job_result.pk

    nodes_devices = [i for i in nodes_list]

    subject, from_email, to = '"ad_hoc_automation" Job Has Executed on %s devices on the NEURAL Server by %s' %(job_count, username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = '"ad_hoc_automation" with job ID %s and UUID %s Has Executed on the NEURAL Server by %s. \n\nLog into NEURAL @ https://neural.domainname.com to check the logs and get more specific job results, status and reports.\n\nYou can also view the summary results at the following link without logging in\nhttps://neural.domainname.com/automation_results/%s\n\nYou can also view the complete output at the following link (login required)\nhttps://neural.domainname.com/full_automation_results/%s\n\nSee below for a list of nodes:\n\n%s' %(job_pk, job_id, username, job_pk, job_pk, nodes_devices)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
###################################################
###################################################
@job('default', timeout=3000)  
def ndna_ssh_entry_point(username, command_sleep, nodes_list, command_list, job_result):
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()
    task_name = 'ad_hoc_or_ndna'

    # remove return from file names, e.g. remove \n from list - but do this in background worker!
    """ New Python 3.5 way of doing it, creates it as a list, just like 2.7 This is only needed for NDNA automation, as it's reading 
        the IP list from a flat file via readlines """
    nodes_list = list(map(lambda x:x.strip(),nodes_list))

    """ old Python 2.7 way of doing it, creates a map object in 3.5 """
    #nodeslist = map(lambda s: s.strip(), nodeslist)
    for node in nodes_list:
        th = threading.Thread(target = write_files_call_net_connect, args = (username, command_sleep, node, command_list,  task_name, job_result))
        th.start()

    """ new code """
    current_thread = threading.currentThread()
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()

    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()

    job_count = job_result.total_device_count
    job_id = job_result.job_id
    job_pk = job_result.pk

    subject, from_email, to = '"ndna_automation" Job Has Executed on %s devices on the NEURAL Server by %s' %(job_count, username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = '"ndna_automation" with job ID %s and UUID %s Has Executed on NEURAL Server by %s.\n\nLog into NEURAL @ https://neural.domainname.com to check the logs and get more specific job results, status and reports.\n\nYou can also view the summary results at the following link without logging in\nhttps://neural.domainname.com/automation_results/%s\n\nYou can also view the complete output at the following link (login required)\nhttps://neural.domainname.com/full_automation_results/%s\n\nSee below for a list of nodes:\n\n%s' %(job_pk, job_id, username, job_pk, job_pk, nodes_list)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()

#################################################################################################
def unique_write_files_net_connect(username, command_sleep, node, config, task_name, job_result):
    """ aquire a thread lock """
    sema.acquire()
    timeis = datetime.datetime.now()
    current_time = timeis.strftime("%m-%d-%Y-%H:%M")

    # THIS NEEDS TO BE UPDATED ON ALL WRITE FILES TO BE TAILORED INTO THE USERS DIRECTORY!
    file_name = './configs/' + username + '/' + node + '_' + current_time + '_' + username + '_unique.txt'
    fo = open(file_name, "w")

    #Calling the SSH function
    """ svcacct_username is used to connect to the network """
    svcacct_username = 'svcacct-netbrains'
    svcacct_password = svcacct.objects.filter(username='svcacct-netbrains')
    for p in svcacct_password:
        password = p.password

        """ Call the Network Connection Sub Class Method and write the return results to flat files for each node """
        neural_net = neural_network_conn_sub_classes()
        neural_net_connect_output = neural_net.open_unique_network_connection(username, svcacct_username, password, command_sleep, node, config, task_name, job_result)
        fo.write(neural_net_connect_output)
        time.sleep(0.5)
        fo.close()

        if job_result.output == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.output = ''
        else:
            pass

        # write ssh func return data to database object called output, appending data each time for each node loop
        job_result.output = job_result.output + '\n\n*****Node Output*****'

        # combine both vars, e.g. keep building dataset of output config files to write to the sql db
        job_result.output += neural_net_connect_output
        job_result.save()

        """ new release the thread """
        time.sleep(2)
        sema.release()
        #print(neural_net_connect_output) # This allows viewing to debug in the rqworker terminal

@job('default', timeout=3000)
def unique_automation_ssh_entry_point(username, command_sleep, node_config, job_result):
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()
    task_name = 'self_service_unique_automation'

    for node, config in node_config.items():
        th = threading.Thread(target = unique_write_files_net_connect, args = (username, command_sleep, node, config, task_name, job_result))
        time.sleep(2)
        th.start()
    
    current_thread = threading.currentThread()
    time.sleep(0.2)
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()

    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()

    job_count = job_result.total_device_count
    job_id = job_result.job_id

    job_pk = job_result.pk
    li = list(node_config.keys())

    subject, from_email, to = '"unique_automation" Job Has Executed on %s devices on the NEURAL Server by %s' %(job_count, username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = '"unique_Automation" with job ID %s and UUID %s Job Has Executed on NEURAL Server by %s.\n\nLog into NEURAL @ https://neural.domainname.com to check the logs and get more specific job results, status and reports.\n\nYou can also view the summary results at the following link without logging in\nhttps://neural.domainname.com/automation_results/%s\n\nYou can also view the complete output at the following link (login required)\nhttps://neural.domainname.com/full_automation_results/%s\n\nSee below for a list of nodes:\n\n%s' %(job_pk, job_id, username, job_pk, job_pk, li)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
#################################################################################################
#################################################################################################
def ad_hoc_unique_write_files_net_connect(username, command_sleep, node, config, task_name, job_result):
    """ aquire a thread lock """
    sema.acquire()
    timeis = datetime.datetime.now()
    current_time = timeis.strftime("%m-%d-%Y-%H:%M")

    # THIS NEEDS TO BE UPDATED ON ALL WRITE FILES TO BE TAILORED INTO THE USERS DIRECTORY!
    file_name = './configs/' + username + '/' + node + '_' + current_time + '_' + username + '_unique.txt'
    fo = open(file_name, "w")

    #Calling the SSH function
    """ svcacct_username is used to connect to the network """
    svcacct_username = 'svcacct-netbrains'
    svcacct_password = svcacct.objects.filter(username='svcacct-netbrains')
    for p in svcacct_password:
        password = p.password

        """ Call the Network Connection Sub Class Method and write the return results to flat files for each node """
        neural_net = neural_network_conn_sub_classes()
        neural_net_connect_output = neural_net.open_ad_hoc_unique_network_connection(username, svcacct_username, password, command_sleep, node, config, task_name, job_result)
        fo.write(neural_net_connect_output)
        time.sleep(0.5)
        fo.close()

        if job_result.output == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.output = ''
        else:
            pass

        # write ssh func return data to database object called output, appending data each time for each node loop
        job_result.output = job_result.output + '\n\n*****Node Output*****'

        # combine both vars, e.g. keep building dataset of output config files to write to the sql db
        job_result.output += neural_net_connect_output
        job_result.save()

        """ new release the thread """
        time.sleep(2)
        sema.release()
        #print(neural_net_connect_output) # This allows viewing to debug in the rqworker terminal

@job('default', timeout=3000)
def ad_hoc_unique_automation_ssh_entry_point(username, command_sleep, node_config, job_result):
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()
    task_name = 'ad_hoc_unique_automation'

    for node, config in node_config.items():
        th = threading.Thread(target = ad_hoc_unique_write_files_net_connect, args = (username, command_sleep, node, config, task_name, job_result))
        time.sleep(2)
        th.start()
    
    current_thread = threading.currentThread()
    time.sleep(0.2)
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()

    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()

    job_count = job_result.total_device_count
    job_id = job_result.job_id

    job_pk = job_result.pk
    li = list(node_config.keys())

    subject, from_email, to = '"unique_automation" Job Has Executed on %s devices on the NEURAL Server by %s' %(job_count, username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = '"unique_Automation" with job ID %s and UUID %s Job Has Executed on NEURAL Server by %s.\n\nLog into NEURAL @ https://neural.domainname.com to check the logs and get more specific job results, status and reports.\n\nYou can also view the summary results at the following link without logging in\nhttps://neural.domainname.com/automation_results/%s\n\nYou can also view the complete output at the following link (login required)\nhttps://neural.domainname.com/full_automation_results/%s\n\nSee below for a list of nodes:\n\n%s' %(job_pk, job_id, username, job_pk, job_pk, li)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
#################################################################################################
#################################################################################################
def manual_unique_write_files_net_connect(username, command_sleep, node, config, task_name, job_result):
    """ aquire a thread lock """
    sema.acquire()
    timeis = datetime.datetime.now()
    current_time = timeis.strftime("%m-%d-%Y-%H:%M")

    # THIS NEEDS TO BE UPDATED ON ALL WRITE FILES TO BE TAILORED INTO THE USERS DIRECTORY!
    file_name = './configs/' + username + '/' + node + '_' + current_time + '_' + username + '_unique.txt'
    fo = open(file_name, "w")

    #Calling the SSH function
    """ svcacct_username is used to connect to the network """
    svcacct_username = 'svcacct-netbrains'
    svcacct_password = svcacct.objects.filter(username='svcacct-netbrains')
    for p in svcacct_password:
        password = p.password

        """ Call the Network Connection Sub Class Method and write the return results to flat files for each node """
        neural_net = neural_network_conn_sub_classes()
        neural_net_connect_output = neural_net.open_manual_unique_network_connection(username, svcacct_username, password, command_sleep, node, config, task_name, job_result)
        fo.write(neural_net_connect_output)
        time.sleep(0.5)
        fo.close()

        if job_result.output == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.output = ''
        else:
            pass

        # write ssh func return data to database object called output, appending data each time for each node loop
        job_result.output = job_result.output + '\n\n*****Node Output*****'

        # combine both vars, e.g. keep building dataset of output config files to write to the sql db
        job_result.output += neural_net_connect_output
        job_result.save()

        """ new release the thread """
        time.sleep(2)
        sema.release()
        #print(neural_net_connect_output) # This allows viewing to debug in the rqworker terminal

@job('default', timeout=3000)  
def manual_unique_automation_ssh_entry_point(username, command_sleep, node_config, job_result):
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()
    task_name = 'self_service_unique_automation'

    for node, config in node_config.items():
        th = threading.Thread(target = manual_unique_write_files_net_connect, args = (username, command_sleep, node, config, task_name, job_result))
        time.sleep(2)
        th.start()
    
    current_thread = threading.currentThread()
    time.sleep(0.2)
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()

    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()

    job_count = job_result.total_device_count
    job_id = job_result.job_id

    job_pk = job_result.pk
    li = list(node_config.keys())

    subject, from_email, to = '"unique_automation" Job Has Executed on %s devices on the NEURAL Server by %s' %(job_count, username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = '"unique_Automation" with job ID %s and UUID %s Job Has Executed on NEURAL Server by %s.\n\nLog into NEURAL @ https://neural.domainname.com to check the logs and get more specific job results, status and reports.\n\nYou can also view the summary results at the following link without logging in\nhttps://neural.domainname.com/automation_results/%s\n\nYou can also view the complete output at the following link (login required)\nhttps://neural.domainname.com/full_automation_results/%s\n\nSee below for a list of nodes:\n\n%s' %(job_pk, job_id, username, job_pk, job_pk, li)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
##################################################################################################################################
##################################################################################################################################
#Open SSHv2 connection to devices
#@retry(wait_fixed=2000, stop_max_attempt_number=2) If you use, note, your db writes and progress bar might not be accurate
def unique_fw_network_connection(username, svcacct_username, password, command_sleep, pcapname, t3pass, node, command, job_result):
    node_output = ''
    try:
        paramiko.util.log_to_file("./logs/paramiko.log")   
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(node, username = svcacct_username, password = password, look_for_keys=False)
        connection = session.invoke_shell()	
        OS = Device.objects.filter(hostname = node).order_by().values_list('OS', flat=True).distinct()
        OS_STR = ''.join(OS)
        if OS_STR == 'SDWAN-IOS' or OS_STR == 'IOS' or OS_STR == 'IOS-XE' or OS_STR == 'IOS-XR' \
            or OS_STR == 'NXOS' or OS_STR == 'NX-OS' or OS_STR == 'AVI' or OS_STR == 'Arista':
            connection.send("term len 0\n")
            time.sleep(2)
        elif OS_STR == 'ASA':
            connection.send("term pager 0\n")
            time.sleep(2)
        elif OS_STR == 'JUNOS':
            connection.send("set cli screen-length 0\n")
            time.sleep(2)
        elif OS_STR == 'PALO-ALTO':
            connection.send("set cli pager off\n")
            time.sleep(2)
        elif OS_STR == 'ARUBA':
            connection.send("no paging\n")   
            time.sleep(2)       
        elif OS_STR == 'CHECKPOINT':
            connection.send("set clienv rows 0\n") 
            time.sleep(2) 
        elif OS_STR == 'ALCATEL':
            connection.send("environment no more\n") 
            time.sleep(2) 
        """ send tcpdump command to start the capture """
        connection.send(command)
        connection.send('\n')        
        time.sleep(command_sleep)

        """ send ctrl c to stop tcpdump """
        connection.send(chr(3))

        """ transfer the capture, and deal w/ host key as needed with conditional and channel.recv customizations """
        connection.send('scp %s T3@neural.domainname.com:\n' %pcapname)
        time.sleep(10)
        node_output = connection.recv(65535)       
        node_output = node_output.decode("utf-8", errors="ignore")
        time.sleep(5)

        if re.search(r"The authenticity", node_output):
            connection.send('yes\n')
            time.sleep(3)
            connection.send('%s\n' %t3pass)
            time.sleep(120)
            connection.send("exit\n") # Not needed due to session.close() method
            node_output2 = connection.recv(65535)
            node_output2 = node_output2.decode("utf-8", errors="ignore")
            node_output += node_output2
        else:
            connection.send('%s\n' %t3pass)
            time.sleep(120)
            connection.send("exit\n") # Not needed due to session.close() method
            node_output2 = connection.recv(65535)
            node_output2 = node_output2.decode("utf-8", errors="ignore")
            node_output += node_output2

        if re.search(r"command not found", node_output):
            completed_message = "There was at least one syntax error on FW device %s" % node
        else:
            completed_message = "* Completed device %s" % node
        
        log = Log(target=node, task="ad_hoc_fw_tcpdump", status="No Exception Raised", time=datetime.datetime.now(), messages=completed_message, user=username, job_result=job_result)
        log.save()

        #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
        time.sleep(0.5)
        job_result.completed_device_count += 1
        job_result.save()

        if job_result.messages == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.messages = ''
        else:
            pass
        job_result.messages += completed_message + '\n'
        job_result.save()

    except Exception as e:
        log = Log(target=node, task="ad_hoc_fw_tcpdump", status="Exception Raised", time=datetime.datetime.now(), messages=e, user='%s' % username)
        log.save()
        
        #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
        time.sleep(0.5)
        job_result.failed_device_count += 1
        job_result.save()


        if job_result.messages == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.messages = ''
        else:
            pass
        job_result.messages += str(e) + ' on target node ' + node + '\n'
        job_result.save()

    finally:
        if session:
            session.close()

    return node_output

def write_files_unique_fw(username, command_sleep, node, command, pcapname, t3pass, job_result):
    """ aquire a thread lock """
    sema.acquire()
    #Calling the SSH function
    """ svcacct_username is used to connect to the network """
    svcacct_username = 'svcacct-netbrains'
    svcacct_password = svcacct.objects.filter(username='root')
    for p in svcacct_password:
        password = p.password

        node_output = unique_fw_network_connection(username, svcacct_username, password, command_sleep, pcapname, t3pass, node, command, job_result)
        ##fo.write(node_output)
        #time.sleep(0.5)
        ##fo.close()

        if job_result.output == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.output = ''
        else:
            pass
        # write ssh func return data to database object called output, appending data each time for each node loop
        job_result.output = job_result.output + '\n\n*****Node Output*****\n\n'

        # combine both vars, e.g. keep building dataset of output config files to write to the sql db
        job_result.output += node_output
        job_result.save()

        """ new aquire a thread lock --> put just before print(node_output) """
        time.sleep(2)
        sema.release()
        #print(node_output) # This allows viewing to debug in the rqworker terminal
###################################################
""" AUTOMATION TCPDUMP SUPPORTING MULTIPLE Nodes/Unique Automation """
@job('default', timeout=3000)  
def fw_automation_unique_command_per_fw_entry_point(username, nodes_list, command_list, command_sleep, pcapname, t3pass, job_result):
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()

    dict = {'nodes_list': nodes_list, 'command_list': command_list, 'pcapname': pcapname}
    df = pd.DataFrame(dict)
    df.to_csv('./tcpdump/tcpdump_vars.csv')
    time.sleep(2)

    df_read = pd.read_csv("./tcpdump/tcpdump_vars.csv")  

    for i in df_read.itertuples():
        a=i.nodes_list
        b=i.command_list
        c=i.pcapname
        th = threading.Thread(target = write_files_unique_fw, args = (username, command_sleep, a, b, c, t3pass, job_result))
        time.sleep(2)
        th.start()

    """ new code """
    current_thread = threading.currentThread()
    time.sleep(0.2)
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()
    """ new  code """

    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()

    job_count = job_result.total_device_count
    job_id = job_result.job_id

    job_pk = job_result.pk

    """ move the capture to the application directory for web based access """
    move_pcaps = r"""
    mv /home/T3/*pcap ./tcpdump/pcaps
    """
    subprocess.Popen(move_pcaps, shell=True, stdout=subprocess.PIPE)
    time.sleep(5)

    subject, from_email, to = '"tcpdump_automation" Job Has Executed on %s devices on the NEURAL Server by %s' %(job_count, username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = '"tcpdump_automation" with job ID %s and UUID %s Has Executed on the NEURAL Server by %s. \n\nLog into NEURAL @ https://neural.domainname.com to check the logs and get more specific job results, status and reports.\n\nYou can also view the summary results at the following link without logging in\nhttps://neural.domainname.com/fw_automation_results/%s\n\nSee below for a list of nodes:\n\n%s' %(job_pk, job_id, username, job_pk, nodes_list)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
####################################################################################################
# Weekly db backup using cron job --> rqscheduler http://x.x.x.x:8000/admin/scheduler/cronjob/
@job('default')
def django_backup():
    COMMAND1 = r"""
    cd /var/www/django_app/mysite/
    python3 manage.py dbbackup
    sleep 10
    python3 manage.py mediabackup
    sleep 10
    """
    subprocess.Popen(COMMAND1, shell=True, stdout=subprocess.PIPE)
    time.sleep(10)

    subject, from_email, to = '"Neural Server Backup" Job Has Executed', 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = '"Neural Server Weekly Backup" Job Has Executed on the NEURAL Server.'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()

""" run every two weeks clean up server backups and paramiko log """
@job('default')
def django_clean_backups():
    COMMAND1 = r"""
    cd /var/www/django_app/django_db_backups/
    rm *
    sleep 10
    cd /var/www/django_app/mysite/logs/
    rm *
    """
    subprocess.Popen(COMMAND1, shell=True, stdout=subprocess.PIPE)
    time.sleep(10)

    subject, from_email, to = '"Neural Server Bi-Monthly Clean Backups Dir" Job Has Executed', 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = '"Neural Server Bi-Monthly Clean Backups Dir" Job Has Executed on the NEURAL Server.'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()

""" run every month - clean out logs, job results, bw-sla's db records: Keep last three months worth """
@job('low')
def django_clean_db():
    now = datetime.datetime.now()
    #remove_three_months_old_log_records = Log.objects.filter(time__range=[now - datetime.timedelta(days=365), now - datetime.timedelta(days=90)], target__regex=r'.*').count()
    remove_three_months_old_log_records = Log.objects.filter(time__range=[now - datetime.timedelta(days=365), now - datetime.timedelta(days=90)], target__regex=r'.*').delete()

    #remove_three_months_old_jobresult_records = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=365), now - datetime.timedelta(days=90)], user__regex=r'.*').count()
    remove_three_months_old_jobresult_records = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=365), now - datetime.timedelta(days=90)], user__regex=r'.*').delete()

    #remove_three_monthss_old_bwsla_records = BwSlaJobResult.objects.filter(time__range=[now - datetime.timedelta(days=365), now - datetime.timedelta(days=90)], src_to_dst_site__regex=r'.*').count()
    remove_three_months_old_bwsla_records = BwSlaJobResult.objects.filter(time__range=[now - datetime.timedelta(days=365), now - datetime.timedelta(days=90)], src_to_dst_site__regex=r'.*').delete()

    subject, from_email, to = '"Neural Server Monthly DataBase Cleanup" Job Has Executed', 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = '"Neural Server Monthly DataBase Cleanup" Job Has Executed on the NEURAL Server.'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()

######### NDNA IOS Update Inventory function
check_sql = True
def sql_connection_full(command, values):
    #Define SQL connection parameters
    sql_host = 'localhost'
    sql_username = 'root'
    sql_password = 'neural123'    
    sql_database = 'djangodb'
    #Connecting and writing to database
    try:
        sql_conn = mdb.connect(sql_host, sql_username, sql_password, sql_database)
        cursor = sql_conn.cursor()
        cursor.execute("USE djangodb")
        cursor.execute(command, values)
        #Commit changes
        sql_conn.commit()
    except Exception as e:
        log = Log(target=sql_db, task="self_service_ios_inventory", status="Exception Raised", time=datetime.datetime.now(), messages=e, user='%s' % username)
        log.save()
##################################
#@retry(wait_fixed=2000, stop_max_attempt_number=2) If you use, note, your db writes and progress bar might not be accurate
def open_network_connection_ios_inventory(username, svcacct_username, password, node, job_result):
    global check_sql
    node_output = ''
    try:
        paramiko.util.log_to_file("./logs/paramiko.log")   
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(node, username = svcacct_username, password = password, look_for_keys=False)
        connection = session.invoke_shell()	
        #Setting terminal length for entire output - disable pagination
        connection.send("terminal length 0\n")
        time.sleep(7)
        #Time length to deal with 37xx and 38xx switch stack bugs
        connection.send("show run | in hostname\n")
        time.sleep(32)
                
        #Reading commands from within the script
        #Using the "\" line continuation character for better readability of the commands to be sent
        selected_cisco_commands = '''show version | include , Version|uptime is|bytes of memory|Hz&\
                                  show inventory&\
                                  dir&\
                                  show ip int brief | include Eth|Fast|Giga|Te|Vlan&'''
                                  
        #Splitting commands by the "&" character
        command_list = selected_cisco_commands.split("&")
        #Writing each line in the command string to the device
        for each_line in command_list:
            connection.send(each_line + '\n')
            time.sleep(5)
#############################################################
        # Get around the 64K bytes (65535). paramiko limitation
        interval = 0.1
        maxseconds = 16
        maxcount = maxseconds / interval
        bufsize = 65535
        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        node_output = ''
        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode("utf-8", errors="ignore")
                node_output += data
            if connection.exit_status_ready():
                break
            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())
            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break
            rbuffer = node_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            node_output += data.decode("utf-8", errors="ignore")
#############################################################
        if re.search(r"% Invalid input detected at", node_output):
            completed_message = "There was at least one IOS syntax error on device %s" % node
        elif re.search(r"% Authorization failed", node_output):
            completed_message = "** Authorization failed for %s Looks Like a TACACS issue" % node
        else:
            completed_message = "* Inventory Information extracted from %s" % node
        
        log = Log(target=node, task="self_service_ios_inventory", status="No Exception Raised", time=datetime.datetime.now(), messages=completed_message, user=username, job_result=job_result)
        log.save()

        dev_os = re.search(r"\), Version (.+)", node_output)
        os = dev_os.group(1)

        dev_image_name = re.search(r" \((.+)\), Version", node_output)
        image_name = dev_image_name.group(1)

        local_hostname = re.search(r"hostname (.+)", node_output)
        hostname = local_hostname.group(1)

        serial_no_group = re.search(r"SN: (.+)", node_output)
        serial_no = serial_no_group.group(1)
        
        dev_flash = re.search(r"(.+ bytes total)", node_output)
        flash = dev_flash.group(1)

        Local_IPs = re.findall(r"Ethernet[0-9].+ ([1-9].+[0-9])", node_output)
        Local_IPs_var = ' | '.join(Local_IPs)

        Local_SVI_IPs = re.findall(r"Vlan[0-9].+ ([1-9].+[0-9])", node_output)
        Local_SVI_IPs_var = ' | '.join(Local_SVI_IPs)
#######################################################
        #NON-TRUCATED DB - first create if doesn't exist
        sql_connection_full("REPLACE INTO neural_ndnaiosdevice(Hostname,Local_IPs,Local_SVI_IPs,IOS_Image,IOSVersion,Flash,SerialNo) VALUES(%s, %s, %s, %s, %s, %s, %s)", (hostname, Local_IPs_var, Local_SVI_IPs_var, image_name, os, flash, serial_no))
#######################################################
        #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
        time.sleep(0.5)
        job_result.completed_device_count += 1
        job_result.save()

        if job_result.messages == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.messages = ''
        else:
            pass
        job_result.messages += completed_message + '\n'
        job_result.save()

    except Exception as e:
        log = Log(target=node, task="self_service_ios_inventory", status="Exception Raised", time=datetime.datetime.now(), messages=e, user='%s' % username)
        log.save()
        
        #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
        time.sleep(0.5)
        job_result.failed_device_count += 1
        job_result.save()

        if job_result.messages == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.messages = ''
        else:
            pass
        job_result.messages += str(e) + ' on target node ' + node + '\n'
        job_result.save()

    finally:
        if session:
            session.close()

    return node_output

#@retry(wait_fixed=2000, stop_max_attempt_number=2) If you use, note, your db writes and progress bar might not be accurate
def write_files_ios_inventory(username, node, job_result):
    """ aquire a thread lock """
    sema.acquire()
    timeis = datetime.datetime.now()
    current_time = timeis.strftime("%m-%d-%Y-%H:%M")
    # THIS NEEDS TO BE UPDATED ON ALL WRITE FILES TO BE TAILORED INTO THE USERS DIRECTORY!
    file_name = './configs/' + username + '/' + node + '_' + current_time + '_' + username + '_ios_inventory.txt'
    fo = open(file_name, "w")
    #Calling the SSH function
    """ svcacct_username is used to connect to the network """
    svcacct_username = 'svcacct-netbrains'
    svcacct_password = svcacct.objects.filter(username='svcacct-netbrains')
    for p in svcacct_password:
        password = p.password
        node_output = open_network_connection_ios_inventory(username, svcacct_username, password, node, job_result)
        fo.write(node_output)
        time.sleep(0.5)
        fo.close()

        if job_result.output == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.output = ''
        else:
            pass
        # write ssh func return data to database object called output, appending data each time for each node loop
        job_result.output = job_result.output + '\n\n*****Node Output*****'

        # combine both vars, e.g. keep building dataset of output config files to write to the sql db
        job_result.output += node_output
        job_result.save()

        """ new aquire a thread lock --> normally put after print(node_output) """
        time.sleep(2)
        sema.release()
        #print(node_output) # This allows viewing to debug in the rqworker terminal

########### IOS Inventory updates to NDNA DATABASE ################
@job('default', timeout=1500)
def ios_inventory_ssh_entry_point(username, nodes_list, job_result):
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()
    ##threads = []
    for node in nodes_list:
        th = threading.Thread(target = write_files_ios_inventory, args = (username, node, job_result))
        th.start()

    """ new code """
    current_thread = threading.currentThread()
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()

    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()

    job_count = job_result.total_device_count
    job_id = job_result.job_id
    job_pk = job_result.pk

    subject, from_email, to = '"NDNA IOS Inventory Update" Job Has Executed on %s devices on the NEURAL Server by %s' %(job_count, username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = 'NDNA IOS Inventory Update with job ID %s and UUID %s Has Executed by %s. \n\nLog into NEURAL @ https://neural.domainname.com to check the logs and get more specific job results, status and reports.\n\nYou can also view the summary results at the following link without logging in\nhttps://neural.domainname.com/automation_results/%s\n\nYou can also view the complete output at the following link (login required)\nhttps://neural.domainname.com/full_automation_results/%s\n\nSee below for a list of nodes:\n\n%s' %(job_pk, job_id, username, job_pk, job_pk, nodes_list)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
####################################################
######### NDNA NX-OS Update Inventory function ########
check_sql = True
def sql_connection_full_nxos(command, values):
    #Define SQL connection parameters
    sql_host = 'localhost'
    sql_username = 'root'
    sql_password = 'neural123'    
    sql_database = 'djangodb'
    #Connecting and writing to database
    try:
        sql_conn = mdb.connect(sql_host, sql_username, sql_password, sql_database)
        cursor = sql_conn.cursor()
        cursor.execute("USE djangodb")
        cursor.execute(command, values)
        #Commit changes
        sql_conn.commit()
    except Exception as e:
        log = Log(target=sql_db, task="self_service_nxos_inventory", status="Exception Raised", time=datetime.datetime.now(), messages=e, user='%s' % username)
        log.save()
##################################
##################################
#@retry(wait_fixed=2000, stop_max_attempt_number=2) If you use, note, your db writes and progress bar might not be accurate
def open_network_connection_nxos_inventory(username, svcacct_username, password, node, job_result):
    global check_sql
    node_output = ''
    try:
        paramiko.util.log_to_file("./logs/paramiko.log")   
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(node, username = svcacct_username, password = password, look_for_keys=False)
        connection = session.invoke_shell()	
        #Setting terminal length for entire output - disable pagination
        connection.send("terminal length 0\n")
        time.sleep(5)
        connection.send("show run | in switchname|hostname\n")
        time.sleep(5)
        selected_cisco_commands = '''show inventory&\
                                  dir&\
                                  sh ver | in version&\
                                  sh ver | in "cisco Nexus"&\
                                  sh ver | in image&\
                                  show ip int brief vrf management&\
                                  show ip int brief | include Eth|Fast|Giga|Te|Vlan&'''
                                                  
        #Splitting commands by the "&" character
        command_list = selected_cisco_commands.split("&")
        #Writing each line in the command string to the device
        for each_line in command_list:
            connection.send(each_line + '\n')
            time.sleep(5)
#############################################################
        # Get around the 64K bytes (65535). paramiko limitation
        interval = 0.1
        maxseconds = 16
        maxcount = maxseconds / interval
        bufsize = 65535
        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        node_output = ''
        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode("utf-8", errors="ignore")
                node_output += data
            if connection.exit_status_ready():
                break
            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())
            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break
            rbuffer = node_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            node_output += data.decode("utf-8", errors="ignore")
#############################################################
        if re.search(r"% Invalid command", node_output):
            completed_message = "* There was at least one NXOS syntax error on device %s" % node
        elif re.search(r"% Authorization failed", node_output):
            completed_message = "** Authorization failed for %s Looks Like a TACACS issue" % node
        else:
            completed_message = "* Inventory Information extracted from %s" % node
    
        log = Log(target=node, task="self_service_nxos_inventory", status="No Exception Raised", time=datetime.datetime.now(), messages=completed_message, user=username, job_result=job_result)
        log.save()

        dev_nxos = re.search(r"System version: (.+)", node_output)
        nxos = dev_nxos.group(1)

        nxosdev_vendor = re.search(r"cisco (.+) .hassis", node_output)
        nxos_platform = nxosdev_vendor.group(1)

        nxosdev_image_name = re.search(r"file is: (.+)", node_output)
        nxosimage_name = nxosdev_image_name.group(1)

        local_hostname = re.search(r"name (.+)", node_output)
        hostname = local_hostname.group(1)

        serial_no_group = re.search(r"SN: (.+)", node_output)
        serial_no = serial_no_group.group(1)
        
        dev_flash = re.search(r"(.+ bytes total)", node_output)
        flash = dev_flash.group(1)

        Local_IPs = re.findall(r"Ethernet[0-9].+ ([1-9].+[0-9])", node_output)
        Local_IPs_var = ' | '.join(Local_IPs)

        Local_SVI_IPs = re.findall(r"Vlan[0-9].+ ([1-9].+[0-9])", node_output)
        Local_SVI_IPs_var = ' | '.join(Local_SVI_IPs)

        Local_mgmt_IPs = re.findall(r"mgmt0.+ ([1-9].+[0-9])", node_output)
        Local_mgmt_IPs_var = ' | '.join(Local_mgmt_IPs)
#######################################################
        #NON-TRUCATED DB - first create if doesn't exist 
        sql_connection_full_nxos("REPLACE INTO neural_ndnanexusdevice(Hostname,Local_IPs,Local_SVI_IPs,Local_mgmt_IPs,NXOS_Platform,NXOS_Image,NXOSVersion,Flash,SerialNo) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (hostname, Local_IPs_var, Local_SVI_IPs_var, Local_mgmt_IPs_var, nxos_platform, nxosimage_name, nxos, flash, serial_no))
#######################################################
        #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
        time.sleep(0.5)
        job_result.completed_device_count += 1
        job_result.save()

        if job_result.messages == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.messages = ''
        else:
            pass
        job_result.messages += completed_message + '\n'
        job_result.save()

    except Exception as e:
        log = Log(target=node, task="self_service_nxos_inventory", status="Exception Raised", time=datetime.datetime.now(), messages=e, user='%s' % username)
        log.save()
        
        #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
        time.sleep(0.5)
        job_result.failed_device_count += 1
        job_result.save()

        if job_result.messages == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.messages = ''
        else:
            pass
        job_result.messages += str(e) + ' on target node ' + node + '\n'
        job_result.save()

    finally:
        if session:
            session.close()

    return node_output

""" this is related to nxos_inventory """
#@retry(wait_fixed=2000, stop_max_attempt_number=2) If you use, note, your db writes and progress bar might not be accurate
def write_files_nxos_inventory(username, node, job_result):
    """ aquire a thread lock """
    sema.acquire()

    timeis = datetime.datetime.now()
    current_time = timeis.strftime("%m-%d-%Y-%H:%M")

    # THIS NEEDS TO BE UPDATED ON ALL WRITE FILES TO BE TAILORED INTO THE USERS DIRECTORY!
    file_name = './configs/' + username + '/' + node + '_' + current_time + '_' + username + '_nxos_inventory.txt'
    fo = open(file_name, "w")

    #Calling the SSH function
    """ svcacct_username is used to connect to the network """
    svcacct_username = 'svcacct-netbrains'
    svcacct_password = svcacct.objects.filter(username='svcacct-netbrains')
    for p in svcacct_password:
        password = p.password
        node_output = open_network_connection_nxos_inventory(username, svcacct_username, password, node, job_result)
        fo.write(node_output)
        time.sleep(0.5)
        fo.close()

        if job_result.output == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.output = ''
        else:
            pass
        # write ssh func return data to database object called output, appending data each time for each node loop
        job_result.output = job_result.output + '\n\n*****Node Output*****'

        # combine both vars, e.g. keep building dataset of output config files to write to the sql db
        job_result.output += node_output
        job_result.save()

        """ new aquire a thread lock --> normally put after print(node_output) """
        time.sleep(2)
        sema.release()
        #print(node_output) # This allows viewing to debug in the rqworker terminal

########### NXOS Inventory updates to NDNA DATABASE ################
@job('default', timeout=1500)
def nxos_inventory_ssh_entry_point(username, nodes_list, job_result):
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()
    ##threads = []
    for node in nodes_list:
        th = threading.Thread(target = write_files_nxos_inventory, args = (username, node, job_result))
        th.start()

    """ new code """
    current_thread = threading.currentThread()
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()

    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()

    job_count = job_result.total_device_count
    job_id = job_result.job_id
    job_pk = job_result.pk

    subject, from_email, to = '"NDNA NX-OS Inventory Update" Job Has Executed on %s devices on the NEURAL Server by %s' %(job_count, username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = 'NDNA NX-OS Inventory Update with job ID %s and UUID %s Has Executed by %s. \n\nLog into NEURAL @ https://neural.domainname.com to check the logs and get more specific job results, status and reports.\n\nYou can also view the summary results at the following link without logging in\nhttps://neural.domainname.com/automation_results/%s\n\nYou can also view the complete output at the following link (login required)\nhttps://neural.domainname.com/full_automation_results/%s\n\nSee below for a list of nodes:\n\n%s' %(job_pk, job_id, username, job_pk, job_pk, nodes_list)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
###########################################################
from netmiko import Netmiko, ConnectHandler, file_transfer
###########################################################
# four hour job timeout due to long jobs - potentially very big configs to push!
@job('low', timeout=14400) 
def scp_file_upload(username, node, scpupload, remote_path, job_result):
    """ svcacct_username is used to connect to the network """
    svcacct_username = 'svcacct-netbrains'
    svcacct_password = svcacct.objects.filter(username='svcacct-netbrains')

    for p in svcacct_password:
        password = p.password

    """ start the job """
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()

    my_connection = ConnectHandler(
        host=node,
        username="svcacct-netbrains",
        password=password,
        device_type="cisco_ios",
    )
    my_connection.enable()

    my_transfer = file_transfer(
        my_connection,
        source_file='./scpfiles/%s' %scpupload,
        dest_file=scpupload,
        file_system=remote_path,
    )
    my_connection.disconnect()

    """  write the job as completed  """
    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()

# four hour job timeout due to long jobs - potentially very big configs to push!
@job('low', timeout=14400)
def scp_nxos_file_upload(username, node, scpupload, remote_path, job_result):
    """ svcacct_username is used to connect to the network """
    svcacct_username = 'svcacct-netbrains'
    svcacct_password = svcacct.objects.filter(username='svcacct-netbrains')

    for p in svcacct_password:
        password = p.password
    
    """ start the job """
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()

    my_connection = ConnectHandler(
        host=node,
        username="svcacct-netbrains",
        password=password,
        device_type="cisco_nxos",
    )
    my_connection.enable()

    my_transfer = file_transfer(
        my_connection,
        source_file='./scpfiles/%s' %scpupload,
        dest_file=scpupload,
        file_system=remote_path,
    )
    my_connection.disconnect()
    
    """  write the job as completed  """
    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()
##########################################################################################################
#Open SSHv2 connection to devices for compliance_check
#@retry(wait_fixed=2000, stop_max_attempt_number=2) If you use, note, your db writes and progress bar might not be accurate
def open_network_connection_compliance_check(username, svcacct_username, password, node, job_result):
    node_output = ''
    try:
        paramiko.util.log_to_file("./logs/paramiko.log")   
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(node, username = svcacct_username, password = password, look_for_keys=False)
        connection = session.invoke_shell()	
        connection.send("term len 0\n")
        time.sleep(3)
        connection.send("sh run\n")
        time.sleep(5)
#############################################################
        # Get around the 64K bytes (65535). paramiko limitation
        interval = 0.1
        maxseconds = 16
        maxcount = maxseconds / interval
        bufsize = 65535
        input_idx = 0
        timeout_flag = False
        start = datetime.datetime.now()
        start_secs = time.mktime(start.timetuple())
#############################################################
        node_output = ''
        while True:
            if connection.recv_ready():
                data = connection.recv(bufsize).decode("utf-8", errors="ignore")
                node_output += data
            if connection.exit_status_ready():
                break
            now = datetime.datetime.now()
            now_secs = time.mktime(now.timetuple())
            et_secs = now_secs - start_secs
            if et_secs > maxseconds:
                timeout_flag = True
                break
            rbuffer = node_output.rstrip(' ')
            if len(rbuffer) > 0 and (rbuffer[-1] == '#' or rbuffer[-1] == '>'): ## got a Cisco command prompt
                break
            time.sleep(0.200)
        if connection.recv_ready():
            data = connection.recv(bufsize)
            node_output += data.decode("utf-8", errors="ignore")
#############################################################
        if re.search(r"% Invalid input detected at", node_output):
            completed_message = "There was at least one IOS syntax error on device %s" % node
        elif re.search(r"% Invalid command at", node_output):
            completed_message = "There was at least one NX-OS syntax error on %s" % node
        elif re.search(r"% Authorization failed", node_output):
            completed_message = "** Authorization failed for %s Looks Like a TACACS issue" % node
        else:
            completed_message = "* Completed device %s" % node
        
        log = Log(target=node, task="self_service_compliance_check", status="No Exception Raised", time=datetime.datetime.now(), messages=completed_message, user=username, job_result=job_result)
        log.save()

        #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
        time.sleep(0.5)
        job_result.completed_device_count += 1
        job_result.save()

        if job_result.messages == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.messages = ''
        else:
            pass
        job_result.messages += completed_message + '\n'
        job_result.save()

    except Exception as e:
        log = Log(target=node, task="self_service_compliance_check", status="Exception Raised", time=datetime.datetime.now(), messages=e, user='%s' % username)
        log.save()
        
        #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
        time.sleep(0.5)
        job_result.failed_device_count += 1
        job_result.save()

        if job_result.messages == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.messages = ''
        else:
            pass
        job_result.messages += str(e) + ' on target node ' + node + '\n'
        job_result.save()

    finally:
        if session:
            session.close()

    return node_output
#############################################################
def write_files_compliance_check(username, node, job_result):
    """ aquire a thread lock """
    sema.acquire()
    timeis = datetime.datetime.now()
    current_time = timeis.strftime("%m-%d-%Y-%H:%M")

    # THIS NEEDS TO BE UPDATED ON ALL WRITE FILES TO BE TAILORED INTO THE USERS DIRECTORY!
    file_name = './golden_config_diffs/'+ node + '_compliance_check.txt'
    fo = open(file_name, "w")

    #Calling the SSH function
    """ svcacct_username is used to connect to the network """
    svcacct_username = 'svcacct-netbrains'
    svcacct_password = svcacct.objects.filter(username='svcacct-netbrains')
    for p in svcacct_password:
        password = p.password

        node_output = open_network_connection_compliance_check(username, svcacct_username, password, node, job_result)
        fo.write(node_output)
        time.sleep(0.5)
        fo.close()

        if job_result.output == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.output = ''
        else:
            pass

        # write ssh func return data to database object called output, appending data each time for each node loop
        job_result.output = job_result.output + '\n\n*****Node Output*****'

        # combine both vars, e.g. keep building dataset of output config files to write to the sql db
        job_result.output += node_output
        job_result.save()

        """ new aquire a thread lock --> put just before print(node_output) """
        time.sleep(2)
        sema.release()
        #print(node_output) # This allows viewing to debug in the rqworker terminal
##################################################################################################################################
""" this is related to compliance_check """
@job('default', timeout=1500)
def compliance_check_ssh_entry_point(username, nodes_list, job_result):
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()

    for node in nodes_list:
        th = threading.Thread(target = write_files_compliance_check, args = (username, node, job_result))
        th.start()

    """ new code """
    current_thread = threading.currentThread()
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()

    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()


    job_count = job_result.total_device_count
    job_id = job_result.job_id
    job_pk = job_result.pk

    subject, from_email, to = '"Single_Node_Compliance Check" Job has run on the NEURAL Server by %s' %(username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = 'Single Node Compliance Check Job Has Executed with job ID %s and UUID %s by %s.' %(job_pk, job_id, username)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
###########################################################################
def multi_node_write_files_compliance_check(device_platform, username, node, job_result):
    """ aquire a thread lock """
    sema.acquire()

    timeis = datetime.datetime.now()
    current_time = timeis.strftime("%m-%d-%Y-%H:%M")

    # THIS NEEDS TO BE UPDATED ON ALL WRITE FILES TO BE TAILORED INTO THE USERS DIRECTORY!
    file_name = './golden_config_diffs/'+ node + '_compliance_check.txt'
    fo = open(file_name, "w")

    #Calling the SSH function
    """ svcacct_username is used to connect to the network """
    svcacct_username = 'svcacct-netbrains'
    svcacct_password = svcacct.objects.filter(username='svcacct-netbrains')
    for p in svcacct_password:
        password = p.password

        node_output = open_network_connection_compliance_check(username, svcacct_username, password, node, job_result)
        fo.write(node_output)
        time.sleep(0.5)
        fo.close()

        if job_result.output == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.output = ''
        else:
            pass

        # write ssh func return data to database object called output, appending data each time for each node loop
        job_result.output = job_result.output + '\n\n*****Node Output*****'

        # combine both vars, e.g. keep building dataset of output config files to write to the sql db
        job_result.output += node_output
        job_result.save()

        """ new aquire a thread lock --> put just before print(node_output) """
        time.sleep(2)

        ########################################################################################################
        """ remove leading/trailing white space & CR/LF if exists, Remove !'s, and add newline to EOF of golden config if it doesn't exist """
        REMOVE_WHITESPACE_FROM_CFG_FILES = r"""
        sed -i 's/^ *//g' ./golden_configs/%s
        sed -i 's/^ *//g' ./golden_config_diffs/%s_compliance_check.txt
        sed -i 's/\r$//' ./golden_configs/%s
        sed -i 's/\r$//' ./golden_config_diffs/%s_compliance_check.txt
        sed -i 's/[[:space:]]*$//' ./golden_configs/%s
        sed -i 's/[[:space:]]*$//' ./golden_config_diffs/%s_compliance_check.txt
        sed -i -e '$a\' ./golden_configs/%s
        sed -i -e '$a\' ./golden_config_diffs/%s_compliance_check.txt

        sed -i 's/!//' ./golden_configs/%s
        """% (device_platform, node, device_platform, node, device_platform, node, device_platform, node, device_platform)

        subprocess.Popen(REMOVE_WHITESPACE_FROM_CFG_FILES, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)

        """ run diff and remove < from file and leading whitespace """
        RUNDIFF = r"""
        diff ./golden_configs/%s ./golden_config_diffs/%s_compliance_check.txt > ./tmp/%s_ooc.txt
        cat ./tmp/%s_ooc.txt | grep \< > ./tmp/%s_ooc_final.txt
        sed -i 's/<//' ./tmp/%s_ooc_final.txt 
        sed -i 's/^ *//g' ./tmp/%s_ooc_final.txt
        """% (device_platform, node, node, node, node, node, node)

        subprocess.Popen(RUNDIFF, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)
        ########################################################################################################

        # for diffs code to render in another form box
        diffs_pre_db = open('./tmp/%s_ooc_final.txt' %node, 'r').readlines()

        # initialize an empty string
        diff_str = " " 
        
        # return string  
        diffs_db = diff_str.join(diffs_pre_db)

        """ write to database """
        diffs_db_write=GoldenConfigDiffs.objects.create(config=diffs_db, device_platform=device_platform + '_' + node + '_' + current_time)
        diffs_db_write.save()

        """ read to database """
        diffs = GoldenConfigDiffs.objects.filter(device_platform=device_platform + '_' + node + '_' + current_time).values_list('config', flat=True)  

        for diff in diffs:
            job_result.messages += '\n============================================================\nThe following code is missing and out of compliance on node ' + node + '\n============================================================\n   *** If nothing is listed, The device is Compliant ***\n============================================================\n*** If there was an exception raised or for any reason, there was a\nfailure to obtain the running config, the full *golden* config will be listed below \n\n================Missing From Live Config====================\n' + diff + '\n=========End of Golden Config to Live Config Diff===========\n\n'
            job_result.save()

        time.sleep(2)
        sema.release()
        #print(node_output) # This allows viewing to debug in the rqworker terminal
##################################################################################################################################
""" this is related to compliance_check """
@job('default', timeout=1500)
def multi_node_compliance_check_ssh_entry_point(device_platform, username, nodes_list, job_result):
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()

    for node in nodes_list:
        th = threading.Thread(target = multi_node_write_files_compliance_check, args = (device_platform, username, node, job_result))
        th.start()

    """ new code """
    current_thread = threading.currentThread()
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()

    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()


    job_count = job_result.total_device_count
    job_id = job_result.job_id
    job_pk = job_result.pk

    subject, from_email, to = '"Multi Node Compliance Check" Job has run on the NEURAL Server by %s' %(username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = 'Multi Node Compliance Check Job Has Executed with job ID %s and UUID %s by %s.' %(job_pk, job_id, username)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()

from napalm import get_network_driver
import json
""" Custom Exception """
class NoValidVendorFound(Exception):
    """Raised when there's no vendor match error"""
    def __init__(self, msg):
        super().__init__(self, msg)

def napalm_get_func(username, node, svcacct_username, svcacct_password, get_var, vendor, job_result):
    try:
        if get_var == 'get_facts' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_facts()
            napalm_output = json.dumps(response, indent=4)

            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_environment' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_environment()
            napalm_output = json.dumps(response, indent=4)

            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_arp_table' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_arp_table()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_bgp_config' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_bgp_config()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_bgp_neighbors' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_bgp_neighbors()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_bgp_neighbors_detail' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_bgp_neighbors_detail()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_interfaces' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_interfaces()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_interfaces_counters' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_interfaces_counters()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_interfaces_ip' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_interfaces_ip()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_config' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_config()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_mac_address_table' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_mac_address_table()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_network_instances' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_network_instances()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_ntp_peers' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_ntp_peers()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_ntp_servers' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_ntp_servers()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_ntp_stats' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_ntp_stats()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_snmp_information' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_snmp_information()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'get_vlans' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.get_vlans()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()

        elif get_var == 'is_alive' and vendor != 'not_valid':
            driver = get_network_driver(vendor)
            connect_to_device = driver(node, svcacct_username,svcacct_password)
            connect_to_device.open()
            response = connect_to_device.is_alive()
            napalm_output = json.dumps(response, indent=4)
            
            log = Log(target=node, task="self_service_napalm_get_automation", status="No Exception Raised", time=datetime.datetime.now(), messages='napalm_get_job_completed', user=username, job_result=job_result)
            log.save()
            
            #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
            time.sleep(0.5)
            job_result.completed_device_count += 1
            job_result.save()

            if job_result.messages == None:
                # build an empty string on first loop or = below or += will fail due to NoneType
                job_result.messages = ''
            else:
                pass
            job_result.messages += napalm_output + '\n\n'
            job_result.save()
            
        else:
            raise NoValidVendorFound("Vendor OS Not Supported")

    except Exception as e:
        log = Log(target=node, task="self_service_napalm_get_automation", status="Exception Raised", time=datetime.datetime.now(), messages=e, user='%s' % username)
        log.save()

        #job_result.refresh_from_db() - do not use, breaks the accuracy of the writes. We just want to increment for each loop for each *node*
        time.sleep(0.5)
        job_result.failed_device_count += 1
        job_result.save()

        if job_result.messages == None:
            # build an empty string on first loop or = below or += will fail due to NoneType
            job_result.messages = ''
        else:
            pass
        job_result.messages += str(e) + ' on target node ' + node + '\n'
        job_result.save()

        #print(napalm_output) # for testing
    return napalm_output


##@retry(wait_fixed=2000, stop_max_attempt_number=2) If you use, note, your db writes and progress bar might not be accurate
def napalm_write_files(username, node, get_var, vendor, job_result):
    sema.acquire()
    timeis = datetime.datetime.now()
    current_time = timeis.strftime("%m-%d-%Y-%H:%M")
    file_name = './configs/' + username + '/' + node + '_' + current_time + '_' + username + '_self_service_napalm.txt'
    fo = open(file_name, "w")

    svcacct_username = 'svcacct-netbrains'
    svcacct_password_list = svcacct.objects.filter(username=svcacct_username).order_by().values_list('password', flat=True).distinct() 
    svcacct_password = ' '.join(svcacct_password_list)

    napalm_output = napalm_get_func(username, node, svcacct_username, svcacct_password, get_var, vendor, job_result)
    fo.write(napalm_output)   
    fo.close()
    if job_result.output == None:
        # build an empty string on first loop or = below or += will fail due to NoneType
        job_result.output = ''
    else:
        pass

    job_result.output = job_result.output + '\n\n'

    # combine both vars, e.g. keep building dataset of output config files to write to the sql db
    job_result.output += napalm_output
    job_result.save()

    """ new aquire a thread lock --> put just before print(node_output) """
    time.sleep(2)
    sema.release()
    #print(node_output) # This allows viewing to debug in the rqworker terminal


""" ["eos", "ios", "junos", "nxos_ssh"] """
@job('default', timeout=3000) 
def napalm_get_entry_point(username, nodes_list, get_var, job_result):
    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()

    for node in nodes_list:
        OS = Device.objects.filter(hostname = node).order_by().values_list('OS', flat=True).distinct()
        OS_STR = ''.join(OS)
        if OS_STR == 'SDWAN-IOS' or OS_STR == 'IOS' or OS_STR == 'IOS-XE':
            vendor = 'ios'
        elif OS_STR == 'NXOS' or OS_STR == 'NX-OS':
            vendor = 'nxos_ssh'
        elif OS_STR == 'JUNOS':
            vendor = 'junos'
        elif OS_STR == 'Arista':
            vendor = 'eos'
        else:
            vendor = 'not_valid'
        th = threading.Thread(target = napalm_write_files, args = (username, node, get_var, vendor, job_result))
        th.start()
    """ new code """
    current_thread = threading.currentThread()
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()

    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()

    job_count = job_result.total_device_count
    job_id = job_result.job_id

    job_pk = job_result.pk

    nodes_devices = [i for i in nodes_list]
 
    subject, from_email, to = '"self_service_napalm_get_automation" Job Has Executed on %s devices on the NEURAL Server by %s' %(job_count, username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = '"self_service_napalm_get_automation" with job ID %s and UUID %s Has Executed on the NEURAL Server by %s. \n\nLog into NEURAL @ https://neural.domainname.com to check the logs and get more specific job results, status and reports.\n\nYou can also view the summary results at the following link without logging in\nhttps://neural.domainname.com/full_automation_results/%s\n\nSee below for a list of nodes:\n\n%s' %(job_pk, job_id, username, job_pk, job_pk, nodes_devices)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
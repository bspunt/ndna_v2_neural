""" rq related """
import django_rq
import uuid
from django_rq import job

from django.db.models import Count, Q, Sum
import django_filters

from .models import *
from .models import svcacct

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
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

""" import neural net network super and sub classes """
from .neural_connection_classes import *

""" global variables """ 
#setup max number of threads for Semaphore method to use. create sema variable for open ssh function to use
max_worker_threads = 15
sema = threading.BoundedSemaphore(value=max_worker_threads)

def clear_out_network_config_backup_dir():
    COMMAND1 = r"""
    rm -r ./configs/svcacct-netbrains/network_configs/*  
    """
    subprocess.Popen(COMMAND1, shell=True, stdout=subprocess.PIPE)
    time.sleep(10)


""" this is related to weekly config backups automation """
########################################################################################
""" this is related to weekly config backups for Cisco, Juniper, and Arista or any other vendor can be coded in """
#@retry(wait_fixed=2000, stop_max_attempt_number=2) If you use, note, your db writes and progress bar might not be accurate
def write_files_config_backups_call_net_connect(username, command_sleep, node, task_name, job_result):
    """ aquire a thread lock """
    sema.acquire()
    timeis = datetime.datetime.now()
    current_time = timeis.strftime("%m-%d-%Y-%H:%M")

    file_name = './configs/' + username + '/network_configs/' + node + '_' + current_time + '_network_config.txt'
    fo = open(file_name, "w")

    """ svcacct_username is used to connect to the network """
    svcacct_username = 'svcacct-netbrains'
    svcacct_password = svcacct.objects.filter(username='svcacct-netbrains')
    for p in svcacct_password:
        password = p.password

        """ Call the Network Connection Super Class Method and write the return results to flat files for each node """
        neural_net = neural_network_conn_super_class()
        neural_net_connect_output = neural_net.open_config_backups_network_connection(username, svcacct_username, password, command_sleep, node, task_name, job_result)
        fo.write(neural_net_connect_output)
        time.sleep(2)
        fo.close()
        ###################################################
        """ don't write output to database, since it's allot of data and will be written to individual files anyway """

        """ release the thread """
        time.sleep(2)
        sema.release()
        #print(neural_net_connect_output) # This allows viewing to debug in the rqworker terminal during development using the development server
########################################################################################
@job('low', timeout=3000)  
def weekly_config_backups():
    username = 'svcacct-netbrains'
    #nodes_list = Device.objects.all()

    """ build nodes list for all IOS, NXOS, EOS, ASA, JUNOS for config backups """
    nodes_list = Device.objects.filter(
    Q(OS ='NXOS') | Q(OS__icontains ='IOS') | Q(OS ='ASA') | Q(OS ='JUNOS') | Q(OS ='Arista') | Q(OS ='NX-OS')
    ).values_list('hostname', flat=True)

    task_name = 'self_service_config_backups'
    command_sleep = 5
    job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='self_service_config_backups', user='%s' % username, total_device_count=len(nodes_list))

    job_result.started = datetime.datetime.now()
    job_result.save()
    job_result.status='running'
    job_result.save()

    for node in nodes_list:
        th = threading.Thread(target = write_files_config_backups_call_net_connect, args = (username, command_sleep, node, task_name, job_result))
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

    subject, from_email, to = '"weekly_network_config_backups" Job (part 1) Has Executed on %s devices on the NEURAL Server by %s' %(job_count, username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = '"weekly_network_config_backups" with job ID %s and UUID %s Has Executed on the NEURAL Server by %s. \n\nLog into NEURAL @ https://neural.domainname.com to check the logs and get more specific job results, status and reports.\n\nYou can also view the summary results at the following link without logging in\nhttps://neural.domainname.com/backup_results/%s\n\nSee below for a list of nodes:\n\n%s' %(job_pk, job_id, username, job_pk, nodes_devices)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
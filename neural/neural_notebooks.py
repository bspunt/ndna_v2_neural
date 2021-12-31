##########################################################
""" neural_notebook_blueprint """
##########################################################
from django_rq import job
from .models import *
from retrying import retry
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

""" background worker.py """
from .background_worker import *

@job('default', timeout=1500)
def neural_notebook_test1(username, neural_notebook_vars, job_result):
    nodes_list = [] # NOT NEEDED....Just for readability to create space after defining the func :-)
    ############## update nodes lists per job, then combine them once per notebook - applies to all jobs ###############
    """ build list of nodes for each job from Django ORM SQL Query from 
    device inventory "source of truth" or you can build any type of Python list of nodes you'd like """
    nodes_list_job_1 = Device.objects.filter(device_type='test').order_by().values_list('hostname', flat=True)
    nodes_list_job_1 = list(nodes_list_job_1)

    nodes_list_job_2 = Device.objects.filter(device_type='test').order_by().values_list('hostname', flat=True)
    nodes_list_job_2 = list(nodes_list_job_2)

    """ this can be any type of flexible SQL query on the device inventory, e.g. below shows example of multiple options 
    for all leafs in the region EMEA """
    nodes_list_job_3 = Device.objects.filter(device_type='leaf', Region='EMEA').order_by().values_list('hostname', flat=True)
    nodes_list_job_3 = list(nodes_list_job_3)

    """ combine all job nodes_list vars into one variable for getting total length for progress bar in the web interface """
    nodes_list = nodes_list_job_1 + nodes_list_job_2   ### keep adding additional jobs to match the notebook

    """ get total nodes to write to the database for web progress bar to track """
    job_result.total_device_count=len(nodes_list)
    job_result.save()

    job_result.started = datetime.datetime.now()
    job_result.save()

    job_result.status='running'
    job_result.save()

    """ set this to the number in seconds you want in between commands sent to nodes using an integer """
    command_sleep = 1

    """ if no new vars are input in the web form interface, e.g. defined at runtime, use default variable values! """
    """ This will set the default variables/python list for all the jobs in the whole notebook! 
    which are then referenced by index in commands_list """
    if neural_notebook_vars == []:
        # vars index range =  0-5 for all jobs 
        """ default variables for all jobs starting from first to last task THESE STAY THE SAME THROUGH-OUT THE NOTEBOOK """
        neural_notebook_vars = [
        '914', 'testing notebook1', '10.19.3.1 255.255.255.0', 
        '915', 'testing notebook2', '10.19.4.2 255.255.255.0',]

############ job specific code to copy/paste/season-to-taste per job #############

######### below is what changes per job in the neural notebook as you build/ad new jobs to a notebook ############
    """ job 1 code start """
    task_name = 'self_service_neural_notebook_build_1stloop_on_router'

    command_list = [
    "conf t",
    "int loop%s" % neural_notebook_vars[0],
    "descript %s" % neural_notebook_vars[1],
    "ip address %s" % neural_notebook_vars[2],
    "end",
    "wr mem"]

    for node in nodes_list_job_1:
        th = threading.Thread(target = write_files_call_net_connect, args = (username, command_sleep, node, command_list, task_name, job_result))
        th.start()
############ above is what changes per job in notebook ###################
    """ clean up threads """
    current_thread = threading.currentThread()
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()

    """ job 1 code end """
##########################################################################

######### below is what changes per job in the neural notebook ############
    """ job 2 code start """
    task_name = 'self_service_neural_notebook_build_2ndloop_on_router'

    command_list = [
    "conf t",
    "int loop%s" % neural_notebook_vars[3],
    "descript %s" % neural_notebook_vars[4],
    "ip address %s" % neural_notebook_vars[5],
    "end",
    "wr mem"]

    for node in nodes_list_job_2:
        th = threading.Thread(target = write_files_call_net_connect, args = (username, command_sleep, node, command_list, task_name, job_result))
        th.start()
    ############ above is what changes per job in notebook ###################
    """ clean up threads """
    current_thread = threading.currentThread()
    for nonactive_thread in threading.enumerate():
        if nonactive_thread != current_thread:
            nonactive_thread.join()

    """ job 2 code end """
##########################################################################

##########################################################################
    """ after all jobs have run """
    job_result.status='completed'
    job_result.completed=datetime.datetime.now()
    job_result.save()

    job_count = job_result.total_device_count
    job_id = job_result.job_id
    job_pk = job_result.pk

    nodes_devices = [i for i in nodes_list]

    subject, from_email, to = '"notebook_test1" Job has run on %s devices on the NEURAL Server by %s' %(job_count, username), 'neural-no-reply@neural.domainname.com', 'notifications'
    text_content = 'notebook_test1 Job Has Executed with job ID %s and UUID %s by %s.\n\nLog into NEURAL @ https://neural.corpzone.internalzone.com to check the logs and get more specific job results, status and reports.\n\nYou can also view the summary results at the following link without logging in\nhttps://neural.corpzone.internalzone.com/automation_results/%s\n\nYou can also view the complete output at the following link (login required)\nhttps://neural.corpzone.internalzone.com/full_automation_results/%s\n\nSee below for a list of nodes:\n\n%s' %(job_pk, job_id, username, job_pk, job_pk, nodes_devices)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
###############################################################################
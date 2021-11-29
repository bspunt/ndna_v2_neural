## 
## ------------------------------------------------------------------
##     NDNAv2 codename: neural: 
##     Copyright (C) 2021  Brett M Spunt, CCIE No. 12745 (US Copyright No. TXu002-053-026)
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
## 
from retrying import retry
from .models import *

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
import MySQLdb as mdb

class neural_network_conn_super_class(object):
    def __init__(self):
        """ no class variables to initialize, possibly future use. 
            Using Classes to bundles methods/functions and reusing code/inheritance via sub-classes """

    """ ssh automation method """
    #@retry(wait_fixed=2000, stop_max_attempt_number=2) If you use, note, your db writes and progress bar might not be accurate, if 
    # run multiple times, e.g. if you run on 20 devices and have 2 auth failures, then retry and one of them succeeds, you'll have one extra 
    # failure write, e.g. your completed_device_count will be == 19 and your failure device count will be == 2 so it'll show a little OVER 100% on your progress bar, etc. 
    def open_network_connection(self, username, svcacct_username, password, command_sleep, node, command_list, task_name, job_result):
        node_output= ''
        try:
            paramiko.util.log_to_file("./logs/paramiko.log")   
            session = paramiko.SSHClient()
            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            session.connect(node, username = svcacct_username, password = password, look_for_keys=False)
            connection = session.invoke_shell()	
            #######################################################################
            """ disable pagination """
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
            """ keep adding additional for other vendors/other OSs as needed """

            """ note: each_line is an arbitrary value/variable created when writing this line of code """
            #Writing each line in the file to the device   
            for each_line in command_list:
                connection.send(each_line + '\n')
                time.sleep(command_sleep)
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
            """ keep adding in custom if for other vendors/other OSs as needed """
            if re.search(r"% Invalid input detected at", node_output):
                completed_message = "There was at least one IOS syntax error on device %s" % node
            elif re.search(r"% Invalid command at", node_output):
                completed_message = "There was at least one NX-OS syntax error on %s" % node
            elif re.search(r"% Authorization failed", node_output):
                completed_message = "** Authorization failed for %s Looks Like a TACACS issue" % node
            elif re.search(r"command not found", node_output):
                completed_message = "There was at least one syntax error on Linux device %s" % node
            else:
                completed_message = "* Completed device %s" % node

            log = Log(target=node, task=task_name, status="No Exception Raised", time=datetime.datetime.now(), messages=completed_message, user=username, job_result=job_result)
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
            log = Log(target=node, task=task_name, status="Exception Raised", time=datetime.datetime.now(), messages=e, user='%s' % username)
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

    """ ssh configs backups method """
    #@retry(wait_fixed=2000, stop_max_attempt_number=2) If you use, note, your db writes and progress bar might not be accurate, if 
    # run multiple times, e.g. if you run on 20 devices and have 2 auth failures, then retry and one of them succeeds, you'll have one extra 
    # failure write, e.g. your completed_device_count will be == 19 and your failure device count will be == 2 so it'll show a little OVER 100% on your progress bar, etc. 
    def open_config_backups_network_connection(self, username, svcacct_username, password, command_sleep, node, task_name, job_result):
        node_output= ''
        try:
            paramiko.util.log_to_file("./logs/paramiko.log")   
            session = paramiko.SSHClient()
            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            session.connect(node, username = svcacct_username, password = password, look_for_keys=False)
            connection = session.invoke_shell()	
            #######################################################################
            """ disable pagination, backup running config """
            OS = Device.objects.filter(hostname = node).order_by().values_list('OS', flat=True).distinct()
            OS_STR = ''.join(OS)
            if OS_STR == 'SDWAN-IOS' or OS_STR == 'IOS' or OS_STR == 'IOS-XE' or OS_STR == 'IOS-XR' \
                or OS_STR == 'NXOS' or OS_STR == 'NX-OS' or OS_STR == 'Arista':
                connection.send("term len 0\nshow run\n")
                time.sleep(4)
            elif OS_STR == 'ASA':
                connection.send("term pager 0\nshow run\n")
                time.sleep(4)
            elif OS_STR == 'JUNOS':
                connection.send("set cli screen-length 0\nshow configuration\n")
                time.sleep(4)
            """ keep adding additional for other vendors/other OSs as needed """
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
            """ keep adding in custom if for other vendors/other OSs as needed """
            if re.search(r"% Invalid input detected at", node_output):
                completed_message = "There was at least one IOS syntax error on device %s" % node
            elif re.search(r"% Invalid command at", node_output):
                completed_message = "There was at least one NX-OS syntax error on %s" % node
            elif re.search(r"% Authorization failed", node_output):
                completed_message = "** Authorization failed for %s Looks Like a TACACS issue" % node
            elif re.search(r"command not found", node_output):
                completed_message = "There was at least one syntax error on Linux device %s" % node
            else:
                completed_message = "* Completed device %s" % node

            """ don't want to write to log on good result, too many entries...will write to log on exception. JobResult will catch/write same result anyway """
            #log = Log(target=node, task=task_name, status="No Exception Raised", time=datetime.datetime.now(), messages=completed_message, user=username, job_result=job_result)
            #log.save()

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
            log = Log(target=node, task=task_name, status="Exception Raised", time=datetime.datetime.now(), messages=e, user='%s' % username)
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

""" unique and self service automation subclass utilizing parent/super class for ssh connections """
class neural_network_conn_sub_classes(neural_network_conn_super_class):
    def __init__(self):
        pass

    """ sending unique commands per device either for programming or pulling information from the network on an ad hoc basis """
    def open_ad_hoc_unique_network_connection(self, username, svcacct_username, password, command_sleep, node, config, task_name, job_result):
        command_list = open('./ad_hoc_unique/configs/%s/' % username + config).readlines()
        command_list = list(map(lambda x:x.strip(),command_list))
        return super().open_network_connection(username, svcacct_username, password, command_sleep, node, command_list, task_name, job_result)

    """ sending unique commands per device from configs created using the config generator program, for either for programming or pulling information from the network """
    def open_unique_network_connection(self, username, svcacct_username, password, command_sleep, node, config, task_name, job_result):
        command_list = open('./unique_automation/%s/' % username + config).readlines()
        command_list = list(map(lambda x:x.strip(),command_list))
        return super().open_network_connection(username, svcacct_username, password, command_sleep, node, command_list, task_name, job_result)

    """ sending unique commands per device from manually loaded configs either for programming or pulling information from the network """
    def open_manual_unique_network_connection(self, username, svcacct_username, password, command_sleep, node, config, task_name, job_result):
        command_list = open('./manual_configs/%s/' % username + config).readlines()
        command_list = list(map(lambda x:x.strip(),command_list))
        return super().open_network_connection(username, svcacct_username, password, command_sleep, node, command_list, task_name, job_result)
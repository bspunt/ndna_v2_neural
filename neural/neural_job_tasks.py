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
class neural_private_automation_task:
    def __init__(self, *args):
        self.username = ''

    def save_task_private(self, username, nodes_list, command_list, task_name):
        self.username = username
        self.nodes_list = nodes_list
        self.command_list = command_list
        self.task_name = task_name

        job_task_name = './job_task_names/' + username + '/' + task_name
        job_open_task_name = open(job_task_name, "w")
        job_open_task_name.close()

        nodes_file_task_name = './job_task_nodes_commands/' + username + '/nodes_file_' + task_name
        nodes_file_open_task_name = open(nodes_file_task_name, "w")

        for node in nodes_list:
            nodes_file_open_task_name.write("%s\n" % node)
            continue
        nodes_file_open_task_name.close()

        commands_file_task_name = './job_task_nodes_commands/' + username + '/commands_file_' + task_name
        commands_file_open_task_name = open(commands_file_task_name, "w")

        for command in command_list:
            commands_file_open_task_name.write("%s\n" % command)
            continue
        commands_file_open_task_name.close()


""" FUTURE SETUP FOR SYSTEM WIDE DYNAMIC SAVED JOB TASK """
class neural_public_automation_task:
    def __init__(self, *args):
        self.public = ''

    def save_task_public(self, public, nodes_list, command_list, task_name):
        self.public = public
        self.nodes_list = nodes_list
        self.command_list = command_list
        self.task_name = task_name

        nodes_file_task_name = './' + public + '/nodes_file_' + task_name
        nodes_file_open_task_name = open(nodes_file_task_name, "w")

        for node in nodes_list:
            nodes_file_open_task_name.write("%s\n" % node)
            continue
        nodes_file_open_task_name.close()

        commands_file_task_name = './' + public + '/commands_file_' + task_name
        commands_file_open_task_name = open(commands_file_task_name, "w")

        for command in command_list:
            commands_file_open_task_name.write("%s\n" % command)
            continue
        commands_file_open_task_name.close()
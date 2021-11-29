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
from django.db import models

# Create your models here.
####################################################
""" note: choices are only relevant to adding from the 
    admin interface, e.g. there's no restriction on device type, or vendor, and these options 
    can also be modified here to allow these options in the django admin interface """
class Device(models.Model):
    hostname = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    site = models.CharField(max_length=255)

    DEVICETYPE_CHOICES = (
        ('access', 'access'),
        ('distribution', 'distribution'),
        ('core', 'core'),
        ('spine', 'spine'),
        ('leaf', 'leaf'),
        ('sdwan_router', 'sdwan_router'),
        ('dmvpn_router', 'dmvpn_router'),
        ('mpls_router', 'mpls_router'),
        ('aws_router', 'aws_router'),
        ('edge_router', 'edge_router'),
        ('edge_switch', 'edge_switch'),
        ('firewall', 'firewall'),
        ('load_balancer', 'load_balancer'),
        ('vpn_concentrator', 'vpn_concentrator'),
        ('riverbed_wac', 'riverbed_wac'),
        ('ips', 'ips'),
        ('linux', 'linux'),
        ('mwg', 'mwg'),
    )
    device_type = models.CharField(max_length=255, choices=DEVICETYPE_CHOICES)

    VENDOR_CHOICES = (
        ('cisco', 'Cisco'),
        ('juniper', 'Juniper'),
        ('forcepoint', 'forcepoint'),
        ('riverbed', 'riverbed'),
        ('linux', 'linux'),
        ('mcafee', 'mcafee'),
    )
    vendor = models.CharField(max_length=255, choices=VENDOR_CHOICES)
    OS = models.CharField(max_length=255, null=True)
    Region = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.hostname
###################################################
class Log(models.Model):
    target = models.CharField(max_length=255)
    # put a refence, e.g. freeform or vxlan, edgeACL, L2_NDNA, etc
    task = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    # for grafana, not used in datatables
    time = models.DateTimeField(null=True)
    messages = models.CharField(max_length=255, blank=True)
    user = models.CharField(max_length=255, blank=True)
    # not used in datatables
    job_result = models.ForeignKey(to='JobResult', on_delete=models.CASCADE, null=True, blank=True)

    # used for grafana to use sum query
    counted = models.PositiveIntegerField(default='1', editable=False)

    def __str__(self):
        return "{} - {}".format(self.target, self.task)
###################################################
class JobResult(models.Model):
    job_id = models.UUIDField()
    user = models.CharField(max_length=255)

    # used to be called name
    job_name = models.CharField(max_length=255)
    output = models.TextField(null=True, blank=True)

    # this is used by me for converting to timestamp output config file names correctly
    started = models.TextField(null=True, blank=True)

    # x-check, but this is being used by django-rq
    created = models.DateTimeField(auto_now_add=True)

    # this is used by me for time series graphs w/ grafana/MySQL
    time = models.DateTimeField(auto_now_add=True)

    completed = models.TextField(null=True, blank=True)
    total_device_count = models.PositiveIntegerField(default=0)
    completed_device_count = models.PositiveIntegerField(default=0)
    failed_device_count = models.PositiveIntegerField(default=0)
    
    # used for grafana to use sum query
    counted = models.PositiveIntegerField(default='1', editable=False)

    # used displaying output to browser of device completed or syntax errors, e.g. same thing sending to log messages
    messages = models.TextField(null=True, blank=True)
    
    STATUS_CHOICES = (
        ('pending', 'Pending'), # left is internal, right is displayed to browser   - pending still sitting in queue
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('scheduled', 'Scheduled'),
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    def __str__(self):
        return "{}".format(self.job_id)

    @property
    def percent_finished_devices(self):
        if self.total_device_count == 0:
            return 0
        return (self.failed_device_count + self.completed_device_count) / self.total_device_count *100
###################################################
class Inventorie(models.Model):
    inventory_file_name = models.CharField(max_length=100)
    uploaded_by = models.CharField(max_length=100)
    inventory_csv = models.FileField(upload_to='inventoryfiles/')

    def __str__(self):
        return self.inventory_file_name

    def delete(self, *args, **kwargs):
        self.inventory_csv.delete()
        super().delete(*args, **kwargs)

class Configtemplate(models.Model):
    csv_file_name = models.CharField(max_length=100)
    uploaded_by = models.CharField(max_length=100)
    csv_variables = models.FileField(upload_to='csv_var_config_templates/')
    #jinja_template = models.FileField(upload_to='jinja2templates/')

    def __str__(self):
        return self.csv_file_name

    def delete(self, *args, **kwargs):
        self.csv_variables.delete()
        #self.jinja_template.delete()
        super().delete(*args, **kwargs)
class Jinjatemplate(models.Model):
    jinja_file_name = models.CharField(max_length=100)
    uploaded_by = models.CharField(max_length=100)
    jinja_template = models.FileField(upload_to='jinja2templates/')

    def __str__(self):
        return self.jinja_file_name

    def delete(self, *args, **kwargs):
        #self.csv_variables.delete()
        self.jinja_template.delete()
        super().delete(*args, **kwargs)
###################################################
class NDNANexusDevice(models.Model):
    Hostname = models.CharField(max_length=64, primary_key=True)
    Local_IPs = models.CharField(max_length=1000, null=True)
    Local_SVI_IPs = models.CharField(max_length=1000, null=True)
    Local_mgmt_IPs = models.CharField(max_length=1000, null=True)
    NXOS_Platform = models.CharField(max_length=1000, null=True)
    NXOS_Image = models.CharField(max_length=1000, null=True)
    NXOSVersion = models.CharField(max_length=1000, null=True)
    Flash = models.CharField(max_length=1000, null=True)
    SerialNo = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.Hostname
###################################################
class NDNAIOSDevice(models.Model):
    Hostname = models.CharField(max_length=64, primary_key=True)
    Local_IPs = models.CharField(max_length=1000, null=True)
    Local_SVI_IPs = models.CharField(max_length=1000, null=True)
    IOS_Image = models.CharField(max_length=1000, null=True)
    IOSVersion = models.CharField(max_length=1000, null=True)
    Flash = models.CharField(max_length=1000, null=True)
    SerialNo = models.CharField(max_length=1000, null=True)
    def __str__(self):
        return self.Hostname
###################################################
class NDNACDP(models.Model):
    Local_Hostname = models.CharField(max_length=1000, null=True)
    Remote_Platform = models.CharField(max_length=1000, null=True)
    Remote_cdp_neighbors = models.CharField(max_length=1000, null=True)
    local_intf_remote_intf = models.CharField(max_length=1000, null=True)
    def __str__(self):
        return self.Hostname
###################################################
""" grant add access for neural interface admin area of neural and/or views that only t3 should have access to """
class T3(models.Model):
    user = models.CharField(max_length=255)
    def __str__(self):
        return self.user
###################################################
""" grant add access for root only/admin only to db/media restore admin area of neural """
class root(models.Model):
    user = models.CharField(max_length=255)
    def __str__(self):
        return self.user
###################################################
""" supress cryptography support warnings """
import warnings 
warnings.filterwarnings(action='ignore',module='.*fernet_fields.*')

from fernet_fields import EncryptedTextField

""" neural svc account for ssh or REST API access to the network """
class svcacct(models.Model):
    username = models.CharField(max_length=255)
    password = EncryptedTextField()

    def __str__(self):
        return self.username
###################################################
class BwSlaJobResult(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    src_to_dst_site = models.TextField(null=True, blank=True)
    throughput_rate = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.time

    def __str__(self):
        return "{} _ {}".format(self.time, self.src_to_dst_site)
###################################################
class VRF(models.Model):
    vrf = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.vrf
###################################################
class SCP(models.Model):
    scp_file_name = models.CharField(max_length=100)
    uploaded_by = models.CharField(max_length=100)
    scp_file = models.FileField(upload_to='scpfiles/')

    def __str__(self):
        return self.scp_file_name

    def delete(self, *args, **kwargs):
        self.scp_file.delete()
        super().delete(*args, **kwargs)
###################################################
class GoldenConfig(models.Model):
    device_platform = models.CharField(max_length=100)
    config = models.TextField(null=True, blank=True)
    submitted_by_user = models.CharField(max_length=50)
    def __str__(self):
        return self.device_platform
        return self.config
###################################################
class GoldenConfigDiffs(models.Model):
    device_platform = models.CharField(max_length=100)
    config = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.device_platform
        return self.config
###################################################
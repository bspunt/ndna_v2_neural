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

""" LOAD UP ALL OUR MODULES AND/OR GET THEM VIA OTHER MODULES, E.G. BACKGROUND_WORKER.py """

""" web related """
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404, HttpResponseRedirect
from django.http import JsonResponse

""" django generic views related """
from django.views.generic import TemplateView, ListView, CreateView, View

""" messages/cache related """
from django.core.cache import cache
from django.contrib import messages

""" auth related """
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.models import Permission

""" forms """
from .forms import *

""" models from db """
from .models import *

""" background worker.py """
from .background_worker import *

""" rq related """
import django_rq
import uuid

""" file storage related """
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
import mimetypes
from django.contrib.staticfiles.utils import get_files
import zipfile
from io import BytesIO

""" REST API and Charts related """
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q, Sum

""" config templating related """
import jinja2
#import logging

""" tabulate libraries """
from django_tabulate import tabulate_qs
from tabulate import tabulate

from django.utils.decorators import method_decorator
########################################
""" Other RestAPI Related """
from rest_framework import viewsets
from .serializers import * # this is a class in my .py module for the models to serialize

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
########################################
#@method_decorator(login_required, name='dispatch')
class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = Device.objects.all().order_by('hostname')
    serializer_class = DeviceSerializer
class GoldenConfigsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = GoldenConfig.objects.all().order_by('device_platform')
    serializer_class = GoldenConfigsSerializer
########################################
########################################
@login_required
def home(request):
    username = request.user.username
    return render(request, 'home.html')
########################################
""" initial open source setup function for fqdn, and email notifications setup """
@login_required
def setup(request):
    username = request.user.username

    if request.method == "POST" and 'btnform1' in request.POST:
        changednsname = request.POST['changednsname']
        to_email_address = request.POST['to_email_address']

        setup_template_links = r"""
        grep -rl neural.domainname.com ./templates/ | xargs sed -i 's/neural.domainname.com/%s/g'
        """ % (changednsname)

        subprocess.Popen(setup_template_links, shell=True, stdout=subprocess.PIPE)
        time.sleep(3)

        setup_domain_system_background_worker = r"""
        grep -rl neural.domainname.com ./neural/background_worker.py | xargs sed -i 's/neural.domainname.com/%s/g'
        """ % (changednsname)

        subprocess.Popen(setup_domain_system_background_worker, shell=True, stdout=subprocess.PIPE)
        time.sleep(3)

        setup_email_to = r"""
        grep -rl notifications ./neural/background_worker.py | xargs sed -i 's/notifications/%s/g'
        """ % (to_email_address)

        subprocess.Popen(setup_email_to, shell=True, stdout=subprocess.PIPE)
        time.sleep(3)

        return redirect('home')

    if request.method == "POST" and 'btnform2' in request.POST:
        currentdnsname = request.POST['currentdnsname']
        current_to_email_address = request.POST['current_to_email_address']
        changednsname = request.POST['changednsname2']
        to_email_address2 = request.POST['to_email_address2']

        setup_template_links = r"""
        grep -rl %s ./templates/ | xargs sed -i 's/%s/%s/g'
        """ % (currentdnsname, currentdnsname, changednsname)

        subprocess.Popen(setup_template_links, shell=True, stdout=subprocess.PIPE)
        time.sleep(3)

        setup_domain_system_background_worker = r"""
        grep -rl %s ./neural/background_worker.py | xargs sed -i 's/%s/%s/g'
        """ % (currentdnsname, currentdnsname, changednsname)

        subprocess.Popen(setup_domain_system_background_worker, shell=True, stdout=subprocess.PIPE)
        time.sleep(3)

        setup_email_to = r"""
        grep -rl %s ./neural/background_worker.py | xargs sed -i 's/%s/%s/g'
        """ % (current_to_email_address, current_to_email_address, to_email_address2)

        subprocess.Popen(setup_email_to, shell=True, stdout=subprocess.PIPE)
        time.sleep(3)

        return redirect('home')

    return render(request, 'setup.html')
########################################
@login_required
def logs(request):
    now = datetime.datetime.now()
    logs = Log.objects.filter(time__range=[now - datetime.timedelta(days=28), now])
    #logs = Log.objects.all() 
    context = {
        'logs': logs
    }
    return render(request, 'log.html', context)
########################################
@login_required
def devices(request):
    all_device = Device.objects.all()

    context = {
        'all_device': all_device
    }

    """ download individual files """
    if request.method == "POST" and 'config' in request.POST:
        config = request.POST['config']
        request.session['config'] = config # set 'config var' in the session

        return redirect('download_specific_files')
    
        """ delete from inventory """
    if request.method == "POST" and 'delete' in request.POST:
        delete = request.POST['delete']
        Device.objects.filter(hostname=delete).delete()
        return render(request, 'devices.html', context)

    return render(request, 'devices.html', context)
#################################################
import glob
@login_required
def download_specific_files(request):
    username = request.user.username
    config = request.session['config'] # get 'config var' from the session
    files = glob.glob('./configs/svcacct-netbrains/network_configs/' + config + '*')

    """ download individual files """
    if request.method == "POST" and 'configfile' in request.POST:
            configfile = request.POST['configfile']

            fl = open(configfile, 'r')

            mime_type, _ = mimetypes.guess_type(configfile)
            response = HttpResponse(fl, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % configfile
            return response

    """ Compare diff on two files """
    if request.method == "POST" and 'compare_diff' in request.POST:
        config1 = request.POST['config1']
        config2 = request.POST['config2']

        compare_diff = r"""
        #rm ./templates/diff.html
        cd ./neural
        python3 compare_diff.py ../configs/svcacct-netbrains/network_configs/%s ../configs/svcacct-netbrains/network_configs/%s -m > ../templates/diff.html
        """ % (config1, config2)

        subprocess.Popen(compare_diff, shell=True, stdout=subprocess.PIPE)
        time.sleep(10)

        return render(request, 'diff.html')

    return render(request, 'download_specific_files.html', {'files': files})
########################################
####### Upload Inventory CSV file - Legacy - Using Nautobot style form #######
class UploadInventory(CreateView):
    model = Inventorie
    form_class = InventoryForm
    success_url = reverse_lazy('inventory_templates')
    template_name = 'upload_inventory.html'
########## - Legacy - Using Nautobot style form 
@login_required
def delete_inventory_template(request, pk):
    if request.method == 'POST':
        inventorytemplate = Inventorie.objects.get(pk=pk)
        inventorytemplate.delete()
    return redirect('inventory_templates')
####### Build Mutiple Devices to Inventory  - Legacy - Using Nautobot style form  #######
@login_required
def inventory_templates(request):
    inventorytemplates = Inventorie.objects.all()
    csvvars = os.listdir('inventoryfiles')  

    if request.method == "POST" and 'btnform2' in request.POST:
        inventorycsv = request.POST['inventorycsv']
        df = pd.read_csv("./inventoryfiles/%s" % inventorycsv) 
        
        for i in df.itertuples(): 
            a = i.hostname
            b = i.model
            c = i.site
            d = i.device_type
            e = i.vendor
            f = i.OS
            g = i.Region

            """ build a list, then then add new line feed to devices var to pass to template to report on upload 
            template redirects via javascript after 20 seconds to devices pages"""
            devices2 = df.values.tolist()
            devices = "\n".join(str(row) for row in devices2)

            """ enforce site, device type, Region and OS naming and standards for inventories """

            if c not in ("dal","res","lv2","dub","cba","mel","syd","sao","mar","wat","zur","bog","mun","rat","ban","mad","par","tbd","hst","cor","tel","bgl","hyd","mum","rom","osa","tok","seo","ldv","mex","ams","amv","joh","riy","sgp","sin","ayl","slo","cmd","dnv","hil","lvs","oak","sjc","smc","smc2","sdwan-aws-cloud","aws","jstephens","pav-pad","hlo"):
                #return redirect('devices')
                return render(request, 'device_inventory_error.html', {'c': c})
            if d not in ('core','leaf','distribution','access','sdwan_router','edge_core','edge_router','mpls_router','sip_router','vhert_router','vpn_switch','edge_router_no_object_group','pub_switch','edge_svc_switch','wlc','saas','dmvpn_router','voip_router','voip_switch','eng_core','pub_core','db_core','pci_core','spine','sdwan_control','aws_router','p2p_router'):
                return render(request, 'device_inventory_error.html', {'d': d})
            if g not in ('NASA','EMEA','APAC'):
                return render(request, 'device_inventory_error.html', {'g': g})
            if f not in ('IOS','NXOS','SDWAN-IOS','WLC-IOS','viptela'):
                return render(request, 'device_inventory_error.html', {'f': f})
            # check to see if exists in the db first, if so, update fields, if not, create a new entry
            check_inventory = Device.objects.filter(hostname='%s' % a)
            if not check_inventory:
                add_to_inventory = Device.objects.create(hostname=a, model=b, site=c, device_type=d, vendor=e, OS=f, Region=g)
                add_to_inventory.save()
            else:
                #update_inventory = Device.objects.filter(hostname='%s' % a).update(hostname=a, model=b, site=c, device_type=d, vendor=e, OS=f, Region=g)
                return render(request, 'device_inventory_error_device_exists.html')
    
        return render(request, 'device_inventory_results.html', {'devices': devices})

    return render(request, 'inventory_templates.html', {'inventorytemplates': inventorytemplates, 'csvvars': csvvars })

# using nautobot style form for csv input w/ headers
@login_required
def import_device_inventory(request):
    #inventorytemplates = Inventorie.objects.all()
    #csvvars = os.listdir('inventoryfiles')  

    if request.method == "POST" and 'btnform1' in request.POST:
        device_import_csv_post = request.POST['inventorycsv'].splitlines()
        export_file_name = './inventoryfiles/csv_devices_export.csv'
        fo_export = open(export_file_name, "w")

        for line in device_import_csv_post:
            fo_export.write("%s\n" % line)
            continue
        fo_export.close()
        time.sleep(2)

        """ use pandas to create variables/dataframe for import and write to the database """
        df = pd.read_csv("%s" % export_file_name) 

        for i in df.itertuples(): 
            a = i.hostname
            b = i.model
            c = i.site
            d = i.device_type
            e = i.vendor
            f = i.OS
            g = i.Region

            """ build a list, then then add new line feed to devices var to pass to template to report on upload 
            template redirects via javascript after 20 seconds to devices pages"""
            devices2 = df.values.tolist()
            devices = "\n".join(str(row) for row in devices2)

            add_to_inventory = Device.objects.create(hostname=a, model=b, site=c, device_type=d, vendor=e, OS=f, Region=g)
            add_to_inventory.save()
                
        return render(request, 'device_inventory_results.html', {'devices': devices})

    return render(request, 'import_device_inventory.html')

####### Build Single Device into Inventory  - Legacy - Using Nautobot style form  #######
@login_required
def inventory_upload_single_device(request):
    if request.method == "POST":
        hostname = request.POST['hostname']
        model = request.POST['model']
        site = request.POST['site']
        device_type = request.POST['device_type']
        vendor = request.POST['vendor']
        OS = request.POST['OS']
        Region = request.POST['Region']

        check_inventory = Device.objects.filter(hostname='%s' % hostname)

        if not check_inventory:
            add_to_inventory = Device.objects.create(hostname=hostname, model=model, site=site, device_type=device_type, vendor=vendor, OS=OS, Region=Region)
            add_to_inventory.save()
        
        else:
            return render(request, 'device_inventory_error_device_exists.html')
            #update_inventory = Device.objects.filter(hostname='%s' % hostname).update(hostname=hostname, model=model, site=site, device_type=device_type, vendor=vendor, OS=OS, Region=Region)

        return redirect('devices')

    return render(request, 'inventory_upload_single_device.html')


####### Update Single Device into Inventory  - Legacy - Using Nautobot style form  #######
@permission_required('neural.add_t3', raise_exception=True)
@login_required
def update_inventory_single_device(request):
    if request.method == "POST":
        hostname = request.POST['hostname']
        model = request.POST['model']
        site = request.POST['site']
        device_type = request.POST['device_type']
        vendor = request.POST['vendor']
        OS = request.POST['OS']
        Region = request.POST['Region']

        check_inventory = Device.objects.filter(hostname='%s' % hostname)

        if not check_inventory:
            add_to_inventory = Device.objects.create(hostname=hostname, model=model, site=site, device_type=device_type, vendor=vendor, OS=OS, Region=Region)
            add_to_inventory.save()
        
        else:
            update_inventory = Device.objects.filter(hostname='%s' % hostname).update(hostname=hostname, model=model, site=site, device_type=device_type, vendor=vendor, OS=OS, Region=Region)

        return redirect('devices')

    return render(request, 'inventory_upload_single_device.html')

####### Update Mutiple Devices to Inventory  - Legacy - Using Nautobot style form  #######
@permission_required('neural.add_t3', raise_exception=True)
@login_required
def update_inventory_templates(request):
    inventorytemplates = Inventorie.objects.all()
    csvvars = os.listdir('inventoryfiles')  

    if request.method == "POST" and 'btnform2' in request.POST:

        inventorycsv = request.POST['inventorycsv']
        
        df = pd.read_csv("./inventoryfiles/%s" % inventorycsv) 
        
        for i in df.itertuples(): 
            a = i.hostname
            b = i.model
            c = i.site
            d = i.device_type
            e = i.vendor
            f = i.OS
            g = i.Region

            """ build a list, then then add new line feed to devices var to pass to template to report on upload 
            template redirects via javascript after 20 seconds to devices pages"""
            devices2 = df.values.tolist()
            devices = "\n".join(str(row) for row in devices2)

            """ enforce site, device type, Region and OS naming and standards for inventories """

            if c not in ("dal","res","lv2","dub","cba","mel","syd","sao","mar","wat","zur","bog","mun","rat","ban","mad","par","tbd","hst","cor","tel","bgl","hyd","mum","rom","osa","tok","seo","ldv","mex","ams","amv","joh","riy","sgp","sin","ayl","slo","cmd","dnv","hil","lvs","oak","sjc","smc","smc2","sdwan-aws-cloud","aws","jstephens","pav-pad","hlo"):
                #return redirect('devices')
                return render(request, 'device_inventory_error.html', {'c': c})
            if d not in ('core','leaf','distribution','access','sdwan_router','edge_core','edge_router','mpls_router','sip_router','vhert_router','vpn_switch','edge_router_no_object_group','pub_switch','edge_svc_switch','wlc','saas','dmvpn_router','voip_router','voip_switch','eng_core','pub_core','db_core','pci_core','spine','sdwan_control','aws_router','p2p_router'):
                return render(request, 'device_inventory_error.html', {'d': d})
            if g not in ('NASA','EMEA','APAC'):
                return render(request, 'device_inventory_error.html', {'g': g})
            if f not in ('IOS','NXOS','SDWAN-IOS','WLC-IOS','viptela'):
                return render(request, 'device_inventory_error.html', {'f': f})

            # check to see if exists in the db first, if so, update fields, if not, create a new entry
            check_inventory = Device.objects.filter(hostname='%s' % a)
            if not check_inventory:
                add_to_inventory = Device.objects.create(hostname=a, model=b, site=c, device_type=d, vendor=e, OS=f, Region=g)
                add_to_inventory.save()
            else:
                update_inventory = Device.objects.filter(hostname='%s' % a).update(hostname=a, model=b, site=c, device_type=d, vendor=e, OS=f, Region=g)
    
        return render(request, 'device_inventory_results.html', {'devices': devices})

    return render(request, 'inventory_templates.html', {'inventorytemplates': inventorytemplates, 'csvvars': csvvars })

####### View Example Inventory  - Legacy - Using Nautobot style form  #######
@login_required
def inventory_csv_example(request):
    return render(request, 'inventory_csv_example.html')

####### Ad_hoc Automation (Freeform Using Datatables Device Selection from MySQL Inventories) #######
from .neural_job_tasks import *
#################################################
@login_required
def ad_hoc_automation_selected_devices(request):
    form = DateForm()
    username = request.user.username

    if not os.path.exists('/var/www/django_app/mysite/job_task_names/%s' % username):
        os.makedirs('/var/www/django_app/mysite/job_task_names/%s' % username)
    else:
        pass

    if not os.path.exists('/var/www/django_app/mysite/job_task_nodes_commands/%s' % username):
        os.makedirs('/var/www/django_app/mysite/job_task_nodes_commands/%s' % username)
    else:
        pass

    tasks = os.listdir('/var/www/django_app/mysite/job_task_names/%s' % username)

    all_device = Device.objects.all()

    context = {
        'all_device': all_device,
        'tasks': tasks,
        'form': form,
    }

    """ create/save private user specific job task """
    if request.method == "POST" and 'btnform1000' in request.POST:
        """ build info for dynamic self service nodes/command list for job task """
        command_list = request.POST['command_list'].splitlines()
        nodes_list = request.POST.getlist('device') 
        task_name = request.POST['task_name']

        """ Call save task method from neural_job_tasks module class """
        x = neural_private_automation_task(username, nodes_list, command_list, task_name)
        private_save_task = x.save_task_private(username, nodes_list, command_list, task_name)

        return render(request, 'ad_hoc_automation_selected_devices.html', context)

    """ Run private user specific job task """
    if request.method == "POST" and 'btnform100' in request.POST:
        run_task = request.POST['run_task']
        time_sleep = request.POST['time_sleep']
        command_sleep=int(time_sleep)
        task_name = run_task

        open_nodes_file_to_run_task = open('./job_task_nodes_commands/' + username + '/nodes_file_' + task_name).readlines()
        nodes_list = list(map(lambda x:x.strip(),open_nodes_file_to_run_task))

        open_commands_file_to_run_task = open('./job_task_nodes_commands/' + username + '/commands_file_' + task_name).readlines()
        command_list = list(map(lambda x:x.strip(),open_commands_file_to_run_task))

        # Make sure this is in all automation views!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))

        ad_hoc_ssh_entry_point.delay(username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id))

        """ progress bar status page and results """
        return redirect('automation_results', job_id = job_result.pk)

    """ delete job task """
    if request.method == "POST" and 'btnform150' in request.POST:
        run_task = request.POST['run_task']

        task_name = run_task

        delete_task = r"""
        rm ./job_task_nodes_commands/%s/nodes_file_%s
        rm ./job_task_names/%s/%s
        rm ./job_task_nodes_commands/%s/commands_file_%s
        """ % (username, task_name, username, task_name, username, task_name)
        subprocess.Popen(delete_task, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)
        
        return render(request, 'ad_hoc_automation_selected_devices.html', context)

    """ review nodes/commands for job task """
    if request.method == "POST" and 'btnform200' in request.POST:
        run_task = request.POST['run_task']
        task_name = run_task

        open_nodes_file_to_run_task = open('./job_task_nodes_commands/' + username + '/nodes_file_' + task_name).readlines()
        nodes_list = list(map(lambda x:x.strip(),open_nodes_file_to_run_task))

        open_commands_file_to_run_task = open('./job_task_nodes_commands/' + username + '/commands_file_' + task_name).readlines()
        command_list = list(map(lambda x:x.strip(),open_commands_file_to_run_task))

        list_of_nodes = [i for i in nodes_list]

        return render(request, 'nodes_list_results.html', {'list_of_nodes': list_of_nodes, 'command_list':command_list})

    if request.method == "POST" and 'btnform10' in request.POST:
        """ build info for pre-preview page """
        command_list = request.POST['command_list'].splitlines()
        nodes_list = request.POST.getlist('device') 

        """ display nodes_list results for ad_hoc_automation_db_query page selection """

        list_of_nodes = [i for i in nodes_list]

        return render(request, 'nodes_list_results.html', {'list_of_nodes': list_of_nodes, 'command_list':command_list})

    if request.method == "POST" and 'btnform1' in request.POST:
        time_sleep = request.POST['time_sleep']
        command_sleep=int(time_sleep)
        command_list = request.POST['command_list'].splitlines()
        nodes_list = request.POST.getlist('device')

        # Make sure this is in all automation views!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))

        ad_hoc_ssh_entry_point.delay(username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id))

        """ progress bar status page and results """
        return redirect('automation_results', job_id = job_result.pk)
    
    if request.method == "POST" and 'btnform2' in request.POST:
        form = DateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            datetime_field = data['datetime_field']

            time_sleep = request.POST['time_sleep']
            command_sleep=int(time_sleep)
            command_list = request.POST['command_list'].splitlines()
            nodes_list = request.POST.getlist('device')

            # Make sure this is in all automation views!
            if not os.path.exists('./configs/%s' %username):
                os.makedirs('./configs/%s' %username)
            else:
                pass

            job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))
            job_id = job_result.pk

            scheduler = django_rq.get_scheduler('default')
            job = scheduler.enqueue_at(datetime_field, ad_hoc_ssh_entry_point, username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id))

            job_result.status='scheduled'
            job_result.save()

            """ dynamic scheduled job results """
            return redirect('scheduled', job_id)

    return render(request, 'ad_hoc_automation_selected_devices.html', context)

####### Ad_hoc Automation (Freeform) #######
@login_required
def ad_hoc_automation(request):
    form = DateForm()
    username = request.user.username
    
    if request.method == "POST" and 'btnform1' in request.POST:
        #password = request.POST['password']  
        time_sleep = request.POST['time_sleep']
        nodes_list = request.POST['nodes_list'].splitlines()
        command_list = request.POST['command_list'].splitlines()

        command_sleep=int(time_sleep)

        # Make sure this is in all automation views!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))

        ad_hoc_ssh_entry_point.delay(username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id))

        """ progress bar status page and results """
        return redirect('automation_results', job_id = job_result.pk)
    
    if request.method == "POST" and 'btnform2' in request.POST:
        form = DateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            datetime_field = data['datetime_field']

            time_sleep = request.POST['time_sleep']
            nodes_list = request.POST['nodes_list'].splitlines()
            command_list = request.POST['command_list'].splitlines()

            command_sleep=int(time_sleep)

            # Make sure this is in all automation views!
            if not os.path.exists('./configs/%s' %username):
                os.makedirs('./configs/%s' %username)
            else:
                pass

            job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))
            job_id = job_result.pk

            scheduler = django_rq.get_scheduler('default')
            job = scheduler.enqueue_at(datetime_field, ad_hoc_ssh_entry_point, username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id))

            job_result.status='scheduled'
            job_result.save()

            """ dynamic scheduled job results """
            return redirect('scheduled', job_id)
            
    return render(request, 'ad_hoc_automation.html', {'form': form})

####### TCPDUMP Ad_hoc UNIQUE Automation (Freeform) #######
@login_required
def fw_ad_hoc_tcpdump_automation(request):
    form = DateForm()
    username = request.user.username
    """ unique command per node CAN BE USED FOR IDENTIFYING PORT TO RUN TCPDUMP 
    across multiple Linux/network nodes that support tcpdump, AND/OR RUNNING TCPDUMP ON MULTIPLE FIREWALLS ON LIMITLESS NUMBER OF FWs! """

    if request.method == "POST" and 'btnform1' in request.POST:
        time_sleep = request.POST['time_sleep']
        nodes_list = request.POST['nodes_list'].splitlines()
        command_list = request.POST['command_list'].splitlines()

        pcapname = request.POST['pcapname'].splitlines()

        command_sleep=int(time_sleep)

        # Make sure this is in all automation views!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_fw_tcpdump_automation', user='%s' % username, total_device_count=len(nodes_list))

        svcacct_t3password = svcacct.objects.filter(username='T3')
        for p in svcacct_t3password:
            t3pass = p.password

            fw_automation_unique_command_per_fw_entry_point.delay(username, nodes_list, command_list, command_sleep, pcapname, t3pass, job_result, job_id=str(job_result.job_id))

        """ progress bar status page and results -- WILL SHOW FULL OUTPUT FOR EFFICIENCY """
        return redirect('fw_automation_results', job_id = job_result.pk)

    if request.method == "POST" and 'btnform2' in request.POST:
        form = DateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            datetime_field = data['datetime_field']

            time_sleep = request.POST['time_sleep']
            nodes_list = request.POST['nodes_list'].splitlines()
            command_list = request.POST['command_list'].splitlines()

            pcapname = request.POST['pcapname']

            command_sleep=int(time_sleep)

            # Make sure this is in all automation views!
            if not os.path.exists('./configs/%s' %username):
                os.makedirs('./configs/%s' %username)
            else:
                pass

            job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_fw_tcpdump_automation', user='%s' % username, total_device_count=len(nodes_list))
            job_id = job_result.pk

            scheduler = django_rq.get_scheduler('default')

            svcacct_t3password = svcacct.objects.filter(username='T3')
            for p in svcacct_t3password:
                t3pass = p.password

                job = scheduler.enqueue_at(datetime_field, fw_automation_unique_command_per_fw_entry_point, username, nodes_list, command_list, command_sleep, pcapname, t3pass, job_result, job_id=str(job_result.job_id))
                job_result.status='scheduled'
                job_result.save()

            """ dynamic scheduled job results """
            return redirect('scheduled', job_id)
        
    return render(request, 'fw_ad_hoc_tcpdump_automation.html', {'form': form})
################################################################################
""" progress bar status page and results """
def fw_automation_results(request, job_id):
    job_result = get_object_or_404(JobResult, pk=job_id)
    return render(request, 'fw_automation_results.html', {'job_result': job_result})

####### Ad_hoc Automation (Freeform) SQL query #######
@login_required
def ad_hoc_automation_db_query(request):
    form = DateForm()
    username = request.user.username

    """ send var db query TO template for dropdown choices """
    site = Device.objects.filter().order_by().values_list('site', flat=True).distinct()
    device_type = Device.objects.filter().order_by().values_list('device_type', flat=True).distinct()
    OS = Device.objects.filter().order_by().values_list('OS', flat=True).distinct()
    Region = Device.objects.filter().order_by().values_list('Region', flat=True).distinct()

    context = {
        'site': site,
        'device_type': device_type,
        'OS': OS,
        'Region': Region,
        'form': form,
    }

    if request.method == "POST" and 'btnform10' in request.POST:
        """ build db query from var or vars submitted FROM template """
        sitevar = request.POST['sitevar']
        devicetypevar = request.POST['devicetypevar']
        command_list = request.POST['command_list'].splitlines()

        if devicetypevar == 'All Device Types':  # equal to no device type chosen
            nodes_list = Device.objects.filter(site=sitevar).values_list('hostname', flat=True)

        elif sitevar == 'All Sites': # equal to no site chosen
            nodes_list = Device.objects.filter(device_type=devicetypevar).values_list('hostname', flat=True)

        else: # equal to site and device type chosen
            nodes_list = Device.objects.filter(site=sitevar, device_type=devicetypevar).values_list('hostname', flat=True)

        """ display nodes_list results for ad_hoc_automation_db_query page selection """

        list_of_nodes = [i for i in nodes_list]

        return render(request, 'nodes_list_results.html', {'list_of_nodes': list_of_nodes, 'command_list':command_list})

    if request.method == "POST" and 'btnform1' in request.POST:
        #password = request.POST['password']  
        time_sleep = request.POST['time_sleep']
        command_list = request.POST['command_list'].splitlines()
        command_sleep=int(time_sleep)

        """ build db query from var or vars submitted FROM template """
        sitevar = request.POST['sitevar']
        devicetypevar = request.POST['devicetypevar']

        """ run automation on all devices at chosen site first option """
        """ run automation for chosen device type at every site second option """
        """ run automation for specific device type at a specific site third option """
        if devicetypevar == 'All Device Types':  # equal to no device type chosen
            nodes_list = Device.objects.filter(site=sitevar).values_list('hostname', flat=True)

        elif sitevar == 'All Sites': # equal to no site chosen
            nodes_list = Device.objects.filter(device_type=devicetypevar).values_list('hostname', flat=True)

        else: # equal to site and device type chosen
            nodes_list = Device.objects.filter(site=sitevar, device_type=devicetypevar).values_list('hostname', flat=True)

        
        # Make sure this is in all automation views!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))

        ad_hoc_ssh_entry_point.delay(username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id))

        """ progress bar status page and results """
        return redirect('automation_results', job_id = job_result.pk)
    
    if request.method == "POST" and 'btnform30' in request.POST:
        command_list = request.POST['command_list'].splitlines()
        region = request.POST['region']
        devicetypevar = request.POST['devicetypevar']

        nodes_list = Device.objects.filter(Region=region, device_type=devicetypevar).values_list('hostname', flat=True)

        """ display nodes_list results for ad_hoc_automation_db_query page selection """

        list_of_nodes = [i for i in nodes_list]

        return render(request, 'nodes_list_results.html', {'list_of_nodes': list_of_nodes, 'command_list':command_list})

    if request.method == "POST" and 'btnform3' in request.POST:
        #password = request.POST['password']  
        time_sleep = request.POST['time_sleep']
        command_list = request.POST['command_list'].splitlines()
        command_sleep=int(time_sleep)

        """ build db query from var or vars submitted FROM template """
        region = request.POST['region']
        devicetypevar = request.POST['devicetypevar']

        nodes_list = Device.objects.filter(Region=region, device_type=devicetypevar).values_list('hostname', flat=True)

        # Make sure this is in all automation views!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))

        ad_hoc_ssh_entry_point.delay(username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id))

        """ progress bar status page and results """
        return redirect('automation_results', job_id = job_result.pk)

    if request.method == "POST" and 'btnform50' in request.POST:
        command_list = request.POST['command_list'].splitlines()

        """ build db query from var or vars submitted FROM template """
        region = request.POST['region']
        OS = request.POST['OS']

        nodes_list = Device.objects.filter(OS=OS, Region=region).values_list('hostname', flat=True)

        """ display nodes_list results for ad_hoc_automation_db_query page selection """

        list_of_nodes = [i for i in nodes_list]

        return render(request, 'nodes_list_results.html', {'list_of_nodes': list_of_nodes, 'command_list':command_list})

    if request.method == "POST" and 'btnform5' in request.POST:
        #password = request.POST['password']  
        time_sleep = request.POST['time_sleep']
        command_list = request.POST['command_list'].splitlines()
        command_sleep=int(time_sleep)

        """ build db query from var or vars submitted FROM template """
        region = request.POST['region']
        OS = request.POST['OS']

        nodes_list = Device.objects.filter(OS=OS, Region=region).values_list('hostname', flat=True)

        # Make sure this is in all automation views!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))

        ad_hoc_ssh_entry_point.delay(username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id))

        """ progress bar status page and results """
        return redirect('automation_results', job_id = job_result.pk)

    if request.method == "POST" and 'btnform70' in request.POST:
        command_list = request.POST['command_list'].splitlines()

        """ build db query from var or vars submitted FROM template """
        sitevar = request.POST['sitevar']
        OS = request.POST['OS']

        nodes_list = Device.objects.filter(OS=OS, site=sitevar).values_list('hostname', flat=True)

        """ display nodes_list results for ad_hoc_automation_db_query page selection """

        list_of_nodes = [i for i in nodes_list]

        return render(request, 'nodes_list_results.html', {'list_of_nodes': list_of_nodes, 'command_list':command_list})

    if request.method == "POST" and 'btnform7' in request.POST:
        #password = request.POST['password']  
        time_sleep = request.POST['time_sleep']
        command_list = request.POST['command_list'].splitlines()
        command_sleep=int(time_sleep)

        """ build db query from var or vars submitted FROM template """
        sitevar = request.POST['sitevar']
        OS = request.POST['OS']

        nodes_list = Device.objects.filter(OS=OS, site=sitevar).values_list('hostname', flat=True)

        # Make sure this is in all automation views!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))

        ad_hoc_ssh_entry_point.delay(username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id))

        """ progress bar status page and results """
        return redirect('automation_results', job_id = job_result.pk)

    if request.method == "POST" and 'btnform2' in request.POST:
        form = DateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            datetime_field = data['datetime_field']
            #password = request.POST['password']  
            time_sleep = request.POST['time_sleep']
            command_list = request.POST['command_list'].splitlines()
            command_sleep=int(time_sleep)

            """ build db query from var or vars submitted FROM template """
            sitevar = request.POST['sitevar']
            devicetypevar = request.POST['devicetypevar']

            """ run automation on all devices at chosen site first option """
            """ run automation for chosen device type at every site second option """
            """ run automation for specific device type at a specific site third option """
            if devicetypevar == 'All Device Types':  # equal to no device type chosen
                nodes_list = Device.objects.filter(site=sitevar).values_list('hostname', flat=True)

            elif sitevar == 'All Sites': # equal to no site chosen
                nodes_list = Device.objects.filter(device_type=devicetypevar).values_list('hostname', flat=True)

            else: # equal to site and device type chosen
                nodes_list = Device.objects.filter(site=sitevar, device_type=devicetypevar).values_list('hostname', flat=True)

            # Make sure this is in all automation views!
            if not os.path.exists('./configs/%s' %username):
                os.makedirs('./configs/%s' %username)
            else:
                pass

            job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))
            job_id = job_result.pk

            scheduler = django_rq.get_scheduler('default')
            job = scheduler.enqueue_at(datetime_field, ad_hoc_ssh_entry_point, username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id),)
            job_result.status='scheduled'
            job_result.save()

            """ dynamic scheduled job results """
            return redirect('scheduled', job_id)
            
    if request.method == "POST" and 'btnform4' in request.POST:
        form = DateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            datetime_field = data['datetime_field']
            #password = request.POST['password']  
            time_sleep = request.POST['time_sleep']
            command_list = request.POST['command_list'].splitlines()
            command_sleep=int(time_sleep)

            """ build db query from var or vars submitted FROM template """
            region = request.POST['region']
            devicetypevar = request.POST['devicetypevar']

            nodes_list = Device.objects.filter(Region=region, device_type=devicetypevar).values_list('hostname', flat=True)

            # Make sure this is in all automation views!
            if not os.path.exists('./configs/%s' %username):
                os.makedirs('./configs/%s' %username)
            else:
                pass

            job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))
            job_id = job_result.pk

            scheduler = django_rq.get_scheduler('default')
            job = scheduler.enqueue_at(datetime_field, ad_hoc_ssh_entry_point, username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id),)
            job_result.status='scheduled'
            job_result.save()

            """ dynamic scheduled job results """
            return redirect('scheduled', job_id)

    if request.method == "POST" and 'btnform6' in request.POST:
        form = DateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            datetime_field = data['datetime_field']
            #password = request.POST['password']  
            time_sleep = request.POST['time_sleep']
            command_list = request.POST['command_list'].splitlines()
            command_sleep=int(time_sleep)

            """ build db query from var or vars submitted FROM template """
            region = request.POST['region']
            OS = request.POST['OS']

            nodes_list = Device.objects.filter(OS=OS, Region=region).values_list('hostname', flat=True)

            # Make sure this is in all automation views!
            if not os.path.exists('./configs/%s' %username):
                os.makedirs('./configs/%s' %username)
            else:
                pass

            job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))
            job_id = job_result.pk

            scheduler = django_rq.get_scheduler('default')
            job = scheduler.enqueue_at(datetime_field, ad_hoc_ssh_entry_point, username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id),)
            job_result.status='scheduled'
            job_result.save()

            """ dynamic scheduled job results """
            return redirect('scheduled', job_id)

    if request.method == "POST" and 'btnform8' in request.POST:
        form = DateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            datetime_field = data['datetime_field']
            #password = request.POST['password']  
            time_sleep = request.POST['time_sleep']
            command_list = request.POST['command_list'].splitlines()
            command_sleep=int(time_sleep)

            """ build db query from var or vars submitted FROM template """
            sitevar = request.POST['sitevar']
            OS = request.POST['OS']

            nodes_list = Device.objects.filter(OS=OS, site=sitevar).values_list('hostname', flat=True)

            # Make sure this is in all automation views!
            if not os.path.exists('./configs/%s' %username):
                os.makedirs('./configs/%s' %username)
            else:
                pass

            job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_automation', user='%s' % username, total_device_count=len(nodes_list))
            job_id = job_result.pk

            scheduler = django_rq.get_scheduler('default')
            job = scheduler.enqueue_at(datetime_field, ad_hoc_ssh_entry_point, username, command_sleep, nodes_list, command_list, job_result, job_id=str(job_result.job_id),)
            job_result.status='scheduled'
            job_result.save()

            """ dynamic scheduled job results """
            return redirect('scheduled', job_id)

    return render(request, 'ad_hoc_automation_db_query.html', context)
################################################################################
""" was configresults.html in lab, now automation_results.html and config_results view name in lab and automation_results in prod  """
""" progress bar status page and results """
def automation_results(request, job_id):
    job_result = get_object_or_404(JobResult, pk=job_id)
    return render(request, 'automation_results.html', {'job_result': job_result})

""" automation_results.html jquery progress bar looks at the URL /jobresults/ which triggers 
    func return_job_results below to get data via JSON Response = (data) """

def return_job_results(request, job_id):
    job = get_object_or_404(JobResult, pk=job_id)

    data = {'id': job.pk,
    'job_name': job.job_name,
    'created': job.created,
    'completed': job.completed,
    'status': job.status,
    'total_device_count': job.total_device_count,
    'completed_device_count': job.completed_device_count,
    'failed_device_count': job.failed_device_count,
    }
    return JsonResponse(data)

""" below includes full config output from the db into the browser via emai link w/ job ID """
@login_required
def full_automation_results(request, job_id):
    job_result = get_object_or_404(JobResult, pk=job_id)
    return render(request, 'full_automation_results.html', {'job_result': job_result})

""" below includes full config output from the db into the browser via emai link w/ job ID """
def backup_results(request, job_id):
    job_result = get_object_or_404(JobResult, pk=job_id)
    return render(request, 'backup_results.html', {'job_result': job_result})
########################################################
########################################################
""" dynamic scheduled job results specific to each user only need this view for all functions scheduled job feedback """
@login_required
def scheduled(request, job_id):       
    job_result = get_object_or_404(JobResult, pk=job_id)
    scheduler = django_rq.get_scheduler('default')
    for job in scheduler.get_jobs():
        if job.id == str(job_result.job_id):
            args = job.args
            return render(request, 'scheduled.html', {'job_result': job_result, 'args': args})

    return Http404
########################################################
########################################################
""" this func is specific to each user, based on filtering in the template """
@login_required
def view_all_scheduled_jobs(request):
    scheduler = django_rq.get_scheduler('default')

    #all_jobs = scheduler.get_jobs(with_times= True)
    all_jobs = scheduler.get_jobs()
    
    if request.method == "POST":
        cancel_job_with_uuid = request.POST['cancel_job_with_uuid']
        scheduler.cancel('%s' % cancel_job_with_uuid)
        return render(request, 'view_all_scheduled_jobs.html', {'all_jobs': all_jobs})

    return render(request, 'view_all_scheduled_jobs.html', {'all_jobs': all_jobs})
########################################################
""" this func looks at all job times system wide """
@login_required
def view_all_scheduled_times(request):
    scheduler = django_rq.get_scheduler('default')

    all_jobs = scheduler.get_jobs(with_times= True)
    
    return render(request, 'view_all_scheduled_times.html', {'all_jobs': all_jobs})
########################################################
########################################
@login_required
def network_configs(request):
    s =FileSystemStorage()
    username = request.user.username
    files = list(get_files(s, location='configs/svcacct-netbrains/network_configs'))

    """ download individual files """
    if request.method == "POST" and 'config' in request.POST:
            config = request.POST['config']
            fl = open(config, 'r')

            mime_type, _ = mimetypes.guess_type(config)
            response = HttpResponse(fl, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % config
            return response

    """ delete individual files """
    if request.method == "POST" and 'delete' in request.POST:
        delete = request.POST['delete']
        # all that is needed is ./%s as the var that's passed from template back e.g. called delete already has the path in it, in this case of 
        # configs/bspunt/<variable file name>, except it doesn't have the relative ./, so we have to add that and specify the variable of 'delete'
        delete_config = r"""
        rm ./%s
        """ % delete
        subprocess.Popen(delete_config, shell=True, stdout=subprocess.PIPE)
    
    """ zipup and download all files """
    if request.method == "POST" and 'zipup' in request.POST:
        byte_data = BytesIO()
        zip_file = zipfile.ZipFile(byte_data, "w")

        for file in files:
            filename = os.path.basename(os.path.normpath(file))
            zip_file.write(file, filename)
        zip_file.close()

        response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=all_network_configs_backups.zip'

        # Print list files in zip_file
        zip_file.printdir()
        return response

    """ delete all files """
    if request.method == "POST" and 'all_files' in request.POST:
        try:
            for file in files:
                delete_all_configs = r"""
                rm ./%s 
                """ % file
                subprocess.Popen(delete_all_configs, shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            pass
    
    """ Compare diff on two files """
    if request.method == "POST" and 'compare_diff' in request.POST:
        config1 = request.POST['config1']
        config2 = request.POST['config2']

        compare_diff = r"""
        #rm ./templates/diff.html
        cd ./neural
        python3 compare_diff.py ../configs/svcacct-netbrains/network_configs/%s ../configs/svcacct-netbrains/network_configs/%s -m > ../templates/diff.html
        """ % (config1, config2)

        subprocess.Popen(compare_diff, shell=True, stdout=subprocess.PIPE)
        time.sleep(10)

        return render(request, 'diff.html')

    return render(request, 'network_configs.html', {'files': files})
########################################
@login_required
def automation_output_configs(request):
    s =FileSystemStorage()
    if request.user.is_authenticated:
        username = request.user.username
        files = list(get_files(s, location='configs/%s' % username))

    """ download individual files """
    if request.method == "POST" and 'config' in request.POST:
            config = request.POST['config']

            fl = open(config, 'r')

            mime_type, _ = mimetypes.guess_type(config)
            response = HttpResponse(fl, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % config
            return response

    """ delete individual files """
    if request.method == "POST" and 'delete' in request.POST:

        delete = request.POST['delete']

        # all that is needed is ./%s as the var that's passed from template back e.g. called delete already has the path in it, in this case of 
        # configs/bspunt/<variable file name>, except it doesn't have the relative ./, so we have to add that and specify the variable of 'delete'
        delete_config = r"""
        rm ./%s
        """ % delete
        subprocess.Popen(delete_config, shell=True, stdout=subprocess.PIPE)
    
    """ zipup and download all files """
    if request.method == "POST" and 'zipup' in request.POST:
        byte_data = BytesIO()
        zip_file = zipfile.ZipFile(byte_data, "w")

        for file in files:
            filename = os.path.basename(os.path.normpath(file))
            zip_file.write(file, filename)
        zip_file.close()

        response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=all_generated_configs.zip'

        # Print list files in zip_file
        zip_file.printdir()
        return response

    """ delete all files """
    if request.method == "POST" and 'all_files' in request.POST:
        try:
            for file in files:
                delete_all_configs = r"""
                rm ./%s 
                """ % file
                subprocess.Popen(delete_all_configs, shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            pass

    return render(request, 'automation_output_configs.html', {'files': files})
########################################
@login_required
def jinja2_templates(request):
    s =FileSystemStorage()
    if request.user.is_authenticated:
        username = request.user.username
        files = list(get_files(s, location='jinja2templates'))

    """ download individual j2 templates """
    if request.method == "POST" and 'config' in request.POST:
            config = request.POST['config']

            fl = open(config, 'r')

            mime_type, _ = mimetypes.guess_type(config)
            response = HttpResponse(fl, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % config
            return response

    """ zipup and download all j2 templates """
    if request.method == "POST" and 'zipup' in request.POST:
        byte_data = BytesIO()
        zip_file = zipfile.ZipFile(byte_data, "w")

        for file in files:
            filename = os.path.basename(os.path.normpath(file))
            zip_file.write(file, filename)
        zip_file.close()

        response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=all_jinja2_templates.zip'

        # Print list files in zip_file
        zip_file.printdir()
        return response

    """ pullfromgit """
    if request.method == "POST" and 'pullfromgit' in request.POST:
        command = "/usr/bin/git pull https://ddfdfdfdfdfp@github.com/bspunt/jinja2templates.git"

        with subprocess.Popen(command, cwd="../jinja2templates", stdout=subprocess.PIPE, stderr=None, shell=True) as process:
            git_status = process.communicate()[0].decode("utf-8")
            #output = process.communicate()[0].decode("utf-8")
            time.sleep(3)

            COPY_GIT_JINJAS = r"""
            rm /var/www/django_app/mysite/jinja2templates/*.j2
            cp /var/www/django_app/jinja2templates/*.j2 /var/www/django_app/mysite/jinja2templates/ 
            """
            subprocess.Popen(COPY_GIT_JINJAS, shell=True, stdout=subprocess.PIPE)
        
            context = {
                'git_status': git_status,
            }

            return render(request, 'jinja2_templates_git_status.html', context)

    return render(request, 'jinja2_templates.html', {'files': files})
########################################
@login_required
def csv_dl_reference_templates(request):
    s =FileSystemStorage()
    if request.user.is_authenticated:
        username = request.user.username
        files = list(get_files(s, location='csv_templates'))

    """ download individual csv_reference templates """
    if request.method == "POST" and 'config' in request.POST:
            config = request.POST['config']

            fl = open(config, 'r')

            mime_type, _ = mimetypes.guess_type(config)
            response = HttpResponse(fl, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % config
            return response

    """ zipup and download all csv templates """
    if request.method == "POST" and 'zipup' in request.POST:
        byte_data = BytesIO()
        zip_file = zipfile.ZipFile(byte_data, "w")

        for file in files:
            filename = os.path.basename(os.path.normpath(file))
            zip_file.write(file, filename)
        zip_file.close()

        response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=all_csv_reference_templates.zip'

        # Print list files in zip_file
        zip_file.printdir()
        return response

    return render(request, 'csv_dl_reference_templates.html', {'files': files})
########################################
@permission_required('neural.add_t3', raise_exception=True)
@login_required
def csv_templates(request):
    configtemplates = Configtemplate.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
        
    return render(request, 'csv_templates.html', {'configtemplates': configtemplates})

@permission_required('neural.add_t3', raise_exception=True)
@login_required
def jinja_templates(request):
    jinjatemplates = Jinjatemplate.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
        
    return render(request, 'jinja_templates.html', {'jinjatemplates': jinjatemplates})
########################################
@login_required
def generate_config_templates(request):
    configtemplates = Configtemplate.objects.all()
    jinjatemplates = os.listdir('jinja2templates')
    csvvars = os.listdir('csv_var_config_templates')  
    
    current_user = request.user
    username = current_user.username

    if not os.path.exists('./unique_automation/%s' % username):
        os.makedirs('./unique_automation/%s' % username)

    if request.method == "POST" and 'btnform2' in request.POST:

        """ csv variables file and jinja2 template file vars """
        csvvarspost = request.POST['csvvarspost']
        jinja2varpost = request.POST['jinja2varpost']

        """ part 1, build no header csv, put into users unique automation folder, 
        then proceed to build templates and put in same folder
        """
        for i in csvvars:
            file = open('./csv_var_config_templates/' + csvvarspost, "rU") # csv is var name passed from the template form
            reader = csv.reader(file, delimiter=',')
        with open('./unique_automation/%s/tmp_outputdata.csv' % username, 'w') as outfile:
            mywriter = csv.writer(outfile)
            for column in reader:
                mywriter.writerow(column[0:2])

        with open("./unique_automation/%s/tmp_outputdata.csv"  % username,'r') as f:
            #with open("./unique_automation/%s/node_name_config_name_header_removed.csv"  % username,'w') as f1:
            # USING APPEND OPTION HERE ALLOWS TO KEEP BUILDING CONFIGS AND UPDATING TO THE CSV WHICH ALLOWS TO PUSH TO THE NETWORK PROPERLY
            with open("./unique_automation/%s/node_name_config_name_header_removed.csv"  % username,'a') as f1:
                #f.next() # skip header line python2 but for python3 it's dunder next!
                f.__next__()
                for line in f:
                    f1.write(line)

        filename1 = "./unique_automation/%s/tmp_outputdata.csv"  % username

        if os.path.exists(filename1):
            os.remove(filename1)
######################################################################################
        """ part 2, build config templates, put into users unique automation folder, 
        then proceed to build templates and put in same folder
        """
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.getcwd()),
            trim_blocks=True, lstrip_blocks=True)

        j2template = env.get_template('./jinja2templates/' + jinja2varpost)

        # chnge to dir we want to write to
        os.chdir('./unique_automation/%s' % username) 

        for row in csv.DictReader(open('../../csv_var_config_templates/' + csvvarspost)):
            with open(row['host_name'], 'w+') as f: 
                f.write(j2template.render(row)) 
                
        """ must get back to base dir for html render or redirect to work! """
        os.chdir('../..') 
######################################################################################
        return redirect('generated_config_files') 
    
    if request.method == "POST" and 'btnform20' in request.POST:
        csvvarspost = request.POST['csvvarspost']
        request.session['csvvarspost'] = csvvarspost # set 'config var' in the session
        return redirect('view_csv_variables_upload') 
    
    return render(request, 'generate_config_templates.html', {
        'configtemplates': configtemplates, 'jinjatemplates': jinjatemplates, 'csvvars': csvvars})
######################################################################
# this relates to finished configs generated via jinja/csv vars merge
def generated_config_files(request):
    s =FileSystemStorage()
    if request.user.is_authenticated:
        username = request.user.username
        files = list(get_files(s, location='unique_automation/%s' % username))

    """ download individual files """
    if request.method == "POST" and 'config' in request.POST:
        config = request.POST['config']
        fl = open(config, 'r')
        mime_type, _ = mimetypes.guess_type(config)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % config

        return response

    """ delete individual files """
    if request.method == "POST" and 'delete' in request.POST:
        delete = request.POST['delete']
        # all that is needed is ./%s as the var that's passed from template back e.g. called delete already has the path in it, in this case of 
        # unique_automation/bspunt/<variable file name>, except it doesn't have the relative ./, so we have to add that and specify the variable of 'delete'
        delete_config_template = r"""
        rm ./%s
        """ % delete
        subprocess.Popen(delete_config_template, shell=True, stdout=subprocess.PIPE)
    
    """ zipup and download all files """
    if request.method == "POST" and 'zipup' in request.POST:
        byte_data = BytesIO()
        zip_file = zipfile.ZipFile(byte_data, "w")

        for file in files:
            filename = os.path.basename(os.path.normpath(file))
            zip_file.write(file, filename)
        zip_file.close()

        response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=all_generated_config_templates.zip'

        # Print list files in zip_file
        zip_file.printdir()
        return response

    """ delete all files """
    if request.method == "POST" and 'all_files' in request.POST:
        try:
            for file in files:
                delete_all_configs = r"""
                rm ./%s 
                """ % file
                subprocess.Popen(delete_all_configs, shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            pass
    return render(request, 'generated_config_files.html', {'files': files})
######################################
# this is for csv uploads, not finished config templates
@login_required
def delete_config_template(request, pk):
    if request.method == 'POST':
        configtemplate = Configtemplate.objects.get(pk=pk)
        configtemplate.delete()
    return redirect('csv_templates')

class UploadConfigTemplate(CreateView):
    model = Configtemplate
    form_class = ConfigTemplatesForm
    success_url = reverse_lazy('generate_config_templates')
    template_name = 'upload_csv.html'

@login_required
def config_templates_example(request):
    return render(request, 'config_templates_example.html')

""" view to view tabulated view of chosen template csv variables file """
@login_required
def view_csv_variables_upload(request):
    csvvarspost = request.session['csvvarspost'] # get 'csvvarspost var' from the session
    
    df = pd.read_csv("./csv_var_config_templates/%s" %csvvarspost) 
    x = tabulate(df, headers='keys', tablefmt='psql')
    context = {
        "x": x,
    } 
    return render(request, 'view_csv_variables_upload.html', context)
################################################################################
######################################
# this is for jinja uploads
@login_required
def delete_jinja_template(request, pk):
    if request.method == 'POST':
        jinjatemplate = Jinjatemplate.objects.get(pk=pk)
        jinjatemplate.delete()
    #return redirect('csv_templates')
    return redirect('jinja_templates')

class UploadJinjaTemplate(CreateView):
    model = Jinjatemplate
    form_class = JinjaTemplatesForm
    success_url = reverse_lazy('generate_config_templates')
    template_name = 'upload_jinja.html'
################################################################################
########################################
""" unique_automation.html uses neural generated config templates and unique_automation_manual_configs.html will use custom config templates """
@login_required
def unique_automation(request):
    form = DateForm()
    username = request.user.username
    """ run now """
    if request.method == "POST" and 'btnform1' in request.POST:
        #password = request.POST['password']  
        time_sleep = request.POST['time_sleep']
        command_sleep=int(time_sleep)

        # Make sure this is in all automation views!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        with open('./unique_automation/%s/node_name_config_name_header_removed.csv' % username, mode='r') as infile:
            reader = csv.reader(infile)
            time.sleep(2)
            #global node_config
            node_config = {rows[0]:rows[1] for rows in reader}

            job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='unique_automation', user='%s' % username, total_device_count=len(node_config))
            
            unique_automation_ssh_entry_point.delay(username, command_sleep, node_config, job_result, job_id=str(job_result.job_id))

            """ progress bar status page and results """
            return redirect('automation_results', job_id = job_result.pk)

    if request.method == "POST" and 'btnform2' in request.POST:
        form = DateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            datetime_field = data['datetime_field']

            #password = request.POST['password']  
            time_sleep = request.POST['time_sleep']
            command_sleep=int(time_sleep)

            # Make sure this is in all automation views!
            if not os.path.exists('./configs/%s' %username):
                os.makedirs('./configs/%s' %username)
            else:
                pass

            with open('./unique_automation/%s/node_name_config_name_header_removed.csv' % username, mode='r') as infile:
                reader = csv.reader(infile)
                time.sleep(2)
                #global node_config
                node_config = {rows[0]:rows[1] for rows in reader}

                job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='unique_automation', user='%s' % username, total_device_count=len(node_config))
                job_id = job_result.pk

                scheduler = django_rq.get_scheduler('default')
                job = scheduler.enqueue_at(datetime_field, unique_automation_ssh_entry_point, username, command_sleep, node_config, job_result, job_id=str(job_result.job_id))
                job_result.status='scheduled'
                job_result.save()

                """ dynamic scheduled job results """
                return redirect('scheduled', job_id)

    return render(request, 'unique_automation.html', {'form': form})

""" unique_automation.html uses neural generated config templates and unique_automation_manual_configs.html will use custom config templates """
########################################
########################################
""" unique_automation.html uses neural generated config templates and unique_automation_manual_configs.html will use custom config templates """
@login_required
def unique_automation_manual_configs(request):
    form = DateForm()
    username = request.user.username

    """ HTML PAGE/TEMPLATE HAS A BTNLINK1 THAT TAKES USER TO manual_configs_upload.html TO UPLOAD ZIP file """

    """ run now """
    if request.method == "POST" and 'btnform1' in request.POST:
        #password = request.POST['password']  
        time_sleep = request.POST['time_sleep']
        command_sleep=int(time_sleep)

        # Create dir if it doesn't exist!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass
        
        # Create dir if it doesn't exist!
        if not os.path.exists('./manual_configs/%s' %username):
            os.makedirs('./manual_configs/%s' %username)
        else:
            pass

        """ clear out directory before unzipping current files into the manual configs directory """
        time.sleep(2)
        COMMAND1 = r"""
        rm -r ./manual_configs/%s/*
        """ % username
        subprocess.Popen(COMMAND1, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)

        """ unzip files into the manual configs directory - zip will have been 
        uploaded to media root, which is just ./ from zip's perspective """
        time.sleep(2)
        UNZIPCONFIGSCOMMAND = r"""
        unzip -q ./%s-manual-ua.zip -d ./manual_configs/%s/
        """ % (username, username)
        subprocess.Popen(UNZIPCONFIGSCOMMAND, shell=True, stdout=subprocess.PIPE)
        time.sleep(4)

        """ after unzipping, remove zip from base site/media root directory """
        REMOVEZIPFILECOMMAND = r"""
        rm -r ./%s-manual-ua.zip
        """ % username
        subprocess.Popen(REMOVEZIPFILECOMMAND, shell=True, stdout=subprocess.PIPE)
        time.sleep(3)

        with open('./manual_configs/%s/node_name_config_name_header_removed.csv' % username, mode='r') as infile:
            reader = csv.reader(infile)
            time.sleep(2)
            #global node_config
            node_config = {rows[0]:rows[1] for rows in reader}

            job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='unique_automation', user='%s' % username, total_device_count=len(node_config))
            
            manual_unique_automation_ssh_entry_point.delay(username, command_sleep, node_config, job_result, job_id=str(job_result.job_id))

            """ progress bar status page and results """
            return redirect('automation_results', job_id = job_result.pk)


    if request.method == "POST" and 'btnform2' in request.POST:
        form = DateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            datetime_field = data['datetime_field']

            #password = request.POST['password']  
            time_sleep = request.POST['time_sleep']
            command_sleep=int(time_sleep)

            # Create dir if it doesn't exist!
            if not os.path.exists('./configs/%s' %username):
                os.makedirs('./configs/%s' %username)
            else:
                pass
        
            # Create dir if it doesn't exist!
            if not os.path.exists('./manual_configs/%s' %username):
                os.makedirs('./manual_configs/%s' %username)
            else:
                pass

            """ clear out directory before unzipping current files into the manual configs directory """
            time.sleep(2)
            COMMAND1 = r"""
            rm -r ./manual_configs/%s/*
            """ % username
            subprocess.Popen(COMMAND1, shell=True, stdout=subprocess.PIPE)
            time.sleep(2)

            """ unzip files into the manual configs directory - zip will have been 
            uploaded to media root, which is just ./ from zip's perspective """
            time.sleep(2)
            UNZIPCONFIGSCOMMAND = r"""
            unzip -q ./%s-manual-ua.zip -d ./manual_configs/%s/
            """ % (username, username)
            subprocess.Popen(UNZIPCONFIGSCOMMAND, shell=True, stdout=subprocess.PIPE)
            time.sleep(4)

            """ after unzipping, remove zip from base site/media root directory """
            REMOVEZIPFILECOMMAND = r"""
            rm -r ./%s-manual-ua.zip
            """ % username
            subprocess.Popen(REMOVEZIPFILECOMMAND, shell=True, stdout=subprocess.PIPE)
            time.sleep(3)


            with open('./manual_configs/%s/node_name_config_name_header_removed.csv' % username, mode='r') as infile:
                reader = csv.reader(infile)
                time.sleep(2)
                #global node_config
                node_config = {rows[0]:rows[1] for rows in reader}

                job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='unique_automation', user='%s' % username, total_device_count=len(node_config))
                job_id = job_result.pk

                scheduler = django_rq.get_scheduler('default')
                job = scheduler.enqueue_at(datetime_field,  manual_unique_automation_ssh_entry_point, username, command_sleep, node_config, job_result, job_id=str(job_result.job_id))
                job_result.status='scheduled'
                job_result.save()

                """ dynamic scheduled job results """
                return redirect('scheduled', job_id)

    return render(request, 'unique_automation_manual_configs.html', {'form': form})

""" unique_automation.html uses neural generated config templates and unique_automation_manual_configs.html will use custom config templates """
########################################

########################################
def manual_configs_upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        #time.sleep(5)
        #return redirect('unique_automation_manual_configs')
        return render(request, 'manual_configs_upload.html', context)

    return render(request, 'manual_configs_upload.html', context)
    #return render(request, 'manual_configs_upload.html')
#######################################
@method_decorator(login_required, name='dispatch')
class monthly_log_stats(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'monthly_log_stats.html')

class LogChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):

        """ DB QUERIES VARS TO INCLUDE IN LISTS (FINAL VARS) """
        ############################################################
        # total devices ran last month log chart
        now = datetime.datetime.now()
        total_devices_ran_Four_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], target__regex=r'.*').count()
        total_devices_ran_Three_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], target__regex=r'.*').count()
        total_devices_ran_Two_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], target__regex=r'.*').count()
        total_devices_ran_Last_7_Days = Log.objects.filter(time__range=[now - datetime.timedelta(days=7), now], target__regex=r'.*').count()
        total_devices_ran_Last_24_Hours = Log.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], target__regex=r'.*').count()

        # total completed without exceptions last month log chart
        total_completed_Four_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], status='No Exception Raised').count()
        total_completed_Three_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], status='No Exception Raised').count()
        total_completed_Two_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], status='No Exception Raised').count()
        total_completed_Last_7_Days = Log.objects.filter(time__range=[now - datetime.timedelta(days=7), now], status='No Exception Raised').count()
        total_completed_Last_24_Hours = Log.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], status='No Exception Raised').count()

        # total exceptions raised last month log chart
        total_exceptions_Four_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], status='Exception Raised').count()
        total_exceptions_Three_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], status='Exception Raised').count()
        total_exceptions_Two_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], status='Exception Raised').count()
        total_exceptions_Last_7_Days = Log.objects.filter(time__range=[now - datetime.timedelta(days=7), now], status='Exception Raised').count()
        total_exceptions_Last_24_Hours = Log.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], status='Exception Raised').count()


        # total ad hoc or ndna automation types last month log chart
        total_type_ad_hoc_ndna_Four_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], task__regex=r'ad_hoc.*').count()
        total_type_ad_hoc_ndna_Three_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], task__regex=r'ad_hoc.*').count()
        total_type_ad_hoc_ndna_Two_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], task__regex=r'ad_hoc.*').count()
        total_type_ad_hoc_ndna_Last_7_Days = Log.objects.filter(time__range=[now - datetime.timedelta(days=7), now], task__regex=r'ad_hoc.*').count()
        total_type_ad_hoc_ndna_Last_24_Hours = Log.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], task__regex=r'ad_hoc.*').count()


        # total unique automation types last month log chart
        total_type_unique_automation_Four_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], task='unique_automation').count()
        total_type_unique_automation_Three_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], task='unique_automation').count()
        total_type_unique_automation_Two_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], task='unique_automation').count()
        total_type_unique_automation_Last_7_Days = Log.objects.filter(time__range=[now - datetime.timedelta(days=7), now], task='unique_automation').count()
        total_type_unique_automation_Last_24_Hours = Log.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], task='unique_automation').count()

        # total self service automation types last month log chart
        total_type_self_service_Four_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], task__regex=r'self_service.*').count()
        total_type_self_service_Three_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], task__regex=r'self_service.*').count()
        total_type_self_service_Two_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], task__regex=r'self_service.*').count()
        total_type_self_service_Last_7_Days = Log.objects.filter(time__range=[now - datetime.timedelta(days=7), now], task__regex=r'self_service.*').count()
        total_type_self_service_Last_24_Hours = Log.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], task__regex=r'self_service.*').count()

        # total rest api automation types last month log chart
        total_type_rest_api_Four_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], task__regex=r'rest_api.*').count()
        total_type_rest_api_Three_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], task__regex=r'rest_api.*').count()
        total_type_rest_api_Two_Weeks_Ago = Log.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], task__regex=r'rest_api.*').count()
        total_type_rest_api_Last_7_Days = Log.objects.filter(time__range=[now - datetime.timedelta(days=7), now], task__regex=r'rest_api.*').count()
        total_type_rest_api_Last_24_Hours = Log.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], task__regex=r'rest_api.*').count()


        """ LISTS FROM VARIABLES BUILT FROM QUERIES """
        ############################################################
        total_devices = [total_devices_ran_Four_Weeks_Ago, total_devices_ran_Three_Weeks_Ago, total_devices_ran_Two_Weeks_Ago, total_devices_ran_Last_7_Days, total_devices_ran_Last_24_Hours]
        total_completed = [total_completed_Four_Weeks_Ago, total_completed_Three_Weeks_Ago, total_completed_Two_Weeks_Ago, total_completed_Last_7_Days, total_completed_Last_24_Hours]
        total_exceptions = [total_exceptions_Four_Weeks_Ago, total_exceptions_Three_Weeks_Ago, total_exceptions_Two_Weeks_Ago, total_exceptions_Last_7_Days, total_exceptions_Last_24_Hours]
        
        # total different types of automation ran last month log chart
        """ 
        for log charts, using this for type ref:
        ad_hoc_or_ndna
        unique_automation
        self_service (base this on regex and then on background worker, use self_service_<type, e.g. vxlan>) 
        """
        total_type_ad_hoc_ndna = [total_type_ad_hoc_ndna_Four_Weeks_Ago, total_type_ad_hoc_ndna_Three_Weeks_Ago, total_type_ad_hoc_ndna_Two_Weeks_Ago, total_type_ad_hoc_ndna_Last_7_Days, total_type_ad_hoc_ndna_Last_24_Hours]
        total_type_unique_automation = [total_type_unique_automation_Four_Weeks_Ago, total_type_unique_automation_Three_Weeks_Ago, total_type_unique_automation_Two_Weeks_Ago, total_type_unique_automation_Last_7_Days, total_type_unique_automation_Last_24_Hours]
        total_type_self_service = [total_type_self_service_Four_Weeks_Ago, total_type_self_service_Three_Weeks_Ago, total_type_self_service_Two_Weeks_Ago, total_type_self_service_Last_7_Days, total_type_self_service_Last_24_Hours]
        total_type_rest_api = [total_type_rest_api_Four_Weeks_Ago, total_type_rest_api_Three_Weeks_Ago, total_type_rest_api_Two_Weeks_Ago, total_type_rest_api_Last_7_Days, total_type_rest_api_Last_24_Hours]
        
        data = {
                "total_devices": total_devices,
                "total_exceptions": total_exceptions,
                "total_completed": total_completed,


                "total_type_ad_hoc_ndna": total_type_ad_hoc_ndna,
                "total_type_unique_automation": total_type_unique_automation,
                "total_type_self_service": total_type_self_service,
                "total_type_rest_api": total_type_rest_api,
        }

        return Response(data)
########################################
@login_required
def all_job_results(request):
    job_results = JobResult.objects.all()
    context = {
        'job_results': job_results
    }

    username = request.user.username

    if request.method == "POST" and 'btnform1' in request.POST:

        config_complete_pre = list(JobResult.objects.values_list('job_id', 'user', 'job_name', 'started', 'completed','output'))
        config_complete = str(config_complete_pre)

        # put on the outside of the loop
        f = open('./tmp/db_config_output.txt', 'w')

        for output in config_complete:
            f.write('%s' % output)   
        
        # put on the outside of the loop
        f.close()

        ############MODIFY FILE AFTER IT'S BEEN WRITTEN############
        CONFIGSDBDLCOMMAND = r"""
        sed -i 's/(UUID/\n\nUUID/g' ./tmp/db_config_output.txt
        sed -i 's/\\n//g' ./tmp/db_config_output.txt
        sed -i 's/\\r/\n/g' ./tmp/db_config_output.txt
        sed -i 's/\*\*\*\*\*Node Output\*\*\*\*\*/\n/g' ./tmp/db_config_output.txt
        sed -i '1s/^/Fields ==\n\njob_uuid | user | job_name | start time | completed time | config output /' ./tmp/db_config_output.txt
        sed -i 's/\[//g' ./tmp/db_config_output.txt
        sed -i 's/\]//g' ./tmp/db_config_output.txt
        """
        subprocess.Popen(CONFIGSDBDLCOMMAND, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)
        ############MODIFY FILE AFTER IT'S BEEN WRITTEN############

        fl_path = './tmp/db_config_output.txt'
        filename = 'db_config_output.txt'

        fl = open(fl_path, 'r')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

    if request.method == "POST" and 'btnform2' in request.POST:
        regex = request.POST['regex']
        config_by_date_pre = list(JobResult.objects.filter(started__regex=r'%s' % regex).values_list('job_id', 'user', 'job_name', 'started', 'completed','output'))
        config_by_date = str(config_by_date_pre)

        # put on the outside of the loop
        f = open('./tmp/config_output.txt', 'w')

        for output in config_by_date:
            f.write('%s' % output)

        # put on the outside of the loop
        f.close()

        ############MODIFY FILE AFTER IT'S BEEN WRITTEN############
        CONFIGSDBDLCOMMAND = r"""
        sed -i 's/(UUID/\n\nUUID/g' ./tmp/config_output.txt
        sed -i 's/\\n//g' ./tmp/config_output.txt
        sed -i 's/\\r/\n/g' ./tmp/config_output.txt
        sed -i 's/\*\*\*\*\*Node Output\*\*\*\*\*/\n/g' ./tmp/config_output.txt
        sed -i '1s/^/Fields ==\n\njob_uuid | user | job_name | start time | completed time | config output /' ./tmp/config_output.txt
        sed -i 's/\[//g' ./tmp/config_output.txt
        sed -i 's/\]//g' ./tmp/config_output.txt
        """
        subprocess.Popen(CONFIGSDBDLCOMMAND, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)
        ############MODIFY FILE AFTER IT'S BEEN WRITTEN############


        fl_path = './tmp/config_output.txt'
        filename = 'db_config_output.txt'

        fl = open(fl_path, 'r')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

    if request.method == "POST" and 'btnform3' in request.POST:
        userid = request.POST['userid']
        config_by_date_pre = list(JobResult.objects.filter(user=userid).values_list('job_id', 'user', 'job_name', 'started', 'completed','output'))
        config_by_date = str(config_by_date_pre)

        # put on the outside of the loop
        f = open('./tmp/config_output.txt', 'w')

        for output in config_by_date:
            f.write('%s' % output)

        # put on the outside of the loop
        f.close()

        ############MODIFY FILE AFTER IT'S BEEN WRITTEN############
        CONFIGSDBDLCOMMAND = r"""
        sed -i 's/(UUID/\n\nUUID/g' ./tmp/config_output.txt
        sed -i 's/\\n//g' ./tmp/config_output.txt
        sed -i 's/\\r/\n/g' ./tmp/config_output.txt
        sed -i 's/\*\*\*\*\*Node Output\*\*\*\*\*/\n/g' ./tmp/config_output.txt
        sed -i '1s/^/Fields ==\n\njob_uuid | user | job_name | start time | completed time | config output /' ./tmp/config_output.txt
        sed -i 's/\[//g' ./tmp/config_output.txt
        sed -i 's/\]//g' ./tmp/config_output.txt
        """
        subprocess.Popen(CONFIGSDBDLCOMMAND, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)
        ############MODIFY FILE AFTER IT'S BEEN WRITTEN############

        fl_path = './tmp/config_output.txt'
        filename = 'db_config_output.txt'

        fl = open(fl_path, 'r')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

    return render(request, 'all_job_results.html', context)
########################################
@login_required
def user_job_results(request):
    job_results = JobResult.objects.all()
    context = {
        'job_results': job_results
    }

    username = request.user.username

    if request.method == "POST" and 'btnform1' in request.POST:

        ##############################################################
        """ this is for user specific jobs """
        config_complete_pre = list(JobResult.objects.filter(user=username).values_list('job_id', 'user', 'job_name', 'started', 'completed','output'))
        config_complete = str(config_complete_pre)
        ##############################################################

        # put on the outside of the loop
        f = open('./tmp/config_output.txt', 'w')

        #for output in config_by_date:
            #f.write('%s' % output)

        for output in config_complete:
            f.write('%s' % output)   
        
        # put on the outside of the loop
        f.close()

        ############MODIFY FILE AFTER IT'S BEEN WRITTEN############
        CONFIGSDBDLCOMMAND = r"""
        sed -i 's/(UUID/\n\nUUID/g' ./tmp/config_output.txt
        sed -i 's/\\n//g' ./tmp/config_output.txt
        sed -i 's/\\r/\n/g' ./tmp/config_output.txt
        sed -i 's/\*\*\*\*\*Node Output\*\*\*\*\*/\n/g' ./tmp/config_output.txt
        sed -i '1s/^/Fields ==\n\njob_uuid | user | job_name | start time | completed time | config output /' ./tmp/config_output.txt
        sed -i 's/\[//g' ./tmp/config_output.txt
        sed -i 's/\]//g' ./tmp/config_output.txt
        """
        subprocess.Popen(CONFIGSDBDLCOMMAND, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)
        ############MODIFY FILE AFTER IT'S BEEN WRITTEN############

        fl_path = './tmp/config_output.txt'
        filename = 'db_config_output.txt'

        fl = open(fl_path, 'r')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

    if request.method == "POST" and 'btnform2' in request.POST:
        regex = request.POST['regex']
        config_by_date_pre = list(JobResult.objects.filter(user=username, started__regex=r'%s' % regex).values_list('job_id', 'user', 'job_name', 'started', 'completed','output'))
        config_by_date = str(config_by_date_pre)

        # put on the outside of the loop
        f = open('./tmp/config_output.txt', 'w')

        for output in config_by_date:
            f.write('%s' % output)

        # put on the outside of the loop
        f.close()

        ############MODIFY FILE AFTER IT'S BEEN WRITTEN############
        CONFIGSDBDLCOMMAND = r"""
        sed -i 's/(UUID/\n\nUUID/g' ./tmp/config_output.txt
        sed -i 's/\\n//g' ./tmp/config_output.txt
        sed -i 's/\\r/\n/g' ./tmp/config_output.txt
        sed -i 's/\*\*\*\*\*Node Output\*\*\*\*\*/\n/g' ./tmp/config_output.txt
        sed -i '1s/^/Fields ==\n\njob_uuid | user | job_name | start time | completed time | config output /' ./tmp/config_output.txt
        sed -i 's/\[//g' ./tmp/config_output.txt
        sed -i 's/\]//g' ./tmp/config_output.txt
        """
        subprocess.Popen(CONFIGSDBDLCOMMAND, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)
        ############MODIFY FILE AFTER IT'S BEEN WRITTEN############

        fl_path = './tmp/config_output.txt'
        filename = 'db_config_output.txt'

        fl = open(fl_path, 'r')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

    return render(request, 'user_job_results.html', context)
#######################################
@method_decorator(login_required, name='dispatch')
class monthly_job_results_stats(View): 
    def get(self, request, *args, **kwargs):
        return render(request, 'monthly_job_results_stats.html')

class JobResultsData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):

        """ DB QUERIES VARS TO INCLUDE IN LISTS (FINAL VARS) """
        now = datetime.datetime.now()

        ############################################################
        # Total Jobs Ran    --> bar chart --> last month job results chart
        total_jobs_Four_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], job_id__regex=r'.*').count()
        total_jobs_Three_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], job_id__regex=r'.*').count()
        total_jobs_Two_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], job_id__regex=r'.*').count()
        total_jobs_Last_7_Days = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=7), now], job_id__regex=r'.*').count()
        total_jobs_Last_24_Hours = JobResult.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], job_id__regex=r'.*').count()

        ############################################################
        # total devices ran last month job results chart
        # Total Device Count (Failed & Completed)    --> bar chart
        total_device_count_Four_Weeks_Ago_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)]).aggregate(Sum('total_device_count')) 
        for key, val1 in total_device_count_Four_Weeks_Ago_pre.items():
            total_device_count_Four_Weeks_Ago = val1

        total_device_count_Three_Weeks_Ago_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)]).aggregate(Sum('total_device_count')) 
        for key, val2 in total_device_count_Three_Weeks_Ago_pre.items():
            total_device_count_Three_Weeks_Ago = val2

        total_device_count_Two_Weeks_Ago_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)]).aggregate(Sum('total_device_count')) 
        for key, val3 in total_device_count_Two_Weeks_Ago_pre.items():
            total_device_count_Two_Weeks_Ago = val3

        total_device_count_Last_7_Days_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=7), now]).aggregate(Sum('total_device_count')) 
        for key, val4 in total_device_count_Last_7_Days_pre.items():
            total_device_count_Last_7_Days = val4

        total_device_count_Last_24_Hours_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(hours=24), now]).aggregate(Sum('total_device_count')) 
        for key, val5 in total_device_count_Last_24_Hours_pre.items():
            total_device_count_Last_24_Hours = val5


        ############################################################
        # Total completed devices last month job results chart
        # Total completed Device Count     --> bar chart
        completed_device_count_Four_Weeks_Ago_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)]).aggregate(Sum('completed_device_count')) 
        for key, val11 in completed_device_count_Four_Weeks_Ago_pre.items():
            completed_device_count_Four_Weeks_Ago = val11

        completed_device_count_Three_Weeks_Ago_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)]).aggregate(Sum('completed_device_count')) 
        for key, val12 in completed_device_count_Three_Weeks_Ago_pre.items():
            completed_device_count_Three_Weeks_Ago = val12

        completed_device_count_Two_Weeks_Ago_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)]).aggregate(Sum('completed_device_count')) 
        for key, val13 in completed_device_count_Two_Weeks_Ago_pre.items():
            completed_device_count_Two_Weeks_Ago = val13

        completed_device_count_Last_7_Days_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=7), now]).aggregate(Sum('completed_device_count')) 
        for key, val14 in completed_device_count_Last_7_Days_pre.items():
            completed_device_count_Last_7_Days = val14

        completed_device_count_Last_24_Hours_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(hours=24), now]).aggregate(Sum('completed_device_count')) 
        for key, val15 in completed_device_count_Last_24_Hours_pre.items():
            completed_device_count_Last_24_Hours = val15


        ############################################################
        # Total failed devices last month job results chart
        # Total failed Device Count     --> bar chart
        failed_device_count_Four_Weeks_Ago_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)]).aggregate(Sum('failed_device_count')) 
        for key, val21 in failed_device_count_Four_Weeks_Ago_pre.items():
            failed_device_count_Four_Weeks_Ago = val21

        failed_device_count_Three_Weeks_Ago_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)]).aggregate(Sum('failed_device_count')) 
        for key, val22 in failed_device_count_Three_Weeks_Ago_pre.items():
            failed_device_count_Three_Weeks_Ago = val22

        failed_device_count_Two_Weeks_Ago_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)]).aggregate(Sum('failed_device_count')) 
        for key, val23 in failed_device_count_Two_Weeks_Ago_pre.items():
            failed_device_count_Two_Weeks_Ago = val23

        failed_device_count_Last_7_Days_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=7), now]).aggregate(Sum('failed_device_count')) 
        for key, val24 in failed_device_count_Last_7_Days_pre.items():
            failed_device_count_Last_7_Days = val24

        failed_device_count_Last_24_Hours_pre = JobResult.objects.filter(time__range=[now - datetime.timedelta(hours=24), now]).aggregate(Sum('failed_device_count')) 
        for key, val25 in failed_device_count_Last_24_Hours_pre.items():
            failed_device_count_Last_24_Hours = val25

        ############################################################
        # Total automation job types last month job results chart
        total_type_ad_hoc_Four_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], job_name__regex=r'ad_hoc.*').count()
        total_type_ad_hoc_Three_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], job_name__regex=r'ad_hoc.*').count()
        total_type_ad_hoc_Two_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], job_name__regex=r'ad_hoc.*').count()
        total_type_ad_hoc_Last_7_Days = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=7), now], job_name__regex=r'ad_hoc.*').count()
        total_type_ad_hoc_Last_24_Hours = JobResult.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], job_name__regex=r'ad_hoc.*').count()

        total_type_ndna_Four_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], job_name='ndna_automation').count()
        total_type_ndna_Three_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], job_name='ndna_automation').count()
        total_type_ndna_Two_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], job_name='ndna_automation').count()
        total_type_ndna_Last_7_Days = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=7), now], job_name='ndna_automation').count()
        total_type_ndna_Last_24_Hours = JobResult.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], job_name='ndna_automation').count()

        total_type_unique_Four_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], job_name='unique_automation').count()
        total_type_unique_Three_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], job_name='unique_automation').count()
        total_type_unique_Two_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], job_name='unique_automation').count()
        total_type_unique_Last_7_Days = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=7), now], job_name='unique_automation').count()
        total_type_unique_Last_24_Hours = JobResult.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], job_name='unique_automation').count()

        total_type_self_service_Four_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], job_name__regex=r'self_service.*').count()
        total_type_self_service_Three_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], job_name__regex=r'self_service.*').count()
        total_type_self_service_Two_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], job_name__regex=r'self_service.*').count()
        total_type_self_service_Last_7_Days = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=7), now], job_name__regex=r'self_service.*').count()
        total_type_self_service_Last_24_Hours = JobResult.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], job_name__regex=r'self_service.*').count()

        total_type_rest_api_Four_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=28), now - datetime.timedelta(days=21)], job_name__regex=r'rest_api.*').count()
        total_type_rest_api_Three_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=21), now - datetime.timedelta(days=14)], job_name__regex=r'rest_api.*').count()
        total_type_rest_api_Two_Weeks_Ago = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=14), now - datetime.timedelta(days=7)], job_name__regex=r'rest_api.*').count()
        total_type_rest_api_Last_7_Days = JobResult.objects.filter(time__range=[now - datetime.timedelta(days=7), now], job_name__regex=r'rest_api.*').count()
        total_type_rest_api_Last_24_Hours = JobResult.objects.filter(time__range=[now - datetime.timedelta(hours=24), now], job_name__regex=r'rest_api.*').count()

        """ LISTS FROM VARIABLES BUILT FROM QUERIES """
        ############################################################
        total_jobs = [total_jobs_Four_Weeks_Ago, total_jobs_Three_Weeks_Ago, total_jobs_Two_Weeks_Ago, total_jobs_Last_7_Days, total_jobs_Last_24_Hours]
        total_devices = [total_device_count_Four_Weeks_Ago, total_device_count_Three_Weeks_Ago, total_device_count_Two_Weeks_Ago, total_device_count_Last_7_Days, total_device_count_Last_24_Hours]
        total_completed = [completed_device_count_Four_Weeks_Ago, completed_device_count_Three_Weeks_Ago, completed_device_count_Two_Weeks_Ago, completed_device_count_Last_7_Days, completed_device_count_Last_24_Hours]
        total_failed = [failed_device_count_Four_Weeks_Ago, failed_device_count_Three_Weeks_Ago, failed_device_count_Two_Weeks_Ago, failed_device_count_Last_7_Days, failed_device_count_Last_24_Hours]

        # total different types of automation
        """ 
        for 
        self_service and 
        rest api (base this on regex and then on background worker, use self_service_<type, e.g. vxlan>) 
        """
        total_ad_hoc = [total_type_ad_hoc_Four_Weeks_Ago, total_type_ad_hoc_Three_Weeks_Ago, total_type_ad_hoc_Two_Weeks_Ago, total_type_ad_hoc_Last_7_Days, total_type_ad_hoc_Last_24_Hours]
        total_ndna = [total_type_ndna_Four_Weeks_Ago, total_type_ndna_Three_Weeks_Ago, total_type_ndna_Two_Weeks_Ago, total_type_ndna_Last_7_Days, total_type_ndna_Last_24_Hours]

        total_unique = [total_type_unique_Four_Weeks_Ago, total_type_unique_Three_Weeks_Ago, total_type_unique_Two_Weeks_Ago, total_type_unique_Last_7_Days, total_type_unique_Last_24_Hours]
        total_self_service = [total_type_self_service_Four_Weeks_Ago, total_type_self_service_Three_Weeks_Ago, total_type_self_service_Two_Weeks_Ago, total_type_self_service_Last_7_Days, total_type_self_service_Last_24_Hours]
        total_rest_api = [total_type_rest_api_Four_Weeks_Ago, total_type_rest_api_Three_Weeks_Ago, total_type_rest_api_Two_Weeks_Ago, total_type_rest_api_Last_7_Days, total_type_rest_api_Last_24_Hours]
        
        data = {
                "total_jobs": total_jobs,
                "total_devices": total_devices,
                "total_completed": total_completed,
                "total_failed": total_failed,

                "total_ad_hoc": total_ad_hoc,
                "total_ndna": total_ndna,
                "total_unique": total_unique,
                "total_self_service": total_self_service,
                "total_rest_api": total_rest_api,
        }

        return Response(data)
#################### ADMIN AREA FUNCTIONS #########################
""" IT'S GOT TO BE ALL LOWER CASE IN THE FORMAT 'app.permission_lowercasemodelname' """
@login_required
@permission_required('neural.add_t3', raise_exception=True)
def admin_manage_inventory(request):

    inventory = Device.objects.all()
        
    context = {
        'inventory': inventory,
    }

    """ delete devices from the database """
    if request.method == "POST" and 'btnform1' in request.POST:
        device = request.POST.getlist('device')
        for d in device:
            Device.objects.filter(hostname=d).delete()
    #return render(request, 'admin_manage_inventory.html', {'inventory': inventory})
    return render(request, 'admin_manage_inventory.html', context)

########################################
@login_required
@permission_required('neural.add_t3', raise_exception=True)
def admin_all_automation_output_configs(request):
    s =FileSystemStorage()
    files = list(get_files(s, location='configs'))

    """ download individual files """
    if request.method == "POST" and 'config' in request.POST:
            config = request.POST['config']

            fl = open(config, 'r')

            mime_type, _ = mimetypes.guess_type(config)
            response = HttpResponse(fl, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % config
            return response

    """ delete individual files """
    if request.method == "POST" and 'delete' in request.POST:

        delete = request.POST['delete']

        delete_config = r"""
        rm ./%s
        """ % delete
        subprocess.Popen(delete_config, shell=True, stdout=subprocess.PIPE)
    
    """ zipup and download all files """
    if request.method == "POST" and 'zipup' in request.POST:
        byte_data = BytesIO()
        zip_file = zipfile.ZipFile(byte_data, "w")

        for file in files:
            filename = os.path.basename(os.path.normpath(file))
            zip_file.write(file, filename)
        zip_file.close()

        response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=all_generated_configs.zip'

        # Print list files in zip_file
        zip_file.printdir()
        return response

    """ delete all files """
    if request.method == "POST" and 'all_files' in request.POST:
        try:
            for file in files:
                delete_all_configs = r"""
                rm ./%s 
                """ % file
                subprocess.Popen(delete_all_configs, shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            pass

    return render(request, 'automation_output_configs.html', {'files': files})
###############################
# this relates to PCAP files downloads system wide
###############################
from django.http import FileResponse

@login_required
#@permission_required('neural.add_t3', raise_exception=True)
def pcap_output_files(request):
    s =FileSystemStorage()
    files = list(get_files(s, location='tcpdump/pcaps'))

    ########################################
    directory = './tcpdump/pcaps'
    list1 = os.listdir(directory)
    sizes = []
    if list1 == []:
            context = {
                'files': files
            }
    else:
        for file in list1:
            location = os.path.join(directory, file)
            size = os.path.getsize(location)
            sizes.append((file, size))
            sizes.sort(key=lambda s: s[0])
                
            context = {
                'sizes': sizes,
                'files': files
            }
    ########################################

    """ download individual files """
    if request.method == "POST" and 'config' in request.POST:
        config = request.POST['config']

        response = FileResponse(open(config, 'rb'))
        
        response['Content-Disposition'] = "attachment; filename=%s" % config
        return response

     
    """ delete individual files """
    if request.method == "POST" and 'delete' in request.POST:

        delete = request.POST['delete']

        delete_config = r"""
        rm ./%s
        """ % delete
        subprocess.Popen(delete_config, shell=True, stdout=subprocess.PIPE)
    
    """ zipup and download all files """
    if request.method == "POST" and 'zipup' in request.POST:
        byte_data = BytesIO()
        zip_file = zipfile.ZipFile(byte_data, "w")

        for file in files:
            filename = os.path.basename(os.path.normpath(file))
            zip_file.write(file, filename)
        zip_file.close()

        response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=all_pcaps.zip'

        # Print list files in zip_file
        zip_file.printdir()
        return response

    """ delete all files """
    if request.method == "POST" and 'all_files' in request.POST:
        try:
            for file in files:
                delete_all_configs = r"""
                rm ./%s 
                """ % file
                subprocess.Popen(delete_all_configs, shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            pass

    #return render(request, 'pcap_output_files.html', {'files': files})
    return render(request, 'pcap_output_files.html', context)
###############################
# this relates to finished configs generated via jinja/csv vars merge
###############################
@login_required
@permission_required('neural.add_t3', raise_exception=True)
def admin_all_generated_config_files(request):
    s =FileSystemStorage()
    files = list(get_files(s, location='unique_automation'))

    """ download individual files """
    if request.method == "POST" and 'config' in request.POST:
        config = request.POST['config']
        fl = open(config, 'r')
        mime_type, _ = mimetypes.guess_type(config)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % config

        return response

    """ delete individual files """
    if request.method == "POST" and 'delete' in request.POST:

        delete = request.POST['delete']

        delete_config_template = r"""
        rm ./%s
        """ % delete
        subprocess.Popen(delete_config_template, shell=True, stdout=subprocess.PIPE)
    
    """ zipup and download all files """
    if request.method == "POST" and 'zipup' in request.POST:
        byte_data = BytesIO()
        zip_file = zipfile.ZipFile(byte_data, "w")

        for file in files:
            filename = os.path.basename(os.path.normpath(file))
            zip_file.write(file, filename)
        zip_file.close()

        response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=all_generated_config_templates.zip'

        # Print list files in zip_file
        zip_file.printdir()
        return response

    """ delete all files """
    if request.method == "POST" and 'all_files' in request.POST:
        try:
            for file in files:
                delete_all_configs = r"""
                rm ./%s 
                """ % file
                subprocess.Popen(delete_all_configs, shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            pass
    return render(request, 'admin_all_generated_config_files.html', {'files': files})
###############################

""" this relates to viewing/deleting all scheduled jobs from all users - part of admin area! """
###############################
@login_required
@permission_required('neural.add_t3', raise_exception=True)
def admin_view_all_scheduled_jobs(request):
    scheduler = django_rq.get_scheduler('default')

    #all_jobs = scheduler.get_jobs(with_times= True)
    all_jobs = scheduler.get_jobs()
    
    if request.method == "POST":
        cancel_job_with_uuid = request.POST['cancel_job_with_uuid']
        scheduler.cancel('%s' % cancel_job_with_uuid)
        return render(request, 'admin_view_all_scheduled_jobs.html', {'all_jobs': all_jobs})

    return render(request, 'admin_view_all_scheduled_jobs.html', {'all_jobs': all_jobs})
###############################
@login_required
@permission_required('neural.add_root', raise_exception=True)
def neural_backup_download(request):

    """ first copy backup to tmp directory """
    if request.method == "POST" and 'copy' in request.POST:
        COMMAND1 = r"""
        cd /var/www/django_app/mysite/
        python3 manage.py dbbackup
        sleep 2
        python3 manage.py mediabackup
        sleep 2
        cd /var/www/django_app/django_db_backups
        cp * /var/www/django_app/mysite/backup_download_tmp/
        sleep 5
        """
        subprocess.Popen(COMMAND1, shell=True, stdout=subprocess.PIPE)

 
    """ zipup and download all files """
    if request.method == "POST" and 'zipup' in request.POST:
        s =FileSystemStorage()
        files = list(get_files(s, location='backup_download_tmp'))
        byte_data = BytesIO()
        zip_file = zipfile.ZipFile(byte_data, "w")

        for file in files:
            filename = os.path.basename(os.path.normpath(file))
            zip_file.write(file, filename)
        zip_file.close()

        response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=full_neural_backup.zip'

        COMMAND2 = r"""
        cd /var/www/django_app/mysite/backup_download_tmp/
        rm *
        sleep 2
        """
        subprocess.Popen(COMMAND2, shell=True, stdout=subprocess.PIPE)

        # Print list files in zip_file
        zip_file.printdir()
        return response

    return render(request, 'neural_backup_download.html')
########## end of admin area functions #########################

from avi.sdk.avi_api import ApiSession
#####################################
import requests
import json
import pprint
from django.http import JsonResponse
#####################################################################
@login_required
def ad_hoc_unique_automation(request):
    form = DateForm()
    username = request.user.username
    
    if request.method == "POST" and 'btnform1' in request.POST:
        time_sleep = request.POST['time_sleep']
        command_sleep=int(time_sleep)

        nodes_list = request.POST['nodes_list'].splitlines()
        command_list = request.POST['command_list'].splitlines()
        
        ############################################
        """ cleanup any and all files before running job """
        FILECLEANUP = r"""
        rm ./ad_hoc_unique/configs/%s/*
        rm ./ad_hoc_unique/nodes/%s/*
        rm ./ad_hoc_unique/parsing_output/configs/%s/configs
        rm ./ad_hoc_unique/parsing_output/nodes/%s/nodes
        """%(username,username,username,username)

        subprocess.Popen(FILECLEANUP, shell=True, stdout=subprocess.PIPE)
        time.sleep(3)
        ############################################
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        if not os.path.exists('./ad_hoc_unique/configs/%s' %username):
            os.makedirs('./ad_hoc_unique/configs/%s' %username)
        else:
            pass

        if not os.path.exists('./ad_hoc_unique/nodes/%s' %username):
            os.makedirs('./ad_hoc_unique/nodes/%s' %username)
        else:
            pass

        if not os.path.exists('./ad_hoc_unique/parsing_output/configs/%s' %username):
            os.makedirs('./ad_hoc_unique/parsing_output/configs/%s' %username)
        else:
            pass

        if not os.path.exists('./ad_hoc_unique/parsing_output/nodes/%s' %username):
            os.makedirs('./ad_hoc_unique/parsing_output/nodes/%s' %username)
        else:
            pass

        count = 0   #### start here and start to work thru it in the interpreter
        ##############
        for node in nodes_list:
            count += 1
            filename = './ad_hoc_unique/nodes/{0}/{1}'.format(username,count)  
            with open(filename, 'w') as f:      
                    f.write('{}\n'.format(node))

        node_file_pre_integer = os.listdir('./ad_hoc_unique/nodes/{0}/'.format(username))
        node_integer_map = map(int, node_file_pre_integer)
        node_integer_list = list(node_integer_map)
        node_integer_list.sort(key=int)
        time.sleep(0.5)

        for each_file in node_integer_list:
            write_file = subprocess.Popen(["cat ./ad_hoc_unique/nodes/{0}/{1} >> ./ad_hoc_unique/parsing_output/nodes/{2}/nodes".format(username, each_file, username)], stdout=subprocess.PIPE, shell=True)
            time.sleep(0.5)
            #continue
        ##############
        ##############
        for command_set in command_list:
            count += 1
            filename = './ad_hoc_unique/configs/{0}/{1}'.format(username, count)
            with open(filename, 'w') as f:      
                    f.write('{}\n'.format(command_set))

        COMMAND1 = r"""
        sed -i 's/,/\n/g' ./ad_hoc_unique/configs/%s/*
        """% username

        subprocess.Popen(COMMAND1, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)
        ##############
        ### still need to work on below and probably above on for command_set in
        config_list_pre_integer = os.listdir('./ad_hoc_unique/configs/{0}'.format(username))
        config_list_integer_map = map(int, config_list_pre_integer)
        config_list= list(config_list_integer_map)
        config_list.sort(key=int)
        time.sleep(0.5)

        config_file = './ad_hoc_unique/parsing_output/configs/%s/configs' % username
        fo1 = open(config_file, "w")

        """ must now convert int back to string before writing to file to paste into csv later """
        config_list_str=map(str, config_list)

        for each_line in config_list_str:
            fo1.write(each_line + '\n')
            continue

        fo1.close()
        ##############
        ##############
        PASTE_COMMAND = r"""
        paste ./ad_hoc_unique/parsing_output/nodes/%s/nodes ./ad_hoc_unique/parsing_output/configs/%s/configs > ./ad_hoc_unique/pre_roll_to_network
        """%(username,username)
        
        subprocess.Popen(PASTE_COMMAND, shell=True, stdout=subprocess.PIPE)

        time.sleep(2)
        ##############
        ##############
        REMOVE_WHITESPACE_FROM_CFG_FILES = r"""
        sed -i 's/^ *//g' ./ad_hoc_unique/configs/%s/*
        """% username

        subprocess.Popen(REMOVE_WHITESPACE_FROM_CFG_FILES, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)
        ##############
        ##############
        FINAL_CSV_COMMAND = r"""
        cat ./ad_hoc_unique/pre_roll_to_network | awk {'print $1","$2'} > ./ad_hoc_unique/roll_to_network.csv
        """
        subprocess.Popen(FINAL_CSV_COMMAND, shell=True, stdout=subprocess.PIPE)
        time.sleep(2)
        ##############
        ##############
        with open('./ad_hoc_unique/roll_to_network.csv', mode='r') as infile:
            reader = csv.reader(infile)
            time.sleep(2)
            node_config = {rows[0]:rows[1] for rows in reader}
            #print(node_config)

            job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_unique_automation', user='%s' % username, total_device_count=len(node_config))

            ad_hoc_unique_automation_ssh_entry_point.delay(username, command_sleep, node_config, job_result, job_id=str(job_result.job_id))

            """ progress bar status page and results """
            return redirect('automation_results', job_id = job_result.pk)

    if request.method == "POST" and 'btnform2' in request.POST:
        form = DateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            datetime_field = data['datetime_field']

            time_sleep = request.POST['time_sleep']
            command_sleep=int(time_sleep)

            nodes_list = request.POST['nodes_list'].splitlines()
            command_list = request.POST['command_list'].splitlines()

            ############################################
            """ cleanup any and all files before running job """
            FILECLEANUP = r"""
            rm ./ad_hoc_unique/configs/%s/*
            rm ./ad_hoc_unique/nodes/%s/*
            rm ./ad_hoc_unique/parsing_output/configs/%s/configs
            rm ./ad_hoc_unique/parsing_output/nodes/%s/nodes
            """%(username,username,username,username)

            subprocess.Popen(FILECLEANUP, shell=True, stdout=subprocess.PIPE)
            time.sleep(2)
            ############################################

            if not os.path.exists('./configs/%s' %username):
                os.makedirs('./configs/%s' %username)
            else:
                pass

            if not os.path.exists('./ad_hoc_unique/configs/%s' %username):
                os.makedirs('./ad_hoc_unique/configs/%s' %username)
            else:
                pass

            if not os.path.exists('./ad_hoc_unique/nodes/%s' %username):
                os.makedirs('./ad_hoc_unique/nodes/%s' %username)
            else:
                pass

            if not os.path.exists('./ad_hoc_unique/parsing_output/configs/%s' %username):
                os.makedirs('./ad_hoc_unique/parsing_output/configs/%s' %username)
            else:
                pass

            if not os.path.exists('./ad_hoc_unique/parsing_output/nodes/%s' %username):
                os.makedirs('./ad_hoc_unique/parsing_output/nodes/%s' %username)
            else:
                pass

            count = 0   #### start here and start to work thru it in the interpreter
            ##############
            for node in nodes_list:
                count += 1
                filename = './ad_hoc_unique/nodes/{0}/{1}'.format(username,count)  
                with open(filename, 'w') as f:      
                        f.write('{}\n'.format(node))

            node_file_pre_integer = os.listdir('./ad_hoc_unique/nodes/{0}/'.format(username))
            node_integer_map = map(int, node_file_pre_integer)
            node_integer_list = list(node_integer_map)
            node_integer_list.sort(key=int)

            for each_line in node_integer_list:
                write_file = subprocess.Popen(["cat ./ad_hoc_unique/nodes/{0}/{1} >> ./ad_hoc_unique/parsing_output/nodes/{2}/nodes".format(username, each_line, username)], stdout=subprocess.PIPE, shell=True)
                continue
            ##############
            ##############
            for command_set in command_list:
                count += 1
                filename = './ad_hoc_unique/configs/{0}/{1}'.format(username, count)
                with open(filename, 'w') as f:      
                        f.write('{}\n'.format(command_set))

            COMMAND1 = r"""
            sed -i 's/,/\n/g' ./ad_hoc_unique/configs/%s/*
            """% username

            subprocess.Popen(COMMAND1, shell=True, stdout=subprocess.PIPE)
            time.sleep(5)
            ##############

            config_list_pre_integer = os.listdir('./ad_hoc_unique/configs/{0}'.format(username))
            config_list_integer_map = map(int, config_list_pre_integer)
            config_list= list(config_list_integer_map)
            config_list.sort(key=int)

            config_file = './ad_hoc_unique/parsing_output/configs/%s/configs' % username
            fo1 = open(config_file, "w")

            """ must now convert int back to string before writing to file to paste into csv later """
            config_list_str=map(str, config_list)

            for each_line in config_list_str:
                fo1.write(each_line + '\n')
                continue

            fo1.close()
            ##############
            ##############
            PASTE_COMMAND = r"""
            paste ./ad_hoc_unique/parsing_output/nodes/%s/nodes ./ad_hoc_unique/parsing_output/configs/%s/configs > ./ad_hoc_unique/pre_roll_to_network
            """%(username,username)
            
            subprocess.Popen(PASTE_COMMAND, shell=True, stdout=subprocess.PIPE)

            time.sleep(3)
            ##############
            ##############
            REMOVE_WHITESPACE_FROM_CFG_FILES = r"""
            sed -i 's/^ *//g' ./ad_hoc_unique/configs/%s/*
            """% username

            subprocess.Popen(REMOVE_WHITESPACE_FROM_CFG_FILES, shell=True, stdout=subprocess.PIPE)
            time.sleep(3)
            ##############
            ##############
            FINAL_CSV_COMMAND = r"""
            cat ./ad_hoc_unique/pre_roll_to_network | awk {'print $1","$2'} > ./ad_hoc_unique/roll_to_network.csv
            """
            subprocess.Popen(FINAL_CSV_COMMAND, shell=True, stdout=subprocess.PIPE)
            time.sleep(3)
            ##############
            ##############
            with open('./ad_hoc_unique/roll_to_network.csv', mode='r') as infile:
                reader = csv.reader(infile)
                time.sleep(2)
                node_config = {rows[0]:rows[1] for rows in reader}
                #print(node_config)

                job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='ad_hoc_unique_automation', user='%s' % username, total_device_count=len(node_config))
                job_id = job_result.pk

                scheduler = django_rq.get_scheduler('default')

                job = scheduler.enqueue_at(datetime_field, ad_hoc_unique_automation_ssh_entry_point, username, command_sleep, node_config, job_result, job_id=str(job_result.job_id))
                
                job_result.status='scheduled'
                job_result.save()

                """ dynamic scheduled job results """
                return redirect('scheduled', job_id)

    return render(request, 'ad_hoc_unique_automation.html', {'form': form})
###############################
@login_required
#@permission_required('neural.add_t3', raise_exception=True)
def user_disk_usage(request):
    ducommand = r"""
    du -h ./configs/ > du.log
    """
    subprocess.Popen(ducommand, shell=True, stdout=subprocess.PIPE)
    time.sleep(2)

    user_disk_usage = open('du.log').readlines()
    user_disk_usage = list(map(lambda x:x.strip(),user_disk_usage))

    return render(request, 'user_disk_usage.html', {'user_disk_usage': user_disk_usage})

########################################
@login_required
def neural_python_interpreter(request):
    return render(request, 'neural_python_interpreter.html')
########################################

################################################################################
####### Upload SCP Files file #######
class UploadSCPFiles(CreateView):
    model = SCP
    form_class = SCPForm
    success_url = reverse_lazy('scp_file_upload_to_neural')
    template_name = 'scp_upload_page.html'

########################################
@login_required
def delete_scp_file(request, pk):
    if request.method == 'POST':
        scp_files = SCP.objects.get(pk=pk)
        scp_files.delete()
    return redirect('scp_file_upload_to_neural')

####### Main SCP Upload File View for Cisco IOS using Netmiko still in testing phase #######
@login_required
def scp_file_upload_to_neural(request):
    username = request.user.username
    scp_files = SCP.objects.all()
    #csvvars = os.listdir('inventoryfiles')  
    scpfiles = os.listdir('scpfiles')

    if request.method == "POST" and 'scp_upload' in request.POST:
        #inventorycsv = request.POST['inventorycsv']
        node = request.POST['node']
        scpupload = request.POST['scpupload']
        remote_path = request.POST['remote_path']

        job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='self_service_scp_uploads', user='%s' % username, total_device_count=1)

        scp_file_upload.delay(username, node, scpupload, remote_path, job_result, job_id=str(job_result.job_id))

        return render(request, 'SCP_Success_Page.html') # Note on page that the job is submitted and to track it via redis job queue

        """ except Exception as e:
            message = e
            return render(request, 'SCP_Failure_Page.html', {'message': message }) """

    if request.method == "POST" and 'scp_nxos_upload' in request.POST:
        node = request.POST['node']
        scpupload = request.POST['scpupload']
        remote_path = request.POST['remote_path']

        job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='self_service_scp_uploads', user='%s' % username, total_device_count=1)

        scp_nxos_file_upload.delay(username, node, scpupload, remote_path, job_result, job_id=str(job_result.job_id))

        return render(request, 'SCP_Success_Page.html') # Note on page that the job is submitted and to track it via redis job queue


        """ except Exception as e:
            message = e
            return render(request, 'SCP_Failure_Page.html', {'message': message }) """

    return render(request, 'scp_file_upload_to_neural.html', {'scp_files': scp_files, 'scpfiles': scpfiles })
################################################################################
####### Main SCP Upload File View #######
from scp import SCPClient

@login_required
def scp_file_upload_to_neural_for_linux(request):
    scp_files = SCP.objects.all()
    #csvvars = os.listdir('inventoryfiles')  
    scpfiles = os.listdir('scpfiles')

    if request.method == "POST" and 'scp_upload' in request.POST:
        #inventorycsv = request.POST['inventorycsv']
        node = request.POST['node']
        scpupload = request.POST['scpupload']
        remote_path = request.POST['remote_path']

        try:
            """ svcacct_username is used to connect to the network """
            svcacct_username = 'svcacct-netbrains'
            svcacct_password = svcacct.objects.filter(username='svcacct-netbrains')

            for p in svcacct_password:
                password = p.password

            session = paramiko.SSHClient()
            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            session.load_system_host_keys()
            session.connect(node, username = svcacct_username, password = password, look_for_keys=False)

            # SCPCLient takes a paramiko transport as an argument
            scp = SCPClient(session.get_transport())
            #scp.put('test.html', 'test2.txt')
            #scp.get('test2.txt')

            #scp.put('test.html', recursive=True, remote_path='/var/www/')
            scp.put('./scpfiles/%s' %scpupload, recursive=True, remote_path=remote_path) 
            scp.close()

            return render(request, 'SCP_Success_Page.html')

        except Exception as e:
            message = e
            return render(request, 'SCP_Failure_Page.html', {'message': message })

    return render(request, 'scp_file_upload_to_neural.html', {'scp_files': scp_files, 'scpfiles': scpfiles })
################################################################################
################################################################################
@login_required
def compliance_golden_configs(request):
    username = request.user.username
    golden_configs = os.listdir('golden_configs')  

    """ write golden config to the database and to a flat file from web/template form """
    if request.method == "POST" and 'btnform1' in request.POST:
        import_golden_config_post = request.POST['goldenconfig'].splitlines()
        import_golden_config_to_db = request.POST['goldenconfig']
        device_type = request.POST['device_type']

        """ write to flat file first for diffing later """
        export_file_name = './golden_configs/%s' % device_type
        fo_export = open(export_file_name, "w")

        for line in import_golden_config_post:
            fo_export.write("%s\n" % line)
            continue
        fo_export.close()
        time.sleep(2)

        """ write to database for viewing in browser WITHOUT SPLITLINES """
        # check to see if exists in the db first, if so, update config, if not, create a new entry
        check_inventory = GoldenConfig.objects.filter(device_platform='%s' % device_type)
        if not check_inventory:
            goldenconfig=GoldenConfig.objects.create(device_platform=device_type, config=import_golden_config_to_db, submitted_by_user='%s' % username)
            #goldenconfig.config = import_golden_config_post
            goldenconfig.save()
        else:
            update_inventory = GoldenConfig.objects.filter(device_platform='%s' % device_type).update(config=import_golden_config_to_db, submitted_by_user='%s' % username)

        golden_configs = os.listdir('golden_configs')  

        return render(request, 'compliance_landing_page.html', {'golden_configs': golden_configs })

    """ write golden config to the database and to a flat file from web/template form """
    if request.method == "POST" and 'btnform10' in request.POST:
        device_platform = request.POST['device_platform']

        """ delete from database and file system """
        goldenconfig=GoldenConfig.objects.filter(device_platform=device_platform).delete()

        delete_gc = r"""
        rm ./golden_configs/%s
        """% (device_platform)

        subprocess.Popen(delete_gc, shell=True, stdout=subprocess.PIPE)

        golden_configs = os.listdir('golden_configs')  

        return render(request, 'compliance_landing_page.html', {'golden_configs': golden_configs })

    """ load up golden config from the database file system web/template form """
    if request.method == "POST" and 'btnform2' in request.POST:
        device_platform = request.POST['device_platform']

        gc_output = GoldenConfig.objects.filter(device_platform=device_platform).values_list('config', flat=True)  
    
        golden_configs = os.listdir('golden_configs')  

        context = {
            'golden_configs': golden_configs,
            'gc_output': gc_output,
        }

        return render(request, 'compliance_landing_page.html', context)

    """ Run Compare Diff from live environment  """
    if request.method == "POST" and 'btnform3' in request.POST:
        nodes_list = request.POST['nodes_list'].splitlines() # Grab live node config to compare against golden config
        device_platform = request.POST['device_platform']    # golden config - read from flat file 

        request.session['device_platform'] = device_platform # set 'device_platform var' in the session
        request.session['nodes_list'] = nodes_list # set 'node var' in the session

        # Make sure this is in all automation views!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        if len(nodes_list) > 1:
            job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='self_service_compliance_check', user='%s' % username, total_device_count=len(nodes_list))
            ########################################################################################################
            multi_node_compliance_check_ssh_entry_point.delay(device_platform, username, nodes_list, job_result, job_id=str(job_result.job_id))
            ########################################################################################################
            return redirect('automation_results', job_id = job_result.pk)
            #return redirect('multi_node_compliance_automation_results', job_id = job_result.pk)

        else:
            job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='self_service_compliance_check', user='%s' % username, total_device_count=len(nodes_list))
            ########################################################################################################
            compliance_check_ssh_entry_point.delay(username, nodes_list, job_result, job_id=str(job_result.job_id))
            ########################################################################################################

            return redirect('compliance_automation_results', job_id = job_result.pk)
            #gc_output_for_diffs = GoldenConfig.objects.filter(device_platform=device_platform).values_list('config', flat=True)  
            # could use this to render the golden config, then after list the diffs in another form box - just for view/reference before presenting diffs
            
    return render(request, 'compliance_landing_page.html', {'golden_configs': golden_configs })
########################################################################################################
@login_required
def display_all_golden_configs(request):
    gc_var = tabulate_qs(GoldenConfig.objects.all())
    return render(request, 'display_all_golden_configs.html', {'gc_var': gc_var })

#################################################
@login_required
def compliance_results(request):
    username = request.user.username

    device_platform = request.session['device_platform'] # get 'device_platform var' from the session
    gc_output_for_diffs = GoldenConfig.objects.filter(device_platform=device_platform).values_list('config', flat=True)  

    nodes_list = request.session['nodes_list'] # get 'node' var' from the session
    node_str = ''
    node = node_str.join(nodes_list)
    
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

    """ run diff and remove < from file """
    RUNDIFF = r"""
    diff ./golden_configs/%s ./golden_config_diffs/%s_compliance_check.txt > ./tmp/ooc.txt
    cat ./tmp/ooc.txt | grep \< > ./tmp/ooc_final.txt
    sed -i 's/<//' ./tmp/ooc_final.txt 
    """% (device_platform, node)

    subprocess.Popen(RUNDIFF, shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    ########################################################################################################
    # for diffs code to render in another form box
    diffs_pre_db = open('./tmp/ooc_final.txt', 'r').readlines()

    # initialize an empty string
    diff_str = " " 
    
    # return string  
    diffs_db = diff_str.join(diffs_pre_db)

    timeis = datetime.datetime.now()
    current_time = timeis.strftime("%m-%d-%Y-%H:%M")

    """ write to database for viewing in browser """
    diffs_db_write=GoldenConfigDiffs.objects.create(config=diffs_db, device_platform=device_platform + '_' + current_time)
    diffs_db_write.save()

    diffs = GoldenConfigDiffs.objects.filter(device_platform=device_platform + '_' + current_time).values_list('config', flat=True)  
    ########################################################################################################
    context = {
        'gc_output_for_diffs': gc_output_for_diffs,
        'diffs': diffs,
    }
    ########################################################################################################
    return render(request, 'compliance_results.html', context)

""" progress bar status page and results """
def compliance_automation_results(request, job_id):
    job_result = get_object_or_404(JobResult, pk=job_id)
    return render(request, 'compliance_automation_results.html', {'job_result': job_result})

""" compliance_automation_results.html jquery progress bar looks at the URL /jobresults/ which triggers 
    func return_job_results below to get data via JSON Response = (data) """

@login_required
def napalm_get_automation(request):
    username = request.user.username
    all_device = Device.objects.all()

    context = {
        'all_device': all_device,
    }

    if request.method == "POST" and 'btnform1' in request.POST:
        get_var = request.POST['get_var']
        nodes_list = request.POST.getlist('device')

        # Make sure this is in all automation views!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='self_service_napalm_get_automation', user='%s' % username, total_device_count=len(nodes_list))

        napalm_get_entry_point.delay(username, nodes_list, get_var, job_result, job_id=str(job_result.job_id))

        """ progress bar status page and results """
        return redirect('automation_results', job_id = job_result.pk)

    return render(request, 'napalm_get_automation.html', context)

from .neural_notebooks import *
@login_required
def neural_notebooks(request):
    username = request.user.username

    all_notebooks = NeuralNotebookParams.objects.all()

    context = {
        'all_notebooks': all_notebooks
    }

    if request.method == "POST" and 'btnform1' in request.POST:
        neural_notebook = request.POST['neural_notebook']
        neural_notebook_vars = request.POST['neural_notebook_vars'].splitlines()

        # Make sure this is in all automation views!
        if not os.path.exists('./configs/%s' %username):
            os.makedirs('./configs/%s' %username)
        else:
            pass

        job_result = JobResult.objects.create(job_id = uuid.uuid4(), job_name='self_service_neural_notebook_automation', user='%s' % username)
        """ globals() allow us to use a variable as the function callable name """
        globals()[neural_notebook].delay(username, neural_notebook_vars, job_result, job_id=str(job_result.job_id))
        
        """ progress bar status page and results """
        return redirect('automation_results', job_id = job_result.pk)

    """ load up a notebooks commands list/task names/config from the database  web/template form """
    if request.method == "POST" and 'btnform2' in request.POST:
        notebook_name = request.POST['notebook_name']

        notebook_command_list_output = NeuralNotebookParams.objects.filter(notebook_name=notebook_name).values_list('notebook_command_list', flat=True)  
    
        context = {
            'all_notebooks': all_notebooks,
            'notebook_command_list_output': notebook_command_list_output,
        }

        return render(request, 'neural_notebooks.html', context)

    """ load up a notebooks nodes list per job from the database  web/template form """
    if request.method == "POST" and 'btnform3' in request.POST:
        notebook_name = request.POST['notebook_name']

        notebook_nodes_list_output = NeuralNotebookParams.objects.filter(notebook_name=notebook_name).values_list('notebook_nodes_lists', flat=True)  
    
        context = {
            'all_notebooks': all_notebooks,
            'notebook_nodes_list_output': notebook_nodes_list_output,
        }

        return render(request, 'neural_notebooks.html', context)

    """ load up a notebooks variables per job from the database  web/template form """
    if request.method == "POST" and 'btnform5' in request.POST:
        notebook_name = request.POST['notebook_name']

        notebook_vars_output = NeuralNotebookParams.objects.filter(notebook_name=notebook_name).values_list('notebook_default_variables', flat=True)  
    
        context = {
            'all_notebooks': all_notebooks,
            'notebook_vars_output': notebook_vars_output,
        }
        return render(request, 'neural_notebooks.html', context)

    return render(request, 'neural_notebooks.html', context)
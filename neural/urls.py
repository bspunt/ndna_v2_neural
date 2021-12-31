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
from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views
from .views import monthly_log_stats, LogChartData, monthly_job_results_stats, JobResultsData

from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'device_inventory_api', views.DeviceViewSet)
router.register(r'golden_configs_api', views.GoldenConfigsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('neural_rest_api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('login/', auth_views.LoginView.as_view(), name ='login'),
    path('logout/', auth_views.LogoutView.as_view(), name ='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'), 
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', views.home, name ='home'),
    path('logs/', views.logs, name ='logs'),
    path('devices/', views.devices, name ='devices'),
    ###################
    path('inventory_templates/', views.inventory_templates, name='inventory_templates'),
    path('upload_inventory/', views.UploadInventory.as_view(), name='upload_inventory'),
    path('inventory_templates/<int:pk>/', views.delete_inventory_template, name='delete_inventory_template'),
    path('inventory_upload_single_device/', views.inventory_upload_single_device, name='inventory_upload_single_device'),
    path('inventory_csv_example/', views.inventory_csv_example, name='inventory_csv_example'),
    path('view_csv_variables_upload/', views.view_csv_variables_upload, name='view_csv_variables_upload'),

    # using nautobot style form for csv input w/ headers
    path('import_device_inventory/', views.import_device_inventory, name='import_device_inventory'),
    ###################
    ###################
    path('ad_hoc_automation/', views.ad_hoc_automation, name='ad_hoc_automation'),
    path('ad_hoc_automation_db_query/', views.ad_hoc_automation_db_query, name='ad_hoc_automation_db_query'),
    path('fw_ad_hoc_tcpdump_automation/', views.fw_ad_hoc_tcpdump_automation, name='fw_ad_hoc_tcpdump_automation'),
    path('pcap_output_files/', views.pcap_output_files, name='pcap_output_files'),
    ###################
    ###################
    path('unique_automation/', views.unique_automation, name='unique_automation'),
    path('unique_automation_manual_configs/', views.unique_automation_manual_configs, name='unique_automation_manual_configs'),
    path('manual_configs_upload/', views.manual_configs_upload, name='manual_configs_upload'),
    ###################
    path('scheduled/<int:job_id>/', views.scheduled, name ='scheduled'),
    path('view_all_scheduled_jobs', views.view_all_scheduled_jobs, name ='view_all_scheduled_jobs'),
    path('view_all_scheduled_times', views.view_all_scheduled_times, name ='view_all_scheduled_times'),
    ###################
    ###################
    path('automation_results/<int:job_id>', views.automation_results, name ='automation_results'),
    path('full_automation_results/<int:job_id>', views.full_automation_results, name ='full_automation_results'),

    path('fw_automation_results/<int:job_id>', views.fw_automation_results, name='fw_automation_results'),
    path('jobresults/<int:job_id>', views.return_job_results, name ='jobresults'),

    path('backup_results/<int:job_id>', views.backup_results, name ='backup_results'),
    ###################
    ###################
    path('automation_output_configs', views.automation_output_configs, name='automation_output_configs'),
    ###################
    ###################
    path('network_configs', views.network_configs, name='network_configs'),
    ###################
    ###################
    path('jinja2_templates', views.jinja2_templates, name='jinja2_templates'),
    path('csv_templates/', views.csv_templates, name='csv_templates'),
    path('csv_dl_reference_templates', views.csv_dl_reference_templates, name='csv_dl_reference_templates'),
    path('generate_config_templates/', views.generate_config_templates, name='generate_config_templates'),
    path('config_templates_example/', views.config_templates_example, name='config_templates_example'),
    path('generated_config_files/', views.generated_config_files, name='generated_config_files'),
    path('config_templates/<int:pk>/', views.delete_config_template, name='delete_config_template'),
    path('upload_config_templates/', views.UploadConfigTemplate.as_view(), name='upload_config_templates'),
    path('jinja_templates/', views.jinja_templates, name='jinja_templates'),
    path('jinja_config_templates/<int:pk>/', views.delete_jinja_template, name='delete_jinja_config_template'),
    path('upload_jinja_config_templates/', views.UploadJinjaTemplate.as_view(), name='upload_jinja_config_templates'),
    ###################
    ###################
    path('monthly_log_stats/', monthly_log_stats.as_view(), name='monthly_log_stats'),
    path('log_chart_data/', LogChartData.as_view(), name='log_chart_data'),
    
    path('all_job_results/', views.all_job_results, name ='all_job_results'),
    path('user_job_results/', views.user_job_results, name ='user_job_results'),
    ###################
    ###################
    path('monthly_job_results_stats/', monthly_job_results_stats.as_view(), name='monthly_job_results_stats'),
    path('job_results_chart_data/', JobResultsData.as_view(), name='job_results_chart_data'),
    ###################
    #### Admin Area URLs ####
    path('admin_manage_inventory/', views.admin_manage_inventory, name='admin_manage_inventory'),

    path('update_inventory_single_device', views.update_inventory_single_device, name='update_inventory_single_device'),
    path('update_inventory_templates', views.update_inventory_templates, name='update_inventory_templates'),

    path('admin_all_automation_output_configs/', views.admin_all_automation_output_configs, name='admin_all_automation_output_configs'),
    path('admin_all_generated_config_files/', views.admin_all_generated_config_files, name='admin_all_generated_config_files'),
    path('admin_view_all_scheduled_jobs', views.admin_view_all_scheduled_jobs, name ='admin_view_all_scheduled_jobs'),

    path('neural_backup_download', views.neural_backup_download, name ='neural_backup_download'),
    ###################
    #### Self Service Programs URLs ####
    ###################
    ###################
    path('ad_hoc_unique_automation', views.ad_hoc_unique_automation, name ='ad_hoc_unique_automation'),
    path('ad_hoc_automation_selected_devices', views.ad_hoc_automation_selected_devices, name ='ad_hoc_automation_selected_devices'),
    ###################
    ###################
    path('download_specific_files', views.download_specific_files, name ='download_specific_files'),
    ###################
    ###################
    path('user_disk_usage', views.user_disk_usage, name ='user_disk_usage'),
    ###################
    path('neural_python_interpreter', views.neural_python_interpreter, name ='neural_python_interpreter'),
    ###################
    ###################
    path('scp_file_upload_to_neural/', views.scp_file_upload_to_neural, name='scp_file_upload_to_neural'),
    path('upload_scp_file/', views.UploadSCPFiles.as_view(), name='upload_scp_file'),
    path('scp_file_upload_to_neural/<int:pk>/', views.delete_scp_file, name='delete_scp_file'),
    path('compliance_golden_configs', views.compliance_golden_configs, name='compliance_golden_configs'),
    path('compliance_results', views.compliance_results, name='compliance_results'),
    path('display_all_golden_configs', views.display_all_golden_configs, name='display_all_golden_configs'),
    path('compliance_automation_results/<int:job_id>', views.compliance_automation_results, name ='compliance_automation_results'),
    path('setup', views.setup, name='setup'),
    path('napalm_get_automation', views.napalm_get_automation, name='napalm_get_automation'),
    path('neural_notebooks', views.neural_notebooks, name='neural_notebooks'),
    ###################
]
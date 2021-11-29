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
from django import forms
import datetime
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.forms import ModelForm, Form
###############################################
# this is the bootstrap datetime widget
from bootstrap_datepicker_plus import DateTimePickerInput
class DateForm(forms.Form):
    datetime_field = forms.DateTimeField(widget=DateTimePickerInput)
###############################################

###############################################
from .models import Inventorie, Configtemplate, Jinjatemplate, SCP
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventorie
        fields = ('inventory_file_name', 'uploaded_by', 'inventory_csv')
class ConfigTemplatesForm(forms.ModelForm):
    class Meta:
        model = Configtemplate
        fields = ('csv_file_name', 'uploaded_by', 'csv_variables')
class JinjaTemplatesForm(forms.ModelForm):
    class Meta:
        model = Jinjatemplate
        fields = ('jinja_file_name', 'uploaded_by', 'jinja_template')
class SCPForm(forms.ModelForm):
    class Meta:
        model = SCP
        fields = ('scp_file_name', 'uploaded_by', 'scp_file')
###############################################
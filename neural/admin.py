
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

from django.contrib import admin
from .models import Device, Log, JobResult, Inventorie, Configtemplate, NDNANexusDevice, NDNAIOSDevice, NDNACDP, T3, root, svcacct, BwSlaJobResult, VRF, Jinjatemplate, SCP, GoldenConfig, GoldenConfigDiffs

# Register your models here.

admin.site.register(Device)
admin.site.register(Log)
admin.site.register(JobResult)
admin.site.register(Inventorie)
admin.site.register(Configtemplate)
admin.site.register(NDNANexusDevice)
admin.site.register(NDNAIOSDevice)
admin.site.register(NDNACDP)
admin.site.register(T3)
admin.site.register(root)
admin.site.register(svcacct)
admin.site.register(BwSlaJobResult)
admin.site.register(Jinjatemplate)
admin.site.register(VRF)
admin.site.register(SCP)
admin.site.register(GoldenConfig)
admin.site.register(GoldenConfigDiffs)
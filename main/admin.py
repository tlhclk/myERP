# -*- coding: utf-8 -*-
### import_part
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

### admin_part
admin.site.register(PanelLM)
admin.site.register(ModelLM)
admin.site.register(FieldLM)
admin.site.register(PathLM)
admin.site.register(PersonGroupLM)
admin.site.register(SchoolLM)
admin.site.register(CorporationLM)
admin.site.register(DepartmentLM)

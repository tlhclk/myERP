# -*- coding: utf-8 -*-
### import_part
from __future__ import unicode_literals
from django.contrib import admin
from .models import *


### admin_part
admin.site.register(PersonalPermission)
admin.site.register(MyUserProfile)
admin.site.register(MyGroup)
admin.site.register(UserGroup)
admin.site.register(HistoryLog)

# -*- coding: utf-8 -*-
### import_part
from __future__ import unicode_literals
from django.contrib import admin
from .models import *


### admin_part
admin.site.register(Event)
admin.site.register(Repetitive)
admin.site.register(RepetitiveRecord)

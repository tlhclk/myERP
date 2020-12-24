# -*- coding: utf-8 -*-
### import_part
from django.contrib import admin
from .models import *


### admin_part
admin.site.register(Currency)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Change)
admin.site.register(CurrencyHistory)

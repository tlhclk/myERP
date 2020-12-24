# -*- coding: utf-8 -*-
### import_part
from __future__ import unicode_literals
from django.contrib import admin
from .models import *


### admin_part
admin.site.register(ContinentLM)
admin.site.register(CountryLM)
admin.site.register(CityLM)
admin.site.register(TownLM)
admin.site.register(CardTypeLM)
admin.site.register(ChangePurposeLM)
admin.site.register(RepetitiveTypeLM)
admin.site.register(CorporationTypeLM)
admin.site.register(EmailTypeLM)
admin.site.register(EventTypeLM)
admin.site.register(GenderLM)
admin.site.register(MediaTypeLM)
admin.site.register(PeriodLM)
admin.site.register(PhoneTypeLM)
admin.site.register(RelationshipLM)
admin.site.register(SchoolTypeLM)
admin.site.register(SeriesDownloadLM)
admin.site.register(SeriesGenreLM)
admin.site.register(SeriesStateLM)
admin.site.register(SeriesTypeLM)
admin.site.register(TransactionCategoryLM)
admin.site.register(TransactionTypeLM)
admin.site.register(MarketLM)

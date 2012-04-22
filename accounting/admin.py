from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *

admin.site.register(Account, MPTTModelAdmin)
admin.site.register(Transaction)
admin.site.register(Vat)

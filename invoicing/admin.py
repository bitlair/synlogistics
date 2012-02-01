from django.contrib import admin
from .models import *

class InvoiceItemInline(admin.StackedInline):
    model = InvoiceItem
    extra = 0

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline]


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem)
admin.site.register(Subscription)

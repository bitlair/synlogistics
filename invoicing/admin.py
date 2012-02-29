from django.contrib import admin
from .models import *

class InvoiceItemInline(admin.StackedInline):
    model = InvoiceItem
    extra = 0

class TimeKeepingEntryInline(admin.StackedInline):
    model = TimeKeepingEntry
    extra = 0
    ordering = ['date']

class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceItemInline, TimeKeepingEntryInline]


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem)
admin.site.register(Subscription)
admin.site.register(TimeBillingRate)
admin.site.register(TimeKeepingEntry)

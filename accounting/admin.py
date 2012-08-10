from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Account, SubTransaction, Transaction, Vat


class SubTransactionInline(admin.TabularInline):
    model = SubTransaction
    extra = 0


class AccountAdmin(MPTTModelAdmin):
    list_display = ['__unicode__', 'account_type', 'balance']
    mptt_indent_field = '__unicode__'
    inlines = [SubTransactionInline]


class TransactionAdmin(admin.ModelAdmin):
    inlines = [SubTransactionInline]

admin.site.register(Account, AccountAdmin)
admin.site.register(SubTransaction)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Vat)

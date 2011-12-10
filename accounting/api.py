from tastypie.resources import ModelResource
from tastypie import fields
from main.api import DjangoAuth
from .models import *

class AccountResource(ModelResource):
    parent = fields.ForeignKey('self', 'parent', null=True)

    class Meta(DjangoAuth):
        queryset = Account.objects.all()
        excludes = ['_balance']

    def dehydrate(self, bundle):
        bundle.data['balance'] = bundle.obj.balance
        return bundle
        
class TransactionResource(ModelResource):
    account = fields.ForeignKey(AccountResource, 'account')

    class Meta(DjangoAuth):
        queryset = Transaction.objects.all()
        filtering = { "account": 'exact'}

class VatResource(ModelResource):
    account = fields.ForeignKey(AccountResource, 'account')

    class Meta(DjangoAuth):
        queryset = Vat.objects.all()

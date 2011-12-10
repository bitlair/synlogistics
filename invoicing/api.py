from tastypie.resources import ModelResource
from tastypie import fields
from main.api import DjangoAuth
from .models import *

class InvoiceResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = Invoice.objects.all()

class InvoiceItemResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = InvoiceItem.objects.all()

class SubscriptionResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = Subscription.objects.all()

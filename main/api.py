from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication
from .models import *

class DjangoAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        if request.user.is_authenticated():
            return True

        return False

    def get_identifier(self, request):
        return request.user.username

class DjangoAuth:
    authentication = DjangoAuthentication()
    authorization = DjangoAuthorization()

class RelationResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = Relation.objects.all()

class ContactResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = Contact.objects.all()

class PurchaseOrderResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = PurchaseOrder.objects.all()

class LocationResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = Location.objects.all()

class ProductGroupResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = ProductGroup.objects.all()

class ProductResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = Product.objects.all()

class SubproductResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = Subproduct.objects.all()

class InternalOrderResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = InternalOrder.objects.all()

class PurchaseOrderItemResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = PurchaseOrderItem.objects.all()

class ItemResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = Item.objects.all()

class ContainerResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = Container.objects.all()

class ContainerItemResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = ContainerItem.objects.all()

class ContainerTemplateResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = ContainerTemplate.objects.all()

class InventoryResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = Inventory.objects.all()

class ProductSellingpriceResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = ProductSellingprice.objects.all()

class BookingPeriodResource(ModelResource):
    class Meta(DjangoAuth):
        queryset = BookingPeriod.objects.all()


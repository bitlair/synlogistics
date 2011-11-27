from django.contrib import admin
from .models import *

admin.site.register(Relation)
admin.site.register(Contact)
admin.site.register(PurchaseOrder)
admin.site.register(Location)
admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(Subproduct)
admin.site.register(InternalOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(Item)
admin.site.register(Container)
admin.site.register(ContainerItem)
admin.site.register(ContainerTemplate)
admin.site.register(Inventory)
admin.site.register(InventoryItem)
admin.site.register(ProductSellingprice)
admin.site.register(BookingPeriod)
admin.site.register(Settings)
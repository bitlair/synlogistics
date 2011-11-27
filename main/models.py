"""
SynLogistics database model
"""
#
# Copyright (C) by Wilco Baan Hofman <wilco@baanhofman.nl> 2011
#   
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#   
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#   
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

 
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Relation(models.Model):
    """ Relations: customers, members or suppliers """
    displayname = models.CharField(unique=True, max_length=180, blank=False)
    visit_address = models.CharField(max_length=180, blank=True, default='')
    visit_postalcode_zip = models.CharField(max_length=30, blank=True, null=True)
    visit_city = models.CharField(max_length=180, blank=True, null=True)
    visit_country = models.CharField(max_length=180, blank=True, null=True)
    postal_address = models.CharField(max_length=180, blank=True)
    postal_code_zip = models.CharField(max_length=30, blank=True)
    postal_city = models.CharField(max_length=180, blank=True)
    postal_country = models.CharField(max_length=180, blank=True)
    email = models.CharField(max_length=180, blank=True)
    phone1 = models.CharField(max_length=60, blank=True)
    phone2 = models.CharField(max_length=60, blank=True)
    active_customer = models.BooleanField(default=True)
    active_supplier = models.BooleanField(default=False)
    invoice_name = models.CharField(max_length=180, blank=True)
    invoice_contact = models.ForeignKey('Contact', blank=False, related_name='+')
    invoice_by_email = models.BooleanField(default=True)
    invoice_email = models.CharField(max_length=180, blank=True)
    notes = models.TextField(blank=True)
    class Meta:
        """ Metadata """
        db_table = u'relations'

class Contact(models.Model):
    """ Contacts per relation """
    relation = models.ForeignKey(Relation, related_name='contacts')
    displayname = models.CharField(max_length=180, blank=False)
    givenname = models.CharField(max_length=75, blank=True)
    infix = models.CharField(max_length=75, blank=True)
    surname = models.CharField(max_length=180, blank=True)
    phone = models.CharField(max_length=60, blank=True)
    mobilephone = models.CharField(max_length=60, blank=True)
    email = models.CharField(max_length=180, blank=True)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    class Meta:
        """ Metadata """
        db_table = u'contacts'

class PurchaseOrder(models.Model):
    """ External purchase order """
    purchasing_date = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(Relation, related_name='purchase_orders')
    order_method = models.IntegerField(null=True, blank=True)
    relation_contact = models.ForeignKey(Contact, related_name='purchase_orders')
    external_order_reference = models.CharField(max_length=90, blank=True)
    class Meta:
        """ Metadata """
        db_table = u'purchase_orders'

class Location(models.Model):
    """ Location: point of sale, storage, warehouse, etc """
    name = models.CharField(max_length=180, blank=True)
    address = models.CharField(max_length=180, blank=True)
    postalzip = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=180, blank=True)
    country = models.CharField(max_length=180, blank=True)
    phone = models.CharField(max_length=60, blank=True)
    location_type = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    class Meta:
        """ Metadata """
        db_table = u'locations'

class ProductGroup(models.Model):
    """ Product groups """
    name = models.CharField(unique=True, max_length=255, blank=False)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    class Meta:
        """ Metadata """
        db_table = u'product_groups'

class Product(models.Model):
    """ Products you trade with """
    TYPE_CHOICES = (
        (00, 'Hardware'),
        (01, 'Service'),
        (02, 'Periodic'))
    INTERVAL_CHOICES = (
        (00, 'Daily'),
        (01, 'Weekly'),
        (02, 'Monthly'),
        (03, 'Quarterly'),
        (04, 'Annually'))
    product_type = models.IntegerField(null=False, choices=TYPE_CHOICES)
    product_group = models.ForeignKey(ProductGroup, related_name='products', null=False)
    code = models.CharField(unique=True, max_length=120, blank=False)
    name = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    minimum_stock = models.IntegerField(null=True, blank=True)
    maximum_stock = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    # Vat is done as a string because of recursive import issues
    vat = models.ForeignKey('accounting.Vat', related_name='products', null=True)  
    has_own_serials = models.BooleanField(default=True)
    invoice_interval = models.IntegerField(null=True, choices=INTERVAL_CHOICES)
    invoice_interval_count = models.IntegerField(null=True, default=1)

    def get_price(self, date=None):
        """ Get the active price for a given date or now.. """
        if date == None:
            date = datetime.utcnow()
    
        price = ProductSellingprice.objects.raw("SELECT s1.* FROM product_sellingprices s1 " +
                "LEFT JOIN product_sellingprices s2 ON s1.product_id=s2.product_id " +
                "AND s1.commencing_date < s2.commencing_date " +
                "WHERE s2.commencing_date IS NULL AND s1.product_id=%s", [ self.id ])
        for p in price:
            return p.price
        return None
        

    class Meta:
        """ Metadata """
        db_table = u'products'

class Subproduct(models.Model):
    """ Specific product, like "High-End 48p 10GbE Switch" -> "Arista 7148S" or "Linksys WRT54g" -> "Linksys WRT54g rev. 3". """
    product = models.ForeignKey(Product, related_name='subproducts')
    ean_upc_code = models.CharField(unique=True, max_length=180, blank=False)
    name = models.CharField(max_length=300, blank=False)
    class Meta:
        """ Metadata """
        db_table = u'subproducts'

class InternalOrder(models.Model):
    """ Internal ordering for things that are to be purchased externally, kind of like an order queue. """
    state = models.IntegerField(null=True, blank=True)
    sale_order_date = models.DateTimeField(null=True, blank=True)
    ordered_by_user = models.ForeignKey(User, related_name='internal_orders')
    amount_needed = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey(Product, related_name='internal_orders')
    product_group = models.ForeignKey(ProductGroup, related_name='internal_orders')
    product_description = models.CharField(max_length=300, blank=True)
    purchase_price_indication = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
    selling_price = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
    supplier_suggestion = models.ForeignKey(Relation, related_name='+')
    for_customer = models.BooleanField(default=False)
    customer = models.ForeignKey(Relation, related_name='internal_orders')
    customer_reference = models.CharField(max_length=180, blank=True)
    class Meta:
        """ Metadata """
        db_table = u'internal_order'

class PurchaseOrderItem(models.Model):
    """ Purchase Order contents """
    purchase_order = models.ForeignKey(PurchaseOrder, related_name='data')
    internal_order = models.ForeignKey(InternalOrder, related_name='purchase_data')
    state = models.IntegerField(null=True, blank=True)
    purchase_price = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
    order_amount = models.IntegerField(null=True, blank=True)
    units_per_pack = models.IntegerField(null=True, blank=True)
    subproduct = models.ForeignKey(Subproduct, related_name='purchase_data')
    supplier_has_in_stock = models.BooleanField(default=False)
    expected_date = models.DateField(null=True, blank=True)
    class Meta:
        """ Metadata """
        db_table = u'purchase_order_data'

class Item(models.Model):
    """ Individual units that are in stock. """
    serial_number = models.CharField(unique=True, max_length=180, blank=False)
    purchase_order_data = models.ForeignKey(PurchaseOrderItem, related_name='items')
    input_by_user = models.ForeignKey(User, related_name='items_input')
    reserved = models.BooleanField(default=False)
    reserved_for_relation = models.ForeignKey(Relation, related_name='items_reserved')
    reserved_by_user = models.ForeignKey(User, related_name='items_reserved')
    reserved_date = models.DateTimeField(null=True, blank=True)
    sold = models.BooleanField(default=False)
    written_off = models.BooleanField(default=False)
    written_off_by_user = models.ForeignKey(User, related_name='items_writtenoff')
    location = models.ForeignKey(Location, related_name='items')
    arrival_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        """ Metadata """
        db_table = u'items'

class Container(models.Model):
    """ Specific containers that contain multiple items """
    container_number = models.CharField(unique=True, max_length=180, blank=False)
    name = models.CharField(max_length=180, blank=True)
    container_template = models.IntegerField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    display_contents = models.IntegerField(null=True, blank=True)
    sold = models.IntegerField(null=True, blank=True)
    class Meta:
        """ Metadata """
        db_table = u'containers'

class ContainerItem(models.Model):
    """ Item inside a container """
    container = models.ForeignKey(Container, related_name='data')
    item = models.ForeignKey(Item, related_name='container_data')
    added_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        """ Metadata """
        db_table = u'container_data'

class ContainerTemplate(models.Model):
    """ Template for specifying/ordering what should be in a container """
    name = models.CharField(unique=True, max_length=255, blank=False)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    products = models.ManyToManyField('product', symmetrical=False)
    class Meta:
        """ Metadata """
        db_table = u'container_templates'


class Inventory(models.Model):
    """ Stock inventory counts """
    date = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)
    class Meta:
        """ Metadata """
        db_table = u'inventories'

class InventoryItem(models.Model):
    """ Stock inventory contents """
    inventory = models.ForeignKey('Inventory', related_name='data')
    item = models.ForeignKey(Item, related_name='item')
    location = models.ForeignKey(Location, related_name='+')
    value = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
    class Meta:
        """ Metadata """
        db_table = u'inventory_data'


class ProductSellingprice(models.Model):
    """ Active selling prices of products for given dates. """
    product = models.ForeignKey(Product, related_name='sellingprices')
    commencing_date = models.DateField(null=False)
    set_date = models.DateField(null=False)
    price = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
    class Meta:
        """ Metadata """
        db_table = u'product_sellingprices'

class BookingPeriod(models.Model):
    number = models.IntegerField(null=False, db_index=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    class Meta:
        """ Metadata """
        db_table = u'booking_periods'
    

class Settings(models.Model):
    """ SynLogistics application settings """
    invoice_format_string = models.CharField(max_length=60, null=False, blank=False)
    letterhead_paper_path = models.CharField(max_length=180, null=False, blank=False)
    periodic_accounts_receivable = models.CharField(max_length=180, null=False, blank=False)
    class Meta:
        """ Metadata """
        db_table = u'settings'

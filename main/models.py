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
from django.db.models import Sum
	

class Relation(models.Model):
	""" Relations: customers, members or suppliers """
	displayname = models.CharField(unique=True, max_length=180, blank=False)
	address = models.CharField(max_length=180, blank=True)
	postalzip = models.CharField(max_length=30, blank=True)
	city = models.CharField(max_length=180, blank=True)
	country = models.CharField(max_length=180, blank=True)
	email = models.CharField(max_length=180, blank=True)
	phone1 = models.CharField(max_length=60, blank=True)
	phone2 = models.CharField(max_length=60, blank=True)
	active_customer = models.BooleanField(default=True)
	active_supplier = models.BooleanField(default=False)
	invoice_by_email = models.BooleanField(default=True)
	invoice_email = models.CharField(max_length=180, blank=True)
	notes = models.TextField(blank=True)
	class Meta:
		""" Metadata """
		db_table = u'relations'

class Contact(models.Model):
	""" Contacts per relation """
	relation = models.ForeignKey(Relation)
	givenname = models.CharField(max_length=75, blank=True)
	infix = models.CharField(max_length=75, blank=True)
	surname = models.CharField(max_length=180, blank=True)
	phone = models.CharField(max_length=60, blank=True)
	mobilephone = models.CharField(max_length=60, blank=True)
	notes = models.TextField(blank=True)
	active = models.BooleanField(default=True)
	class Meta:
		""" Metadata """
		db_table = u'contacts'

class PurchaseOrder(models.Model):
	""" External purchase order """
	purchasing_date = models.DateTimeField(null=True, blank=True)
	customer = models.ForeignKey(Relation)
	order_method = models.IntegerField(null=True, blank=True)
	relation_contact = models.ForeignKey(Contact)
	external_order_reference = models.CharField(max_length=90, blank=True)
	class Meta:
		""" Metadata """
		db_table = u'purchase_orders'

class Account(models.Model):
	""" Accounting ledger account """
	TYPE_CHOICES = (
		(00, 'Assets'),
		(01, 'Accounts receivable'),
		(02, 'Bank account'),
		(03, 'Cash'),
		(04, 'Stock'),
		(10, 'Liabilities'),
		(11, 'Accounts payable'),
		(12, 'Credit card'),
		(20, 'Equity'),
		(40, 'Expenses'),
		(80, 'Income'))
	number = models.CharField(unique=True, max_length=24, blank=False)
	name = models.CharField(max_length=180, blank=False)
	description = models.CharField(max_length=765, blank=True)
	account_type = models.IntegerField(null=False, blank=False, choices=TYPE_CHOICES)
	is_readonly = models.BooleanField(null=False, default=False)
	_balance = models.DecimalField(decimal_places=5, max_digits=25, null=False, blank=False, default=0.0)
	parent = models.ForeignKey('self', null=True, related_name='children')

	def get_balance(self):
		""" Get the active balance """
		balance = 0

		for child in self.children.all():
			balance += child.balance
		
		mysum = Transaction.objects.filter(account=self.id).aggregate(total=Sum('amount'))
		if 'total' in mysum and mysum['total'] != None:
			balance += mysum['total']
	
		return balance

	
	def set_balance(self, value):
		""" Set the active balance recursively """
		self._balance += value

		# This should be recursive
		parent = Account.objects.get(id=self.parent)
		if parent:
			parent._balance += value

	balance = property(get_balance, set_balance)

	class Meta:
		""" Metadata """
		db_table = u'accounts'

class Transaction(models.Model):
	""" Transactions in the accounting ledger """
	date = models.DateField(null=False, blank=False)
	account = models.ForeignKey(Account, related_name='transaction')
	transfer = models.ForeignKey(Account, related_name='transaction_transfer')
	related = models.ManyToManyField('self', blank=False)
	relation = models.ForeignKey(Relation, null=True)
	description = models.CharField(max_length=765, blank=True)
	amount = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
	invoice_number = models.CharField(max_length=45, null=True, blank=True)
	purchase_order = models.ForeignKey(PurchaseOrder, null=True)
	#sale = models.ForeignKey('SaleItem')
	document = models.TextField(blank=True)
	class Meta:
		""" Metadata """
		db_table = u'transactions'

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

class Vat(models.Model):
	""" VAT table: Describes VAT/GST percentage and to which account it's to be booked """
	name = models.CharField(max_length=30, blank=True)
	percent = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
	account = models.ForeignKey(Account, null=False)
	class Meta:
		""" Metadata """
		db_table = u'vat'

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
	product_group = models.ForeignKey(ProductGroup)
	code = models.CharField(unique=True, max_length=120, blank=False)
	name = models.CharField(max_length=300, blank=True)
	description = models.TextField(blank=True)
	minimum_stock = models.IntegerField(null=True, blank=True)
	maximum_stock = models.IntegerField(null=True, blank=True)
	active = models.BooleanField(default=True)
	vat = models.ForeignKey(Vat)
	has_own_serials = models.BooleanField(default=True)
	invoice_interval = models.IntegerField(null=True, choices=INTERVAL_CHOICES)
	invoice_interval_count = models.IntegerField(null=True, default=1)
	class Meta:
		""" Metadata """
		db_table = u'products'

class Subproduct(models.Model):
	""" Specific product, like "High-End 10GbE Switch" -> "Arista 7500" or "Linksys WRT54g" -> "Linksys WRT54g rev. 3". """
	product = models.ForeignKey(Product)
	ean_upc_code = models.CharField(unique=True, max_length=180, blank=False)
	name = models.CharField(max_length=300, blank=False)
	class Meta:
		""" Metadata """
		db_table = u'subproducts'

class Subscription(models.Model):
	""" Customer subscriptions to products of type 02 'Periodic'. """
	product = models.ForeignKey(Product)
	customer = models.ForeignKey(Relation)
	start_date = models.DateTimeField(null=False, blank=False)
	end_date = models.DateTimeField(null=True)
	discount = models.DecimalField(decimal_places=5, max_digits=9, null=False, default=0.0)
	invoiced_until_date = models.DateTimeField(null=True)
	intervals_per_invoice = models.IntegerField(null=False, default=0)
	extra_info = models.TextField(null=False, blank=False)
	active = models.BooleanField(null=False, default=1)
	class Meta:
		""" Metadata """
		db_table = u'subscriptions'

class InternalOrder(models.Model):
	""" Internal ordering for things that are to be purchased externally, kind of like an order queue. """
	state = models.IntegerField(null=True, blank=True)
	sale_order_date = models.DateTimeField(null=True, blank=True)
	ordered_by_user = models.ForeignKey(User)
	amount_needed = models.IntegerField(null=True, blank=True)
	product = models.ForeignKey(Product)
	product_group = models.ForeignKey(ProductGroup)
	product_description = models.CharField(max_length=300, blank=True)
	purchase_price_indication = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
	selling_price = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
	supplier_suggestion = models.ForeignKey(Relation, related_name='+')
	for_customer = models.BooleanField(default=False)
	customer = models.ForeignKey(Relation)
	customer_reference = models.CharField(max_length=180, blank=True)
	class Meta:
		""" Metadata """
		db_table = u'internal_order'

class PurchaseOrderItem(models.Model):
	""" Purchase Order contents """
	purchase_order = models.ForeignKey(PurchaseOrder)
	internal_order = models.ForeignKey(InternalOrder)
	state = models.IntegerField(null=True, blank=True)
	purchase_price = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
	order_amount = models.IntegerField(null=True, blank=True)
	units_per_pack = models.IntegerField(null=True, blank=True)
	subproduct = models.ForeignKey(Subproduct)
	supplier_has_in_stock = models.BooleanField(default=False)
	expected_date = models.DateField(null=True, blank=True)
	class Meta:
		""" Metadata """
		db_table = u'purchase_order_data'

class Item(models.Model):
	""" Individual units that are in stock. """
	serial_number = models.CharField(unique=True, max_length=180, blank=False)
	purchase_order_data = models.ForeignKey(PurchaseOrderItem)
	input_by_user = models.ForeignKey(User, related_name='items_input')
	reserved = models.BooleanField(default=False)
	reserved_for_relation = models.ForeignKey(Relation, related_name='items_reserved')
	reserved_by_user = models.ForeignKey(User, related_name='items_reserved')
	reserved_date = models.DateTimeField(null=True, blank=True)
	sold = models.BooleanField(default=False)
	written_off = models.BooleanField(default=False)
	written_off_by_user = models.ForeignKey(User, related_name='items_writtenoff')
	location = models.ForeignKey(Location)
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
	container = models.ForeignKey(Container)
	item = models.ForeignKey(Item)
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
	inventory = models.ForeignKey('Inventory')
	item = models.ForeignKey(Item)
	location = models.ForeignKey(Location)
	value = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
	class Meta:
		""" Metadata """
		db_table = u'inventory_data'


class ProductSellingprice(models.Model):
	""" Active selling prices of products for given dates. """
	product = models.ForeignKey(Product)
	commencing_date = models.DateField(null=True, blank=True)
	set_date = models.DateField(null=True, blank=True)
	price = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
	class Meta:
		""" Metadata """
		db_table = u'product_sellingprices'




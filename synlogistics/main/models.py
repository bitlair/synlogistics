# Create your models here.
 
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#	 * Rearrange models' order
#	 * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
	

class Relation(models.Model):
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
		db_table = u'relations'

class Contact(models.Model):
	relation = models.ForeignKey(Relation)
	givenname = models.CharField(max_length=75, blank=True)
	infix = models.CharField(max_length=75, blank=True)
	surname = models.CharField(max_length=180, blank=True)
	phone = models.CharField(max_length=60, blank=True)
	mobilephone = models.CharField(max_length=60, blank=True)
	notes = models.TextField(blank=True)
	active = models.BooleanField(default=True)
	class Meta:
		db_table = u'contacts'

class PurchaseOrder(models.Model):
	purchasing_date = models.DateTimeField(null=True, blank=True)
	customer = models.ForeignKey(Relation)
	order_method = models.IntegerField(null=True, blank=True)
	relation_contact = models.ForeignKey(Contact)
	external_order_reference = models.CharField(max_length=90, blank=True)
	class Meta:
		db_table = u'purchase_orders'

class Account(models.Model):
	TYPE_CHOICES = (
		(00, 'Assets'),
		(01, 'Accounts receivable'),
		(02, 'Bank account'),
		(03, 'Cash'),
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
	_balance = models.FloatField(null=False, blank=False, default=0.0)
	parent = models.ForeignKey('self', null=True, related_name='children')

	def get_balance(self):
		balance = 0

		for child in self.children.all():
			balance += child.balance
		
		mysum = Transaction.objects.filter(account=self.id).aggregate(total=Sum('amount'))
		if 'total' in mysum and mysum['total'] != None:
			balance += mysum['total']
	
		return balance

	
	def set_balance(self, value):
		self._balance += value

		# This should be recursive
		parent = Account.objects.get(id=self.parent)
		if parent:
			parent.balance += value

	balance = property(get_balance, set_balance)

	class Meta:
		db_table = u'accounts'

class Transaction(models.Model):
	date = models.DateField(null=True, blank=True)
	account = models.ForeignKey(Account, related_name='transaction')
	transfer = models.ForeignKey(Account, related_name='transaction_transfer')
	related = models.ManyToManyField('self', blank=False)
	relation = models.ForeignKey(Relation)
	description = models.CharField(max_length=765, blank=True)
	amount = models.FloatField(null=True, blank=True)
	invoice_number = models.CharField(max_length=45, blank=True)
	purchase_order = models.ForeignKey(PurchaseOrder)
	#sale = models.ForeignKey('SaleItem')
	document = models.TextField(blank=True)
	class Meta:
		db_table = u'transactions'

class Location(models.Model):
	name = models.CharField(max_length=180, blank=True)
	address = models.CharField(max_length=180, blank=True)
	postalzip = models.CharField(max_length=30, blank=True)
	city = models.CharField(max_length=180, blank=True)
	country = models.CharField(max_length=180, blank=True)
	phone = models.CharField(max_length=60, blank=True)
	location_type = models.IntegerField(null=True, blank=True)
	active = models.BooleanField(default=True)
	class Meta:
		db_table = u'locations'

class Vat(models.Model):
	name = models.CharField(max_length=30, blank=True)
	percent = models.FloatField(null=True, blank=True)
	class Meta:
		db_table = u'vat'

class ProductGroup(models.Model):
	name = models.CharField(unique=True, max_length=255, blank=False)
	description = models.TextField(blank=True)
	active = models.BooleanField(default=True)
	class Meta:
		db_table = u'product_groups'

class Product(models.Model):
	TYPE_CHOICES = (
		(00, 'Hardware'),
		(01, 'Service'),
		(02, 'Periodic'))
	product_type = models.IntegerField(null=False, choices=TYPE_CHOICES)
	product_group = models.ForeignKey(ProductGroup)
	code = models.CharField(unique=True, max_length=120, blank=False)
	name = models.CharField(max_length=300, blank=True)
	description = models.TextField(blank=True)
	minimum_stock = models.IntegerField(null=True, blank=True)
	maximum_stock = models.IntegerField(null=True, blank=True)
	active = models.BooleanField(default=True)
	vat = models.ForeignKey(Vat)
	class Meta:
		db_table = u'products'

class Subproduct(models.Model):
	product = models.ForeignKey(Product)
	ean_upc_code = models.CharField(unique=True, max_length=180, blank=False)
	name = models.CharField(max_length=300, blank=False)
	class Meta:
		db_table = u'subproducts'

class InternalOrder(models.Model):
	state = models.IntegerField(null=True, blank=True)
	sale_order_date = models.DateTimeField(null=True, blank=True)
	ordered_by_user = models.ForeignKey(User)
	amount_needed = models.IntegerField(null=True, blank=True)
	product = models.ForeignKey(Product)
	product_group = models.ForeignKey(ProductGroup)
	product_description = models.CharField(max_length=300, blank=True)
	purchase_price_indication = models.FloatField(null=True, blank=True)
	selling_price = models.FloatField(null=True, blank=True)
	supplier_suggestion = models.ForeignKey(Relation, related_name='+')
	for_customer = models.BooleanField(default=False)
	customer = models.ForeignKey(Relation)
	customer_reference = models.CharField(max_length=180, blank=True)
	class Meta:
		db_table = u'internal_order'

class PurchaseOrderItem(models.Model):
	purchase_order = models.ForeignKey(PurchaseOrder)
	internal_order = models.ForeignKey(InternalOrder)
	state = models.IntegerField(null=True, blank=True)
	purchase_price = models.FloatField(null=True, blank=True)
	order_amount = models.IntegerField(null=True, blank=True)
	units_per_pack = models.IntegerField(null=True, blank=True)
	subproduct = models.ForeignKey(Subproduct)
	supplier_has_in_stock = models.BooleanField(default=False)
	expected_date = models.DateField(null=True, blank=True)
	class Meta:
		db_table = u'purchase_order_data'

class Item(models.Model):
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
		db_table = u'items'

class Container(models.Model):
	container_number = models.CharField(unique=True, max_length=180, blank=False)
	name = models.CharField(max_length=180, blank=True)
	container_template = models.IntegerField(null=True, blank=True)
	create_date = models.DateTimeField(null=True, blank=True)
	display_contents = models.IntegerField(null=True, blank=True)
	sold = models.IntegerField(null=True, blank=True)
	class Meta:
		db_table = u'containers'

class ContainerItem(models.Model):
	container = models.ForeignKey('Container')
	item = models.ForeignKey(Item)
	added_date = models.DateTimeField(null=True, blank=True)
	class Meta:
		db_table = u'container_data'

class ContainerTemplate(models.Model):
	name = models.CharField(unique=True, max_length=255, blank=False)
	description = models.TextField(blank=True)
	active = models.BooleanField(default=True)
	products = models.ManyToManyField('product', symmetrical=False)
	class Meta:
		db_table = u'container_templates'


class Inventory(models.Model):
	date = models.DateTimeField(null=True, blank=True)
	name = models.CharField(max_length=120, blank=True)
	notes = models.TextField(blank=True)
	class Meta:
		db_table = u'inventories'

class InventoryItem(models.Model):
	inventory = models.ForeignKey('Inventory')
	item = models.ForeignKey(Item)
	location = models.ForeignKey(Location)
	value = models.FloatField(null=True, blank=True)
	class Meta:
		db_table = u'inventory_data'


class ProductSellingprice(models.Model):
	product = models.ForeignKey(Product)
	commencing_date = models.DateField(null=True, blank=True)
	set_date = models.DateField(null=True, blank=True)
	price = models.FloatField(null=True, blank=True)
	class Meta:
		db_table = u'product_sellingprices'




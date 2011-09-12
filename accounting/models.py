"""
SynLogistics accounting models
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
from django.db import transaction as db_trans
from django.db.models import Sum
from main.models import Relation, PurchaseOrder

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
	account = models.ForeignKey(Account, related_name='transactions')
	transfer = models.ForeignKey(Account, related_name='+')
	related = models.ManyToManyField('self', blank=False)
	relation = models.ForeignKey(Relation, null=True, related_name='transactions')
	description = models.CharField(max_length=765, blank=True)
	amount = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
	invoice_number = models.CharField(max_length=45, null=True, blank=True)
	purchase_order = models.ForeignKey(PurchaseOrder, related_name='transactions', null=True)
	#sale = models.ForeignKey('SaleItem')
	document = models.TextField(blank=True)

	@db_trans.commit_manually
	def save(self, *args, **kwargs):
		""" Inserts/updates the related transaction. This extends the models.Model save() function """

		try:
			new = False

			# Insert or update the related transaction for the transfer account.
			if self.id:
				assert self.related.count() == 1
				for related in self.related.all():
					pass
			else:
				new = True
				related = Transaction()
			
			related.account = self.transfer
			related.date = self.date
			related.transfer = self.account
			related.description = self.description
			related.relation = self.relation
			related.amount = self.amount

			# Some accounts, like liabilities and expenses are inverted.
			# Determine if we need to invert the amount on the related transaction
			if (self.account.account_type < 10 or self.account.account_type == 40) \
				==	(self.transfer.account_type < 10 or self.transfer.account_type == 40):
				related.amount = -self.amount


			# The super class does the actual saving to the database.
			super(Transaction, related).save()

			if new:
				self.related.add(related)

			super(Transaction, self).save(*args, **kwargs)
		
			# If we just added the related bit we need to save again, because the related id is only known now.
			if new:
				related.related.add(self)
				super(Transaction, related).save()
		except:
			db_trans.rollback()
			raise
		else:
			db_trans.commit()	

	class Meta:
		""" Metadata """
		db_table = u'transactions'

class Vat(models.Model):
	""" VAT table: Describes VAT/GST percentage and to which account it's to be booked """
	name = models.CharField(max_length=30, blank=True)
	percent = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
	account = models.ForeignKey(Account, related_name='+', null=True)
	class Meta:
		""" Metadata """
		db_table = u'vat'


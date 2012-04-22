# -*- coding: utf-8 -*-
"""
SynLogistics accounting models
"""
#
# Copyright (C) by Wilco Baan Hofman <wilco@baanhofman.nl> 2011
# Copyright (C) 2012 Jeroen Dekkers <jeroen@dekkers.ch>
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
from django.db.models import Sum
import mptt
from mptt.managers import TreeManager
from mptt.models import TreeForeignKey
from djmoney.models.fields import MoneyField

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
    number = models.CharField(unique=True, max_length=24)
    name = models.CharField(max_length=180)
    description = models.CharField(max_length=765, blank=True)
    account_type = models.IntegerField(choices=TYPE_CHOICES)
    is_readonly = models.BooleanField(default=False)
    _balance = MoneyField(decimal_places=5, max_digits=25, default=0.0, default_currency='EUR')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    objects = TreeManager()

    class Meta:
        """ Metadata """
        db_table = u'accounts'
        ordering = ['number']

    def __unicode__(self):
        return "%s: %s" % (self.number, self.name)

    @property
    def balance(self):
        """ Get the active balance """
        balance = 0

        for child in self.get_children():
            balance += child.balance
        
        mysum = Transaction.objects.filter(account=self.id).aggregate(total=Sum('amount'))
        if 'total' in mysum and mysum['total'] != None:
            balance += mysum['total']
    
        return balance

    @balance.setter
    def balance(self, value):
        """ Set the active balance recursively """
        self._balance += value

        # This should be recursive
        parent = Account.objects.get(id=self.parent)
        if parent:
            parent._balance += value

# We manually register with mptt here, because django-money changes the manager
# in such a way that it doesn't work when we subclass directly from MPPTModel.
mptt.register(Account, order_insertion_by=['number'])

class Transaction(models.Model):
    """ Transactions in the accounting ledger """
    date = models.DateField()
    account = models.ForeignKey(Account, related_name='transactions')
    transfer = models.ForeignKey(Account, related_name='+')
    related = models.ManyToManyField('self')
    relation = models.ForeignKey('main.Relation', related_name='transactions', null=True, blank=True)
    description = models.CharField(max_length=765, blank=True)
    amount = MoneyField(decimal_places=5, max_digits=25, null=True, blank=True, default_currency='EUR')
    invoice_number = models.CharField(max_length=45, blank=True)
    purchase_order = models.ForeignKey('main.PurchaseOrder', related_name='transactions', null=True, blank=True)
    invoice_item = models.ForeignKey('invoicing.InvoiceItem', null=True, blank=True)
    document = models.TextField(blank=True)

    class Meta:
        """ Metadata """
        db_table = u'transactions'
        ordering = ['-date']

    def __unicode__(self):
        return "%s %s (%s -> %s): %d" % (self.date, self.description, self.account.name, self.transfer.name, self.amount)

    def save(self, *args, **kwargs):
        """ Inserts/updates the related transaction. This extends the models.Model save() function """
        # Insert or update the related transaction for the transfer account.
        if self.id:
            new = False
            # There must only be one related transaction, so we can use get() here.
            related = self.related.get()
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
            ==    (self.transfer.account_type < 10 or self.transfer.account_type == 40):
            related.amount = -self.amount


        # The super class does the actual saving to the database.
        super(Transaction, related).save()
        super(Transaction, self).save(*args, **kwargs)

        if new:
            self.related.add(related)

class Vat(models.Model):
    """ VAT table: Describes VAT/GST percentage and to which account it's to be booked """
    name = models.CharField(max_length=30, blank=True)
    percent = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
    account = models.ForeignKey(Account, related_name='+', null=True, blank=True)

    class Meta:
        """ Metadata """
        db_table = u'vat'

    def __unicode__(self):
        return "%s: %s%%" % (self.name, self.percent)

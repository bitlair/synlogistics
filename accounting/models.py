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
from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from django.db.models import Sum
import mptt
from mptt.managers import TreeManager
from mptt.models import TreeForeignKey
from djmoney.models.fields import MoneyField
from easycrud.models import EasyCrudModel


class Account(EasyCrudModel):
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
        balance = Decimal(0)

        for child in self.get_children():
            balance += child.balance

        mysum = SubTransaction.objects.filter(account=self.id).aggregate(total=Sum('amount'))
        if 'total' in mysum and mysum['total'] != None:
            balance += mysum['total']

        # FIXME: we need an integral solution for rounding
        balance = balance.quantize(Decimal('0.01'), ROUND_HALF_UP)

        return balance

    @property
    def increase_is_debit(self):
        if self.account_type in [10, 11, 12, 80]:
            return False
        else:
            return True

# We manually register with mptt here, because django-money changes the manager
# in such a way that it doesn't work when we subclass directly from MPPTModel.
mptt.register(Account, order_insertion_by=['number'])


class TransactionManager(models.Manager):
    def create_simple(self, date, description, source, dest, amount):
        transaction = self.create(date=date, description=description)
        if source.increase_is_debit:
            SubTransaction.objects.create(transaction=transaction, date=date, account=source, amount=-amount)
        else:
            SubTransaction.objects.create(transaction=transaction, date=date, account=source, amount=amount)
        if dest.increase_is_debit:
            SubTransaction.objects.create(transaction=transaction, date=date, account=dest, amount=amount)
        else:
            SubTransaction.objects.create(transaction=transaction, date=date, account=dest, amount=-amount)
        return transaction


class Transaction(models.Model):
    """ Transactions in the accounting ledger """
    date = models.DateField()
    description = models.CharField(max_length=765, blank=True)
    invoice = models.OneToOneField('invoicing.Invoice', null=True, blank=True, unique=True)

    objects = TransactionManager()

    class Meta:
        """ Metadata """
        db_table = u'transactions'
        ordering = ['date']

    def __unicode__(self):
        return "%s %s" % (self.date, self.description)


class SubTransaction(models.Model):
    transaction = models.ForeignKey('Transaction')
    date = models.DateField()
    account = models.ForeignKey(Account, related_name='subtransactions')
    amount = MoneyField(decimal_places=5, max_digits=25, null=True, blank=True, default_currency='EUR')

    class Meta:
        ordering = ['date']

    def __unicode__(self):
        return "%s: %s" % (self.date, self.account)


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

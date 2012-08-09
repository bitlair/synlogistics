#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from django.core.management import setup_environ
import settings

setup_environ(settings)

from invoicing.models import Invoice
from datetime import date
from calendar import monthrange
from moneyed import Money
import moneyed.localization

def format_money(money):
    return moneyed.localization._FORMATTER.format(money, locale="nl_NL")

year = int(sys.argv[1])
quarter = int(sys.argv[2])
first_day= date(year, quarter*3-2, 1)
last_day = date(year, quarter*3, monthrange(year, quarter*3)[1])

tot_ex_btw = Money(0, 'EUR')
tot_inc_btw = Money(0, 'EUR')
tot_btw = Money(0, 'EUR')
for invoice in Invoice.objects.filter(date__gte=first_day, date__lte=last_day):
    print "%s invoice %d to %s" % (invoice.date, invoice.number, invoice.customer.name)
    print "%s ex btw + %s btw = %s incl btw" % (format_money(invoice.total), format_money(invoice.vat), format_money(invoice.total_inc_vat))
    tot_ex_btw += invoice.total
    tot_inc_btw += invoice.total_inc_vat
    tot_btw += invoice.vat

print
print "Totaal ex btw: %s" % format_money(tot_ex_btw)
print "Totaal btw: %s" % format_money(tot_btw)
print "Totaal incl btw: %s" % format_money(tot_inc_btw)

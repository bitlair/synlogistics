#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from django.core.management import setup_environ
import settings

setup_environ(settings)

from invoicing.models import Invoice, TimeKeepingEntry
from itertools import chain
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
    invoice_ex_btw = Money(0, 'EUR')
    invoice_btw = Money(0, 'EUR')

    # FIXME: These calculations belong in the Invoice model
    for item in chain(invoice.timekeepingentry_set.order_by('date'), invoice.simple_items.all()):
        if isinstance(item, TimeKeepingEntry):
            if item.start_time:
                description = "%s: %s-%s %s" % (item.date, item.start_time.strftime("%H:%M"), item.end_time.strftime("%H:%M"), item.description)
            else:
                description = "%s: %s" % (item.date, item.description)
            count = item.hours
            print count
            price = item.rate.rate
            vat_percent = item.rate.vat.percent
        else:
            description = item.description
            count = item.count
            price = item.price
            vat_percent = item.vat.percent
        item_ex_btw = count * price
        item_btw = item_ex_btw * vat_percent/100
        invoice_ex_btw += item_ex_btw
        invoice_btw += item_btw

    # FIXME, check how py-moneyed does rounding
    #invoice_btw = invoice_btw.quantize(Decimal('.01'))
    invoice_inc_btw = invoice_ex_btw + invoice_btw
    print "%s invoice %d to %s" % (invoice.date, invoice.number, invoice.customer.name)
    print "%s ex btw + %s btw = %s incl btw" % (format_money(invoice_ex_btw), format_money(invoice_btw), format_money(invoice_inc_btw))
    tot_ex_btw += invoice_ex_btw
    tot_inc_btw += invoice_inc_btw
    tot_btw += invoice_btw

print
print "Totaal ex btw: %s" % format_money(tot_ex_btw)
print "Totaal btw: %s" % format_money(tot_btw)
print "Totaal incl btw: %s" % format_money(tot_inc_btw)

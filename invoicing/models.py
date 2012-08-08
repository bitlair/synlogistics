# -*- coding: utf-8 -*-
"""
SynLogistics: Invoice class
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
from django.db.models import Max
from durationfield.db.models.fields.duration import DurationField
from djmoney.models.fields import MoneyField
from main.models import BookingPeriod
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from cStringIO import StringIO
from pyPdf import PdfFileReader, PdfFileWriter
from os.path import exists
from settings import STATIC_ROOT
from constance import config
from datetime import datetime, date
from decimal import Decimal
import os
import errno


class Invoice(models.Model):
    """ Invoice """
    customer = models.ForeignKey('main.Relation', related_name='invoices')
    date = models.DateField(db_index=True)
    booking_period = models.ForeignKey('main.BookingPeriod')
    number = models.IntegerField(db_index=True, editable=False)
    full_invoice_no = models.CharField(max_length=25, db_index=True, editable=False)

    def __unicode__(self):
        return u'%s: %s (%s)' % (self.full_invoice_no, self.customer, self.date)

    class Meta:
        """ Metadata """
        db_table = u'invoices'

    def save(self, *args, **kwargs):
        """
        Assign invoice number and save to the database. This extends the default django save() function.
        """
        if not self.pk:
            # Get the active booking period for this invoice
            self.booking_period = BookingPeriod.get_by_date(self.date)

            # Select the first available invoice number
            if config.invoice_number_per_booking_period:
                number_max = Invoice.objects.filter(booking_period=self.booking_period).aggregate(Max('number'))['number__max']
            else:
                number_max = Invoice.objects.all().aggregate(Max('number'))['number__max']

            # When there aren't any invoices, number_max will be None
            if number_max:
                self.number = number_max + 1
            else:
                self.number = 1

            # Create the full invoice number based on the user defined format string
            self.full_invoice_no = config.invoice_number_format % {
                    'booking_period': self.booking_period.number,
                    'year': self.date.year,
                    'month': self.date.month,
                    'day': self.date.day,
                    'number': self.number, }

        # Call the superclass's save function to write to the database
        super(Invoice, self).save(*args, **kwargs)

    def book(self):
        """ Books the invoice """
        # FIXME This is a stub function

        for item in self.items.all():
            print item.amount

            # If there is VAT on this product, book that as well.
            if item.product.vat.percent > 0:
                print item.amount * item.product.vat.percent

    def pdf(self):
        """ Generates PDF invoice """

        # Test if we're already stored. Programmer error if this invoice is not in the database yet.
        assert self.id

        # FIXME This function only works for periodic invoices at this time

        # Verify the watermark PDF exists or bail
        if not exists(config.letterhead_paper_path):
            raise IOError(errno.ENOENT)

        # Read the letterhead paper
        # FIXME Make page size configurable
        pdf_buffer = StringIO()
        canvas = Canvas(pdf_buffer, pagesize=A4)
        pdfmetrics.registerFont(TTFont('FreeSerif', 'fonts' + os.sep + 'FreeSerif.ttf'))
        pdfmetrics.registerFont(TTFont('FreeSerifB', 'fonts' + os.sep + 'FreeSerifBold.ttf'))
        pdfmetrics.registerFont(TTFont('FreeSerifI', 'fonts' + os.sep + 'FreeSerifItalic.ttf'))
        pdfmetrics.registerFont(TTFont('FreeSerifBI', 'fonts' + os.sep + 'FreeSerifBoldItalic.ttf'))

        # Draw the address
        # FIXME the invoice contact should be added
        canvas.setFont("FreeSerif", 12)
        canvas.drawString(40 * mm, A4[1] - (60 * mm), self.customer.invoice_name)
        canvas.drawString(40 * mm, A4[1] - (60 * mm), self.customer.invoice_contact.displayname)
        canvas.drawString(40 * mm, A4[1] - (65 * mm), self.customer.postal_address)
        canvas.drawString(40 * mm, A4[1] - (70 * mm), self.customer.postal_zip_code + " " + self.customer.postal_city)
        canvas.drawString(40 * mm, A4[1] - (75 * mm), self.customer.postal_country)

        # Draw the invoice information
        # FIXME 1. Need locale support for invoices
        # FIXME 2. Need customer reference and order numbers for the subscriptions
        # FIXME 3. The currency is still hardcoded
        canvas.drawString(10 * mm, A4[1] - (100 * mm), 'Invoice number:')
        canvas.drawString(50 * mm, A4[1] - (100 * mm), self.full_invoice_no)
        canvas.drawString(110 * mm, A4[1] - (100 * mm), 'Order number:')
        canvas.drawString(160 * mm, A4[1] - (100 * mm), '-')
        canvas.drawString(10 * mm, A4[1] - (105 * mm), 'Customer reference:')
        canvas.drawString(50 * mm, A4[1] - (105 * mm), '-')
        canvas.drawString(110 * mm, A4[1] - (105 * mm), 'ISO-4217 currency:')
        canvas.drawString(160 * mm, A4[1] - (105 * mm), 'EUR')

        # Draw the invoice data header
        canvas.setFont("FreeSerifB", 12)
        canvas.drawString(10 * mm, A4[1] - (115 * mm), 'Product')
        canvas.drawString(50 * mm, A4[1] - (115 * mm), 'Period')
        canvas.drawString(110 * mm, A4[1] - (115 * mm), 'Extra information')
        canvas.drawString(175 * mm, A4[1] - (115 * mm), 'Price')

        total_amount = 0
        total_vat = 0

        y = 120
        for item in self.items.all():
            canvas.setFont("FreeSerif", 12)
            canvas.drawString(10 * mm, A4[1] - (y * mm), item.product.name)
            canvas.drawString(50 * mm, A4[1] - (y * mm), item.period)
            canvas.drawString(110 * mm, A4[1] - (y * mm), item.description)
            # FIXME Need variable currency
            canvas.setFont("FreeSerif", 10)
            canvas.drawString(175 * mm, A4[1] - (y * mm), '€')
            canvas.setFont("Courier", 10)
            canvas.drawString(178 * mm, A4[1] - (y * mm), "%10.2f" % item.amount)
            y += 5
            total_amount += item.amount
            total_vat += item.amount * item.vat.percent

        canvas.drawString(175 * mm, A4[1] - ((y - 4) * mm), "____________")
        canvas.setFont("FreeSerif", 12)
        canvas.drawString(150 * mm, A4[1] - (y * mm), 'Subtotal')
        canvas.setFont("FreeSerif", 10)
        canvas.drawString(175 * mm, A4[1] - (y * mm), '€')
        canvas.setFont("Courier", 10)
        canvas.drawString(178 * mm, A4[1] - (y * mm), "%10.2f" % total_amount)
        y += 5
        canvas.setFont("FreeSerif", 12)
        canvas.drawString(150 * mm, A4[1] - (y * mm), 'VAT')
        canvas.setFont("FreeSerif", 10)
        canvas.drawString(175 * mm, A4[1] - (y * mm), '€')
        canvas.setFont("Courier", 10)
        canvas.drawString(178 * mm, A4[1] - (y * mm), "%10.2f" % total_vat)
        y += 5
        canvas.setFont("FreeSerif", 12)
        canvas.drawString(150 * mm, A4[1] - (y * mm), 'Total')
        canvas.setFont("FreeSerif", 10)
        canvas.drawString(175 * mm, A4[1] - (y * mm), '€')
        canvas.setFont("Courier", 10)
        canvas.drawString(178 * mm, A4[1] - (y * mm), "%10.2f" % (total_amount + total_vat))
        y += 5

        # Finish the page and save the PDF
        canvas.showPage()
        canvas.save()

        # Merge the letterhead paper with the data
        letterhead = PdfFileReader(file(config.letterhead_paper_path, "rb"))
        page = letterhead.getPage(0)
        pdfInput = PdfFileReader(StringIO(pdf_buffer.getvalue()))
        page.mergePage(pdfInput.getPage(0))
        output = PdfFileWriter()
        output.addPage(page)
        pdf_buffer.close()

        filename = "%s/invoices/%s.pdf" % (STATIC_ROOT, self.full_invoice_no)
        output.write(file(filename, "wb"))

        return filename


class InvoiceItem(models.Model):
    """ Invoice contents """
    invoice = models.ForeignKey(Invoice, related_name="items")
    item = models.ForeignKey('main.Item', related_name="invoice_data", null=True, blank=True)
    product = models.ForeignKey('main.Product', related_name="invoice_data")
    period = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=255)
    count = models.IntegerField()
    amount = MoneyField(decimal_places=5, max_digits=25, default_currency='EUR')
    vat = models.ForeignKey('accounting.Vat', null=True, blank=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.product, self.item)

    class Meta:
        """ Metadata """
        db_table = u'invoice_data'


class Subscription(models.Model):
    """ Customer subscriptions to products of type 02 'Periodic'. """
    product = models.ForeignKey('main.Product', related_name='subscriptions')
    customer = models.ForeignKey('main.Relation', related_name='subscriptions')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    discount = MoneyField(decimal_places=5, max_digits=9, default=0.0, default_currency='EUR')
    invoiced_until_date = models.DateTimeField(null=True, blank=True)
    intervals_per_invoice = models.IntegerField(default=0)
    extra_info = models.TextField()
    active = models.BooleanField(default=1)

    def __unicode__(self):
        return u'%s: %s' % (self.customer, self.product)

    class Meta:
        """ Metadata """
        db_table = u'subscriptions'


class TimeBillingRate(models.Model):
    name = models.CharField(max_length=30)
    rate = MoneyField(decimal_places=2, max_digits=12, default_currency='EUR')
    vat = models.ForeignKey('accounting.Vat')

    def __unicode__(self):
        return u'%s: %s' % (self.name, self.rate)


class TimeKeepingEntry(models.Model):
    rate = models.ForeignKey('TimeBillingRate')
    customer = models.ForeignKey('main.Relation')
    description = models.TextField()
    date = models.DateField(default=date.today, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    duration = DurationField()
    invoice = models.ForeignKey('Invoice', blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        if self.date:
            return u'%s: %s (%s)' % (self.date, self.description, self.customer)
        else:
            return u'%s (%s)' % (self.description, self.customer)

    @property
    def end_time(self):
        if self.start_time:
            return (datetime.combine(date.today(), self.start_time) + self.duration).time()
        else:
            return None

    @property
    def hours(self):
        return int(self.duration.total_seconds()) / Decimal(3600)


class SimpleInvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="simple_items")
    description = models.TextField()
    count = models.DecimalField(decimal_places=2, max_digits=12)
    price = MoneyField(decimal_places=5, max_digits=25, default_currency='EUR')
    vat = models.ForeignKey('accounting.Vat', null=True, blank=True)

    def __unicode__(self):
        return u'%s' % (self.description)

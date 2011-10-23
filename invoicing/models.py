# -*- coding: utf-8 -*-
"""
SynLogistics: Invoice class
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
from django.db import models, transaction as db_trans
from main.models import BookingPeriod, Settings
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from cStringIO import StringIO
from pyPdf import PdfFileReader, PdfFileWriter
from os.path import exists
from settings import STATIC_ROOT
import os
import errno

class Invoice(models.Model):
	""" Invoice """
	customer = models.ForeignKey('main.Relation', related_name='invoices', null=False)
	date = models.DateField(null=False, db_index=True)
	booking_period = models.ForeignKey('main.BookingPeriod', null=False)
	number = models.IntegerField(null=False, db_index=True)
	full_invoice_no = models.CharField(max_length=25, db_index=True)
	
	class Meta:
		""" Metadata """
		db_table = u'invoices'

	@db_trans.commit_manually
	def save(self, *args, **kwargs):
		""" 
		Assign invoice number and save to the database. This extends the default django save() function.
		"""
		# Assert that the mandatory fields are set
		assert self.customer
		assert self.date

		try:
			# Get the active booking period for this invoice
			booking_periods = BookingPeriod.objects.filter(start_date__lte=self.date).filter(end_date__gte=self.date)
			assert booking_periods.count() == 1
			self.booking_period = booking_periods[0]
		
			# Get the list of invoices in this booking period ordered by number
			invoices = Invoice.objects.filter(booking_period=self.booking_period.id).order_by('number')

			# Select the first available invoice number
			self.number = 1
			for invoice in invoices:
				if self.number < invoice.number:
					break
				self.number += 1

			# We need the settings for the invoice format string	
			settings = Settings.objects.all()
			assert settings.count() == 1
			settings = settings[0]

			# Create the full invoice number based on the user defined format string
			self.full_invoice_no = settings.invoice_format_string % {
					'booking_period': self.booking_period.number,
					'year': self.date.year,
					'month': self.date.month,
					'day': self.date.day,
					'number': self.number, }

			# Call the superclass's save function to write to the database
			super(Invoice, self).save(*args, **kwargs)

		except:
			db_trans.rollback()			
			raise
		else:
			db_trans.commit()

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

		# FIXME Use a configuration variable to find the PDF
		if not exists("letterhead_paper.pdf"):
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
		canvas.drawString(40 * mm, A4[1] - (60 * mm), self.customer.displayname)
		canvas.drawString(40 * mm, A4[1] - (65 * mm), self.customer.address)
		canvas.drawString(40 * mm, A4[1] - (70 * mm), self.customer.postalzip + " " + self.customer.city)
		canvas.drawString(40 * mm, A4[1] - (75 * mm), self.customer.country)

		# Draw the invoice information
		# FIXME 1. Need locale support for invoices
		# FIXME 2. Need customer reference and order numbers for the subscriptions
		canvas.drawString(10 * mm, A4[1] - (100 * mm), 'Invoice number:')
		canvas.drawString(50 * mm, A4[1] - (100 * mm), self.full_invoice_no)
		canvas.drawString(110 * mm, A4[1] - (100 * mm), 'Order number:')
		canvas.drawString(140 * mm, A4[1] - (100 * mm), '-')
		canvas.drawString(10 * mm, A4[1] - (105 * mm), 'Customer reference:')
		canvas.drawString(50 * mm, A4[1] - (105 * mm), '-')

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

		canvas.drawString(175 * mm, A4[1] - ((y-4) * mm), "____________")
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
		# FIXME Use configurable paths
		letterhead = PdfFileReader(file("letterhead_paper.pdf", "rb"))
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
	item = models.ForeignKey('main.Item', related_name="invoice_data", null=True)
	product = models.ForeignKey('main.Product', related_name="invoice_date")
	period = models.CharField(max_length=30, blank=True, null=True)
	description = models.CharField(max_length=255, blank=False, null=False)
	count = models.IntegerField(null=False)
	amount = models.DecimalField(decimal_places=5, max_digits=25, null=False)
	vat = models.ForeignKey('accounting.Vat', null=True)
	class Meta:
		""" Metadata """
		db_table = u'invoice_data'

class Subscription(models.Model):
	""" Customer subscriptions to products of type 02 'Periodic'. """
	product = models.ForeignKey('main.Product', related_name='subscriptions')
	customer = models.ForeignKey('main.Relation', related_name='subscriptions')
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

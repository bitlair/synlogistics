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
from main.models import Relation, Item, Product, Vat, BookingPeriod, Settings

class Invoice(models.Model):
	""" Invoice """
	customer = models.ForeignKey(Relation, related_name='invoices', null=False)
	date = models.DateField(null=False, db_index=True)
	booking_period = models.ForeignKey(BookingPeriod, null=False)
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
			print "Booking period: %d" % self.booking_period.number
		
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
			super(Invoice, self).save(*args, **kwargs)

		except:
			db_trans.rollback()			
			raise
		else:
			db_trans.commit()

	def pdf(self):
		""" Generates PDF invoice """

		assert self.id

		print self.id
		print self.number
		print self.full_invoice_no
		print "Excellent, you've done it!"

class InvoiceItem(models.Model):
	""" Invoice contents """
	invoice = models.ForeignKey(Invoice, related_name="data")
	item = models.ForeignKey(Item, related_name="invoice_data", null=True)
	product = models.ForeignKey(Product, related_name="invoice_date")
	period = models.CharField(max_length=30, blank=True, null=True)
	description = models.CharField(max_length=255, blank=False, null=False)
	count = models.IntegerField(null=False)
	amount = models.DecimalField(decimal_places=5, max_digits=25, null=False)
	vat = models.ForeignKey(Vat, null=True)
	class Meta:
		""" Metadata """
		db_table = u'invoice_data'


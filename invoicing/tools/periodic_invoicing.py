"""
SynLogistics: Generate periodic invoices and mails them if necessary
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

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.db.models import Q, F
from datetime import datetime, date, timedelta
from main.models import Subscription
from invoicing.models import Invoice, InvoiceItem

# FIXME This code should use database transactions!

def main():
	"""
	Find subscriptions that are due to be invoiced, generate the invoices, 
	update the accounts, update the subscription and kill all humans
	"""

	# Get current subscriptions and subscriptions that have not been (fully) invoiced and are due to be invoiced.
	subscriptions = Subscription.objects.filter(active = 1)
	subscriptions = subscriptions.filter(Q(invoiced_until_date__isnull = True) | Q(invoiced_until_date__gt = F('start_date')))
	subscriptions = subscriptions.filter(Q(end_date__isnull = True) | Q(invoiced_until_date__lt = F('end_date')))
	subscriptions = subscriptions.filter(Q(invoiced_until_date__isnull = True) | Q(invoiced_until_date__lt = datetime.utcnow()))

	print datetime.utcnow()
	for subscription in subscriptions:

		print "Subscription: %s %s inv: %s start: %s end: %s, int: %d, active: %d" % (subscription.customer.displayname,
				subscription.product.name, subscription.invoiced_until_date, 
				subscription.start_date, subscription.end_date, subscription.intervals_per_invoice, subscription.active)
		print "Product: interval (day:0,week,month,quarter,year): %d count: %d" % (subscription.product.invoice_interval, subscription.product.invoice_interval_count)
		print ""

		invoice = Invoice()
		invoice.customer = subscription.customer
		invoice.date = date.today()
		invoice.save()

		#
		# Calculate the date until which we are invoicing
		#
		if subscription.invoiced_until_date:
			start_date = subscription.invoiced_until_date
		else:
			start_date = subscription.start_date

		if subscription.product.invoice_interval == 0:
			subscription.invoiced_until_date = start_date + timedelta(days = subscription.product.invoice_interval_count * subscription.intervals_per_invoice)

		if subscription.product.invoice_interval == 1:
			subscription.invoiced_until_date = start_date + timedelta(weeks = subscription.product.invoice_interval_count * subscription.intervals_per_invoice)

		elif subscription.product.invoice_interval == 2:
			months = subscription.product.invoice_interval_count * subscription.intervals_per_invoice
			month = start_date.month + months % 12
			year = start_date.year + int(months / 12)
			subscription.invoiced_until_date = date(year, month, start_date.day)

		elif subscription.product.invoice_interval == 3:
			quarters = subscription.product.invoice_interval_count * subscription.intervals_per_invoice
			month = start_date.month + (quarters * 3) % 12
			year = start_date.year + int((quarters * 3) / 12)
			subscription.invoiced_until_date = date(year, month, start_date.day)

		elif subscription.product.invoice_interval == 4:
			years = subscription.product.invoice_interval_count * subscription.intervals_per_invoice
			subscription.invoiced_until_date = date(start_date.year + years, month, day)

		print subscription.invoiced_until_date
		
		# Add the subscription lines to the invoice
		invoiceline = InvoiceItem()
		invoiceline.invoice = invoice
		invoiceline.item = None # Only used for products with serials
		invoiceline.product = subscription.product
		invoiceline.period = start_date.isoformat() + " - " + subscription.invoiced_until_date.isoformat()
		invoiceline.description = subscription.extra_info
		invoiceline.count = 1
		invoiceline.amount = subscription.product.get_price()
		if invoiceline.amount == None:
			# FIXME This should be an exception with transaction rollback
			print "NO PRICE!!"
		else:
			print invoiceline.amount
		invoiceline.vat = subscription.product.vat
		invoiceline.save()

		pdf = invoice.pdf()

		# TODO Mail the invoice to the client if requested, otherwise put the PDF in the outgoing snailmail queue
		

	
if __name__ == "__main__":
	main()

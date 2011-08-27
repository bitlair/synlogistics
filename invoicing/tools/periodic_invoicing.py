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
from datetime import datetime, date
from main.models import Subscription
from invoicing.models import Invoice


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
		# TODO Add the subscription lines to the invoice

		pdf = invoice.pdf()
		# TODO Mail the invoice to the client if requested, otherwise put the PDF in the outgoing snailmail queue


	
if __name__ == "__main__":
	main()

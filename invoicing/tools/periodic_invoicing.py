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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU Affero General Public License for more details.
#	 
# You should have received a copy of the GNU Affero General Public License
# along with this program.	If not, see <http://www.gnu.org/licenses/>.
#

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.db import transaction as db_trans
from django.db.models import Q, F
from datetime import datetime, date, time, timedelta
from invoicing.models import Invoice, InvoiceItem, Subscription
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email import Encoders
from smtplib import SMTP

def send_mail(address, invoice_no, pdf):

	# FIXME Make 'From', 'Subject' and 'Text' configurable
	msg = MIMEMultipart()
	msg['From'] = "SynLogistics <wilco@baanhofman.nl>"
	msg['To'] = address
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = "Invoice from %s" % invoice_no

	msg.attach( MIMEText("Hi,\n\nPlease find your new invoice attached to this message.\n\nRegards,\n\nSynLogistics Accounting System") )

	for f in [ pdf ]:
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open(f, "rb").read() )
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
		msg.attach(part)


	# FIXME Make SMTP server configurable
	smtp = SMTP("localhost")
	smtp.sendmail(msg['From'], address, msg.as_string())
	smtp.close()


@db_trans.commit_manually
def main():
	"""
	Find subscriptions that are due to be invoiced, generate the invoices, 
	update the accounts, update the subscription and kill all humans
	"""

	invoices = []
	try:
		# Get current subscriptions and subscriptions that have not been (fully) invoiced and are due to be invoiced.
		subscriptions = Subscription.objects.filter(active = 1)
		subscriptions = subscriptions.filter(Q(invoiced_until_date__isnull = True) | Q(invoiced_until_date__gte = F('start_date')))
		subscriptions = subscriptions.filter(Q(end_date__isnull = True) | Q(invoiced_until_date__lte = F('end_date')))
		subscriptions = subscriptions.filter(Q(invoiced_until_date__isnull = True) | Q(invoiced_until_date__lte = datetime.utcnow()))

		for subscription in subscriptions:
			invoice = Invoice()
			invoice.customer = subscription.customer
			invoice.date = date.today()
			invoice.save()

			if subscription.invoiced_until_date:
				start_date = subscription.invoiced_until_date
			else:
				start_date = subscription.start_date

			# Invoice every invoice period that needs to be invoiced.
			while start_date < datetime.utcnow():
				#
				# Calculate the date until which we are invoicing
				#
	
				if subscription.product.invoice_interval == 0:
					subscription.invoiced_until_date = start_date + timedelta(days = subscription.product.invoice_interval_count * subscription.intervals_per_invoice)

				if subscription.product.invoice_interval == 1:
					subscription.invoiced_until_date = start_date + timedelta(weeks = subscription.product.invoice_interval_count * subscription.intervals_per_invoice)

				elif subscription.product.invoice_interval == 2:
					months = subscription.product.invoice_interval_count * subscription.intervals_per_invoice
					month = start_date.month + months % 12
					year = start_date.year + int(months / 12)
					subscription.invoiced_until_date = datetime(year, month, start_date.day, 0, 0, 0)

				elif subscription.product.invoice_interval == 3:
					quarters = subscription.product.invoice_interval_count * subscription.intervals_per_invoice
					month = start_date.month + (quarters * 3) % 12
					year = start_date.year + int((quarters * 3) / 12)
					subscription.invoiced_until_date = datetime(year, month, start_date.day, 0, 0, 0)
	
				elif subscription.product.invoice_interval == 4:
					years = subscription.product.invoice_interval_count * subscription.intervals_per_invoice
					subscription.invoiced_until_date = datetime(start_date.year + years, month, day, 0, 0, 0)

				# Add the subscription lines to the invoice
				invoiceitem = InvoiceItem()
				invoiceitem.invoice = invoice
				invoiceitem.item = None # Only used for products with serials
				invoiceitem.product = subscription.product
				invoiceitem.period = start_date.strftime("%Y-%m-%d") + " - " + subscription.invoiced_until_date.strftime("%Y-%m-%d")
				invoiceitem.description = subscription.extra_info
				invoiceitem.count = 1
				invoiceitem.amount = subscription.product.get_price()
				if invoiceitem.amount == None:
					# This item has no price
					raise LookupError
	
				invoiceitem.amount *= subscription.intervals_per_invoice
				invoiceitem.vat = subscription.product.vat
				invoiceitem.save()

				start_date = subscription.invoiced_until_date

			# This subscription has been invoiced.
			subscription.save()

			# The transactions should be made to the VAT tables and accounts receivable
			invoice.book()		

			invoices.append(invoice)

	except:
		db_trans.rollback()
		raise
	else:
		db_trans.commit()

	for invoice in invoices:
			# Mail the invoice to the client if requested, otherwise put the PDF in the outgoing snailmail queue
			if invoice.customer.invoice_by_email:
				pdf = invoice.pdf()
				send_mail("%s <%s>" % (invoice.customer.displayname, invoice.customer.invoice_email), invoice.full_invoice_no, pdf)
			else:
				# FIXME Snailmail queue should be here
				pass
	db_trans.commit()
	
if __name__ == "__main__":
	main()

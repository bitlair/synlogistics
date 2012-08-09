from django.test import TestCase
from datetime import timedelta, time, date
from moneyed import Money

from main.models import Relation, BookingPeriod
from accounting.models import Vat
from .models import Invoice, SimpleInvoiceItem, TimeBillingRate, TimeKeepingEntry


class TimeKeepingTest(TestCase):
    def setUp(self):
        self.customer = Relation.objects.create(name="Customer")
        vat = Vat.objects.create(name="Vat", percent=19)
        self.rate = TimeBillingRate.objects.create(name="Standard", rate=10, vat=vat)

    def test_timekeeping(self):
        self.entry1 = TimeKeepingEntry.objects.create(rate=self.rate, customer=self.customer, description="entry1", duration=timedelta(hours=2))
        self.entry2 = TimeKeepingEntry.objects.create(rate=self.rate, customer=self.customer, description="entry1", start_time=time(hour=10, minute=30), duration=timedelta(hours=1.25))
        self.entry3 = TimeKeepingEntry.objects.create(rate=self.rate, customer=self.customer, description="entry1", duration=timedelta(hours=30))
        self.assertEqual(self.entry1.end_time, None)
        self.assertEqual(self.entry2.end_time, time(hour=11, minute=45))
        self.assertEqual(self.entry1.hours, 2)
        self.assertEqual(self.entry2.hours, 1.25)
        self.assertEqual(self.entry3.hours, 30)


class InvoiceTest(TestCase):
    def setUp(self):
        self.customer = Relation.objects.create(name="Customer")
        self.booking_period1 = BookingPeriod.objects.create(number=2011, start_date=date(2011, 1, 1), end_date=date(2011, 12, 31))
        self.booking_period2 = BookingPeriod.objects.create(number=2012, start_date=date(2012, 1, 1), end_date=date(2012, 12, 31))
        self.booking_period3 = BookingPeriod.objects.create(number=2013, start_date=date(2013, 1, 1), end_date=date(2013, 12, 31))

    def test_invoice(self):
        invoice1 = Invoice.objects.create(customer=self.customer, date=date(2012, 4, 21))
        invoice2 = Invoice.objects.create(customer=self.customer, date=date(2012, 4, 21))
        invoice3 = Invoice.objects.create(customer=self.customer, date=date(2012, 4, 21))
        self.assertEqual(invoice1.booking_period, self.booking_period2)
        self.assertEqual(invoice1.number, 1)
        self.assertEqual(invoice2.number, 2)
        self.assertEqual(invoice3.number, 3)

    def test_vat(self):
        vat = Vat.objects.create(name="Vat", percent=19)
        invoice = Invoice.objects.create(customer=self.customer, date=date(2012, 4, 21))
        SimpleInvoiceItem.objects.create(invoice=invoice, vat=vat, count=4.25, price=85)
        SimpleInvoiceItem.objects.create(invoice=invoice, vat=vat, count=2, price=45)
        self.assertEqual(invoice.total, Money(451.25, 'EUR'))
        self.assertEqual(invoice.vat, Money(85.74, 'EUR'))

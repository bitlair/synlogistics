from django.test import TestCase
from datetime import timedelta, time
from main.models import Relation
from accounting.models import Vat
from .models import *

class TimeKeepingTest(TestCase):
    def setUp(self):
        self.customer = Relation.objects.create(name="Customer")
        vat = Vat.objects.create(name="Vat", percent=19)
        self.rate = TimeBillingRate.objects.create(name="Standard", rate=10, vat=vat)

    def test_timekeeping(self):
        self.entry1 = TimeKeepingEntry.objects.create(rate=self.rate, customer=self.customer, description="entry1", duration=timedelta(hours=2))
        self.entry2 = TimeKeepingEntry.objects.create(rate=self.rate, customer=self.customer, description="entry1", start_time=time(hour=10, minute=30), duration=timedelta(hours=1.25))
        self.assertEqual(self.entry1.end_time, None)
        self.assertEqual(self.entry2.end_time, time(hour=11, minute=45))
        self.assertEqual(self.entry1.hours, 2)
        self.assertEqual(self.entry2.hours, 1.25)

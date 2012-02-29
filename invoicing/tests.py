from django.test import TestCase
from datetime import timedelta, time
from main.models import Relation
from accounting.models import Vat
from .models import *

class TimeKeepingTest(TestCase):
    def setUp(self):
        customer = Relation.objects.create(displayname="Customer")
        vat = Vat.objects.create(name="Vat", percent=19)
        rate = TimeBillingRate.objects.create(name="Standard", rate=10, vat=vat)
        self.entry1 = TimeKeepingEntry.objects.create(rate=rate, customer=customer, description="entry1", duration=timedelta(hours=2))
        self.entry2 = TimeKeepingEntry.objects.create(rate=rate, customer=customer, description="entry1", start_time=time(hour=10, minute=30) ,duration=timedelta(hours=1.25))

    def test_timekeeping(self):
        self.assertEqual(self.entry1.end_time, None)
        self.assertEqual(self.entry2.end_time, time(hour=11, minute=45))
        self.assertEqual(self.entry1.hours, 2)
        self.assertEqual(self.entry2.hours, 1.25)

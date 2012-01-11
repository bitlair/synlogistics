from django.utils import unittest
from accounting.models import Account, Transaction
from main.models import Relation
from datetime import datetime

class AccountTestCase(unittest.TestCase):
    def setUp(self):
        self.banking_account = Account.objects.create(
                number = '12345',
                name = 'banking_account',
                account_type = '02')

        self.expenses_account = Account.objects.create(
                number = '54321',
                name = 'expenses_account',
                account_type = '40')

        self.relation = Relation.objects.create(
                displayname = 'Henk de Vries')

    def tearDown(self):
        self.banking_account.delete()
        self.expenses_account.delete()
        self.relation.delete()

    def test_account_start_balance_is_zero(self):
        self.assertEqual(self.banking_account.balance, 0.0)
        self.assertEqual(self.expenses_account.balance, 0.0)

    def test_transaction_from_banking_to_expenses_account(self):
        transaction = Transaction()
        transaction.relation = self.relation
        transaction.date = datetime.strptime('2012-01-01:00:00:00', '%Y-%m-%d:%H:%M:%S')
        transaction.account = self.banking_account
        transaction.transfer = self.expenses_account
        transaction.description = 'Monies!'
        transaction.amount = -10.0
        transaction.save()

        self.assertEqual(self.banking_account.balance, -10.0)
        self.assertEqual(self.expenses_account.balance, 10.0)

# -*- coding: utf-8 -*-
"""
SynLogistics accounting tests
"""
#
# Copyright (C) by Kristian Vlaardingerbroek <kristian.vlaardingerbroek@gmail.com> 2012
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

from django.test import TestCase
from accounting.models import Account, Transaction
from main.models import Relation
from datetime import date


class AccountTestCase(TestCase):
    def setUp(self):
        self.banking_account = Account.objects.create(
                number='12345',
                name='banking_account',
                account_type='02')

        self.expenses_account = Account.objects.create(
                number='54321',
                name='expenses_account',
                account_type='40')

        self.relation = Relation.objects.create(
                name='Henk de Vries')

    def test_account_start_balance_is_zero(self):
        self.assertEqual(self.banking_account.balance, 0.0)
        self.assertEqual(self.expenses_account.balance, 0.0)

    def test_transaction_from_banking_to_expenses_account(self):
        Transaction.objects.create_simple(date.today(), "Monies!", self.banking_account, self.expenses_account, 10.0)

        self.assertEqual(self.banking_account.balance, -10.0)
        self.assertEqual(self.expenses_account.balance, 10.0)

    def test_balance_propagates_to_parent(self):
        parent_account = Account.objects.create(
                number='67890',
                name='parent_account',
                account_type='40')

        self.expenses_account.parent = parent_account
        self.expenses_account.save()
        Transaction.objects.create_simple(date.today(), "Monies!", self.banking_account, self.expenses_account, 10.0)

        self.assertEqual(parent_account.balance, 10.0)

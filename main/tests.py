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

from django.utils import unittest
from main.models import Product, ProductGroup, ProductSellingprice
from datetime import datetime
from decimal import Decimal

class MainTestCase(unittest.TestCase):
    def test_product_price(self):
        product = Product()
        product.product_type = '00'
        product_group = ProductGroup()
        product_group.name = 'Bouncy'
        product_group.save()
        product.product_group = product_group
        product.code = 'BBALL'
        product.name = 'Bouncy Ball'
        product.save()
        
        product_sellingprice = ProductSellingprice()
        product_sellingprice.product = product
        product_sellingprice.commencing_date = datetime.strptime('2012-02-01:00:00:00', '%Y-%m-%d:%H:%M:%S')
        product_sellingprice.set_date = datetime.strptime('2012-01-01:00:00:00', '%Y-%m-%d:%H:%M:%S')
        product_sellingprice.price = '4.00'
        product_sellingprice.save()
        
        product_sellingprice = ProductSellingprice()
        product_sellingprice.product = product
        product_sellingprice.commencing_date = datetime.strptime('2012-03-01:00:00:00', '%Y-%m-%d:%H:%M:%S')
        product_sellingprice.set_date = datetime.strptime('2012-01-01:00:00:00', '%Y-%m-%d:%H:%M:%S')
        product_sellingprice.price = '6.00'
        product_sellingprice.save()
        
        self.assertEqual(product.get_price(date=datetime.strptime('2012-02-02:00:00:00', '%Y-%m-%d:%H:%M:%S')), Decimal('4.00'))
        self.assertEqual(product.get_price(date=datetime.strptime('2012-03-02:00:00:00', '%Y-%m-%d:%H:%M:%S')), Decimal('6.00'))

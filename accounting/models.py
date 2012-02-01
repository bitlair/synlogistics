# -*- coding: utf-8 -*-
"""
SynLogistics accounting models
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

from django.db import models
from django.db.models import Sum


CURRENCY_CHOICES = (
    ('AED', 'United Arab Emirates dirham'),
    ('AFN', 'Afghan afghani'),
    ('ALL', 'Albanian lek'),
    ('AMD', 'Armenian dram'),
    ('ANG', 'Netherlands Antillean guilder'),
    ('AOA', 'Angolan kwanza'),
    ('ARS', 'Argentine peso'),
    ('AUD', 'Australian dollar'),
    ('AWG', 'Aruban florin'),
    ('BAM', 'Bosnia and Herzegovnia convertible mark'),
    ('BBD', 'Barbados dollar'),
    ('BDT', 'Bangladeshi taka'),
    ('BGN', 'Bulgarian lev'),
    ('BHD', 'Bahrain dinar'),
    ('BIF', 'Burundi franc'),
    ('BMD', 'Bermudian dollar'),
    ('BND', 'Brunei dollar'),
    ('BOB', 'Boliviano'),
    ('BRL', 'Brazilian real'),
    ('BSD', 'Bahamian dollar'),
    ('BTN', 'Bhutanese ngultrum'),
    ('BWP', 'Botswana pula'),
    ('BYR', 'Belarusian Ruble'),
    ('BZD', 'Belizean dollar'),
    ('CAD', 'Canadian dollar'),
    ('CDF', 'Congo/Kinshasa dollar'),
    ('CHF', 'Swiss franc'),
    ('CLP', 'Chilean peso'),
    ('CNY', 'China Yuan renminbi'),
    ('COP', 'Colombian peso'),
    ('CRC', 'Costa Rican colón'),
    ('CUC', 'Cuban convertible peso'),
    ('CUP',    'Cuban peso'),
    ('CVE', 'Cape Verdean escudo'),
    ('CZK', 'Czech koruna'),
    ('DJF', 'Djiboutian franc'),
    ('DKK', 'Danish krone'),
    ('DOP', 'Dominican peso'),
    ('DZD', 'Algerian dinar'),
    ('EGP', 'Egyptian pound'),
    ('ERN', 'Eritrean nakfa'),
    ('ETB', 'Ethiopian birr'),
    ('EUR',    'Euro'),
    ('FJD', 'Fijian dollar'),
    ('FKP', 'Falkland Islands pound'),
    ('GBP', 'Pound sterling'),
    ('GEL', 'Georgian lari'),
    ('GHS', 'Ghanaian cedi'),
    ('GIP', 'Gibraltar pound'),
    ('GMD', 'Gambian dalasi'),
    ('GNF', 'Guinean franc'),
    ('GTQ', 'Guatemalan quetzal'),
    ('GYD', 'Guyanese dollar'),
    ('HKD', 'Hong Kong dollar'),
    ('HNL', 'Honduran lempira'),
    ('HRK', 'Croatian kuna'),
    ('HTG', 'Haitian gourde'),
    ('HUF', 'Hungarian forint'),
    ('IDR', 'Indonesian rupiah'),
    ('ILS', 'Israeli new sheqel'),
    ('INR', 'Indian rupee'),
    ('IQD', 'Iraqi dinar'),
    ('IRR', 'Iranian rial'),
    ('ISK', 'Icelandic króna'),
    ('JMD', 'Jamaican dollar'),
    ('JOD', 'Jordanian dinar'),
    ('JPY', 'Japanese yen'),
    ('KES', 'Kenyan shilling'),
    ('KGS', 'Kyrgyzstani som'),
    ('KMF', 'Comorian franc'),
    ('KPW', 'North Korean won'),
    ('KRW', 'South Korean won'),
    ('KWD', 'Kuwaiti dinar'),
    ('KYD',    'Cayman Islands dollar'),
    ('KZT', 'Kazakhstani tenge'),
    ('LAK', 'Lao kip'),
    ('LBP', 'Lebanese pound'),
    ('LKR', 'Sri Lanka rupee'),
    ('LRD', 'Liberian dollar'),
    ('LSL', 'Lesotho loti'),
    ('LTL', 'Lithuanian litas'),
    ('LVL', 'Latvian lat'),
    ('LYD', 'Libyan dinar'),
    ('MAD', 'Moroccan dirham'),
    ('MDL', 'Moldovan leu'),
    ('MGA', 'Malagasy ariary'),
    ('MKD', 'Macedonian denar'),
    ('MMK', 'Myanma kyat'),
    ('MNT', 'Mongolian tughrik'),
    ('MOP', 'Macanese pataca'),
    ('MRO', 'Mauritanian ouguiya'),
    ('MUR', 'Mauritian rupee'),
    ('MVR', 'Maldivian rufiyaa'),
    ('MWK', 'Malawian kwacha'),
    ('MXN', 'Mexican peso'),
    ('MYR', 'Malaysian ringgit'),
    ('MZN', 'Mozambican metical'),
    ('NAD', 'Namibian dollar'),
    ('NGN', 'Nigerian naira'),
    ('NIO', 'Nicaraguan córdoba'),
    ('NOK', 'Norwegian krone'),
    ('NPR', 'Nepalese rupee'),
    ('NZD', 'New Zealand dollar'),
    ('OMR', 'Omani rial'),
    ('PAB', 'Panamanian balboa'),
    ('PEN', 'Peruvian nuevo sol'),
    ('PGK', 'Papua New Guinean kina'),
    ('PHP', 'Philippine peso'),
    ('PKR', 'Pakistani rupee'),
    ('PLN', 'Polish złoty'),
    ('PYG', 'Paraguayan guarani'),
    ('QAR', 'Qatari riyal'),
    ('RON', 'Romanian new leu'),
    ('RSD', 'Serbian rinar'),
    ('RUB', 'Russian ruble'),
    ('RWF', 'Rwandan franc'),
    ('SAR', 'Saudi riyal'),
    ('SBD', 'Solomon Islands dollar'),
    ('SCR', 'Seychelles rupee'),
    ('SDG', 'Sudanese pound'),
    ('SEK', 'Swedish krona'),
    ('SGD', 'Singapore dollar'),
    ('SHP', 'Saint Helena pound'),
    ('SLL', 'Sierra Leonean leone'),
    ('SOS', 'Somali shilling'),
    ('SRD', 'Surinamese dollar'),
    ('STD', 'São Tomé and Príncipe dobra'),
    ('SYP', 'Syrian pound'),
    ('SZL', 'Swazi lilangeni'),
    ('THB', 'Thai baht'),
    ('TJS', 'Tajikistani somoni'),
    ('TMT', 'Turkmenistani manat'),
    ('TND', 'Tunisian dinar'),
    ('TOP', 'Tongan pa\'anga'),
    ('TRY', 'Turkish lira'),
    ('TTD', 'Trinidad and Tobago dollar'),
    ('TWD', 'New Taiwan dollar'),
    ('TZS', 'Tanzanian shilling'),
    ('UAH', 'Ukrainian hryvna'),
    ('UGX', 'Ugandan shilling'),
    ('USD', 'United States dollar'),
    ('UYU', 'Uruguayan peso'),
    ('UZS', 'Uzbekistani som'),
    ('VEF', 'Venezuelan bolívar fuerte'),
    ('VND', 'Vietnamese đồng'),
    ('VUV', 'Vanuatu vatu'),
    ('WST', 'Samoan tala'),
    ('XAF', 'CFA franc BEAC'),
    ('XCD', 'East Caribbean dollar'),
    ('XDR', 'IMF Special Drawing Rights'),
    ('XOF', 'CFA franc BCEAO'),
    ('XPF', 'CFP franc'),
    ('YER', 'Yemeni rial'),
    ('ZAR', 'South African rand'),
    ('ZMK', 'Zambian kwacha'),
    ('ZWD', 'Zimbabwean dollar'))

CURRENCY_SYMBOLS = (
    ('AED', 'د.إ'),
    ('AFN', 'Afs'),
    ('ALL', 'Lek'),
    ('AGH', 'Դ'), # This is wrong, but unicode 058f has not been implemented yet.
    ('ANG', 'ƒ'),
    ('AOA', 'Kz'),
    ('ARS', '$'),
    ('AUD', '$'),
    ('AWG', 'ƒ'),
    ('BAM', 'KM'),
    ('BBD', '$'),
    ('BDT', '৳'),
    ('BGN', 'лв'),
    ('BHD', 'BD'),
    ('BIF', 'FBu'),
    ('BMD', '$'),
    ('BND', '$'),
    ('BOB', 'Bs.'),
    ('BRL', 'R$'),
    ('BSD', '$'),
    ('BTN', 'Nu.'),
    ('BWP', 'P'),
    ('BYR', 'Br'),
    ('BZD', '$'),
    ('CAD', '$'),
    ('CDF', 'FC'),
    ('CHF', 'Fr.'),
    ('CLP', '$'),
    ('CNY', '¥'),
    ('COP', '$'),
    ('CRC', '₡'),
    ('CUC', '$'),
    ('CUP',    '₱'),
    ('CVE', '$'),
    ('CZK', 'Kč'),
    ('DJF', 'Fdj'),
    ('DKK', 'kr.'),
    ('DOP', '$'),
    ('DZD', 'DA'),
    ('EGP', 'LE'),
    ('ERN', 'Nfk'),
    ('ETB', 'Br'),
    ('EUR',    '€'),
    ('FJD', '$'),
    ('FKP', '£'),
    ('GBP', '£'),
    ('GEL', 'ლ'),
    ('GHS', 'GH₵'),
    ('GIP', '£'),
    ('GMD', 'D'),
    ('GNF', 'FG'),
    ('GTQ', 'Q'),
    ('GYD', '$'),
    ('HKD', '$'),
    ('HNL', 'L'),
    ('HRK', 'kn'),
    ('HTG', 'G'),
    ('HUF', 'Ft'),
    ('IDR', 'Rp'),
    ('ILS', '₪'),
    ('INR', '₹'),
    ('IQD', 'ع.د'),
    ('IRR', 'ریال'),
    ('ISK', 'kr'),
    ('JMD', '$'),
    ('JOD', 'JD'),
    ('JPY', '¥'),
    ('KES', 'Ksh'),
    ('KGS', 'COM'),
    ('KMF', 'CF'),
    ('KPW', '₩'),
    ('KRW', '₩'),
    ('KWD', 'K.D.'),
    ('KYD',    '$'),
    ('KZT', '₸'),
    ('LAK', '₭'),
    ('LBP', '£'),
    ('LKR', 'Rs'),
    ('LRD', '$'),
    ('LSL', 'M'),
    ('LTL', 'Lt'),
    ('LVL', 'Ls'),
    ('LYD', 'LD'),
    ('MAD', 'م.د.'),
    ('MDL', 'MDL'),
    ('MGA', 'Ar'),
    ('MKD', 'DEN'),
    ('MMK', 'Myanma kyat'), # FIXME Need to do the rest as well
    ('MNT', 'Mongolian tughrik'),
    ('MOP', 'Macanese pataca'),
    ('MRO', 'Mauritanian ouguiya'),
    ('MUR', 'Mauritian rupee'),
    ('MVR', 'Maldivian rufiyaa'),
    ('MWK', 'Malawian kwacha'),
    ('MXN', 'Mexican peso'),
    ('MYR', 'Malaysian ringgit'),
    ('MZN', 'Mozambican metical'),
    ('NAD', 'Namibian dollar'),
    ('NGN', 'Nigerian naira'),
    ('NIO', 'Nicaraguan córdoba'),
    ('NOK', 'Norwegian krone'),
    ('NPR', 'Nepalese rupee'),
    ('NZD', 'New Zealand dollar'),
    ('OMR', 'Omani rial'),
    ('PAB', 'Panamanian balboa'),
    ('PEN', 'Peruvian nuevo sol'),
    ('PGK', 'Papua New Guinean kina'),
    ('PHP', 'Philippine peso'),
    ('PKR', 'Pakistani rupee'),
    ('PLN', 'Polish złoty'),
    ('PYG', 'Paraguayan guarani'),
    ('QAR', 'Qatari riyal'),
    ('RON', 'Romanian new leu'),
    ('RSD', 'Serbian rinar'),
    ('RUB', 'Russian ruble'),
    ('RWF', 'Rwandan franc'),
    ('SAR', 'Saudi riyal'),
    ('SBD', 'Solomon Islands dollar'),
    ('SCR', 'Seychelles rupee'),
    ('SDG', 'Sudanese pound'),
    ('SEK', 'Swedish krona'),
    ('SGD', 'Singapore dollar'),
    ('SHP', 'Saint Helena pound'),
    ('SLL', 'Sierra Leonean leone'),
    ('SOS', 'Somali shilling'),
    ('SRD', 'Surinamese dollar'),
    ('STD', 'São Tomé and Príncipe dobra'),
    ('SYP', 'Syrian pound'),
    ('SZL', 'Swazi lilangeni'),
    ('THB', 'Thai baht'),
    ('TJS', 'Tajikistani somoni'),
    ('TMT', 'Turkmenistani manat'),
    ('TND', 'Tunisian dinar'),
    ('TOP', 'Tongan pa\'anga'),
    ('TRY', 'Turkish lira'),
    ('TTD', 'Trinidad and Tobago dollar'),
    ('TWD', 'New Taiwan dollar'),
    ('TZS', 'Tanzanian shilling'),
    ('UAH', 'Ukrainian hryvna'),
    ('UGX', 'Ugandan shilling'),
    ('USD', '$'),
    ('UYU', 'Uruguayan peso'),
    ('UZS', 'Uzbekistani som'),
    ('VEF', 'Venezuelan bolívar fuerte'),
    ('VND', 'Vietnamese đồng'),
    ('VUV', 'Vanuatu vatu'),
    ('WST', 'Samoan tala'),
    ('XAF', 'CFA franc BEAC'),
    ('XCD', 'East Caribbean dollar'),
    ('XDR', 'IMF Special Drawing Rights'),
    ('XOF', 'CFA franc BCEAO'),
    ('XPF', 'CFP franc'),
    ('YER', 'Yemeni rial'),
    ('ZAR', 'South African rand'),
    ('ZMK', 'Zambian kwacha'),
    ('ZWD', 'Zimbabwean dollar'))


class Account(models.Model):
    """ Accounting ledger account """
    TYPE_CHOICES = (
        (00, 'Assets'),
        (01, 'Accounts receivable'),
        (02, 'Bank account'),
        (03, 'Cash'),
        (04, 'Stock'),
        (10, 'Liabilities'),
        (11, 'Accounts payable'),
        (12, 'Credit card'),
        (20, 'Equity'),
        (40, 'Expenses'),
        (80, 'Income'))
    number = models.CharField(unique=True, max_length=24)
    name = models.CharField(max_length=180)
    description = models.CharField(max_length=765, blank=True)
    account_type = models.IntegerField(choices=TYPE_CHOICES)
    is_readonly = models.BooleanField(default=False)
    _balance = models.DecimalField(decimal_places=5, max_digits=25, default=0.0)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    class Meta:
        """ Metadata """
        db_table = u'accounts'
        ordering = ['number']

    def __unicode__(self):
        return "%s: %s" % (self.number, self.name)

    def get_balance(self):
        """ Get the active balance """
        balance = 0

        for child in self.children.all():
            balance += child.balance
        
        mysum = Transaction.objects.filter(account=self.id).aggregate(total=Sum('amount'))
        if 'total' in mysum and mysum['total'] != None:
            balance += mysum['total']
    
        return balance

    
    def set_balance(self, value):
        """ Set the active balance recursively """
        self._balance += value

        # This should be recursive
        parent = Account.objects.get(id=self.parent)
        if parent:
            parent._balance += value

    balance = property(get_balance, set_balance)


class Transaction(models.Model):
    """ Transactions in the accounting ledger """
    date = models.DateField()
    account = models.ForeignKey(Account, related_name='transactions')
    transfer = models.ForeignKey(Account, related_name='+')
    related = models.ManyToManyField('self')
    relation = models.ForeignKey('main.Relation', null=True, related_name='transactions')
    description = models.CharField(max_length=765, blank=True)
    amount = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
    invoice_number = models.CharField(max_length=45, null=True, blank=True)
    purchase_order = models.ForeignKey('main.PurchaseOrder', related_name='transactions', null=True)
    invoice_item = models.ForeignKey('invoicing.InvoiceItem', null=True)
    document = models.TextField(blank=True)

    class Meta:
        """ Metadata """
        db_table = u'transactions'
        ordering = ['-date']

    def __unicode__(self):
        return "%s %s (%s -> %s): %d" % (self.date, self.description, self.account.name, self.transfer.name, self.amount)

    def save(self, *args, **kwargs):
        """ Inserts/updates the related transaction. This extends the models.Model save() function """
        # Insert or update the related transaction for the transfer account.
        if self.id:
            new = False
            # There must only be one related transaction, so we can use get() here.
            related = self.related.get()
        else:
            new = True
            related = Transaction()

        related.account = self.transfer
        related.date = self.date
        related.transfer = self.account
        related.description = self.description
        related.relation = self.relation
        related.amount = self.amount

        # Some accounts, like liabilities and expenses are inverted.
        # Determine if we need to invert the amount on the related transaction
        if (self.account.account_type < 10 or self.account.account_type == 40) \
            ==    (self.transfer.account_type < 10 or self.transfer.account_type == 40):
            related.amount = -self.amount


        # The super class does the actual saving to the database.
        super(Transaction, related).save()
        super(Transaction, self).save(*args, **kwargs)

        if new:
            self.related.add(related)

class Vat(models.Model):
    """ VAT table: Describes VAT/GST percentage and to which account it's to be booked """
    name = models.CharField(max_length=30, blank=True)
    percent = models.DecimalField(decimal_places=5, max_digits=25, null=True, blank=True)
    account = models.ForeignKey(Account, related_name='+', null=True)

    class Meta:
        """ Metadata """
        db_table = u'vat'

    def __unicode__(self):
        return "%s: %s%%" % (self.name, self.percent)

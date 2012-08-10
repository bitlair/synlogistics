# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SubTransaction'
        db.create_table('accounting_subtransaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounting.Transaction'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subtransactions', to=orm['accounting.Account'])),
            ('amount_currency', self.gf('djmoney.models.fields.CurrencyField')(default='EUR', max_length=3)),
            ('amount', self.gf('djmoney.models.fields.MoneyField')(decimal_places=5, default='0.0', max_digits=25, blank=True, null=True, default_currency='EUR')),
        ))
        db.send_create_signal('accounting', ['SubTransaction'])

        # Deleting field 'Account._balance'
        db.delete_column(u'accounts', '_balance')

        # Deleting field 'Account._balance_currency'
        db.delete_column(u'accounts', '_balance_currency')

        # Deleting field 'Account.is_readonly'
        db.delete_column(u'accounts', 'is_readonly')

        # Deleting field 'Transaction.relation'
        db.delete_column(u'transactions', 'relation_id')

        # Deleting field 'Transaction.invoice_item'
        db.delete_column(u'transactions', 'invoice_item_id')

        # Deleting field 'Transaction.invoice_number'
        db.delete_column(u'transactions', 'invoice_number')

        # Deleting field 'Transaction.account'
        db.delete_column(u'transactions', 'account_id')

        # Deleting field 'Transaction.transfer'
        db.delete_column(u'transactions', 'transfer_id')

        # Deleting field 'Transaction.amount'
        db.delete_column(u'transactions', 'amount')

        # Deleting field 'Transaction.purchase_order'
        db.delete_column(u'transactions', 'purchase_order_id')

        # Deleting field 'Transaction.amount_currency'
        db.delete_column(u'transactions', 'amount_currency')

        # Deleting field 'Transaction.document'
        db.delete_column(u'transactions', 'document')

        # Adding field 'Transaction.invoice'
        db.add_column(u'transactions', 'invoice',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['invoicing.Invoice'], unique=True, null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field related on 'Transaction'
        db.delete_table('transactions_related')

    def backwards(self, orm):
        # Deleting model 'SubTransaction'
        db.delete_table('accounting_subtransaction')

        # Adding field 'Account._balance'
        db.add_column(u'accounts', '_balance',
                      self.gf('djmoney.models.fields.MoneyField')(default=0.0, max_digits=25, decimal_places=5, default_currency='EUR'),
                      keep_default=False)

        # Adding field 'Account._balance_currency'
        db.add_column(u'accounts', '_balance_currency',
                      self.gf('djmoney.models.fields.CurrencyField')(default='EUR', max_length=3),
                      keep_default=False)

        # Adding field 'Account.is_readonly'
        db.add_column(u'accounts', 'is_readonly',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Transaction.relation'
        db.add_column(u'transactions', 'relation',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', null=True, to=orm['main.Relation']),
                      keep_default=False)

        # Adding field 'Transaction.invoice_item'
        db.add_column(u'transactions', 'invoice_item',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invoicing.InvoiceItem'], null=True),
                      keep_default=False)

        # Adding field 'Transaction.invoice_number'
        db.add_column(u'transactions', 'invoice_number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=45, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Transaction.account'
        raise RuntimeError("Cannot reverse this migration. 'Transaction.account' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Transaction.transfer'
        raise RuntimeError("Cannot reverse this migration. 'Transaction.transfer' and its values cannot be restored.")
        # Adding field 'Transaction.amount'
        db.add_column(u'transactions', 'amount',
                      self.gf('djmoney.models.fields.MoneyField')(decimal_places=5, default='0.0', max_digits=25, blank=True, null=True, default_currency='EUR'),
                      keep_default=False)

        # Adding field 'Transaction.purchase_order'
        db.add_column(u'transactions', 'purchase_order',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', null=True, to=orm['main.PurchaseOrder']),
                      keep_default=False)

        # Adding field 'Transaction.amount_currency'
        db.add_column(u'transactions', 'amount_currency',
                      self.gf('djmoney.models.fields.CurrencyField')(default='EUR', max_length=3),
                      keep_default=False)

        # Adding field 'Transaction.document'
        db.add_column(u'transactions', 'document',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'Transaction.invoice'
        db.delete_column(u'transactions', 'invoice_id')

        # Adding M2M table for field related on 'Transaction'
        db.create_table(u'transactions_related', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_transaction', models.ForeignKey(orm['accounting.transaction'], null=False)),
            ('to_transaction', models.ForeignKey(orm['accounting.transaction'], null=False))
        ))
        db.create_unique(u'transactions_related', ['from_transaction_id', 'to_transaction_id'])

    models = {
        'accounting.account': {
            'Meta': {'ordering': "['number']", 'object_name': 'Account', 'db_table': "u'accounts'"},
            'account_type': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '24'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['accounting.Account']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'accounting.subtransaction': {
            'Meta': {'ordering': "['-date']", 'object_name': 'SubTransaction'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subtransactions'", 'to': "orm['accounting.Account']"}),
            'amount': ('djmoney.models.fields.MoneyField', [], {'decimal_places': '5', 'default': "'0.0'", 'max_digits': '25', 'blank': 'True', 'null': 'True', 'default_currency': "'EUR'"}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'EUR'", 'max_length': '3'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounting.Transaction']"})
        },
        'accounting.transaction': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Transaction', 'db_table': "u'transactions'"},
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['invoicing.Invoice']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'accounting.vat': {
            'Meta': {'object_name': 'Vat', 'db_table': "u'vat'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['accounting.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '25', 'decimal_places': '5', 'blank': 'True'})
        },
        'invoicing.invoice': {
            'Meta': {'object_name': 'Invoice', 'db_table': "u'invoices'"},
            'booking_period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.BookingPeriod']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoices'", 'to': "orm['main.Relation']"}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'full_invoice_no': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'main.bookingperiod': {
            'Meta': {'object_name': 'BookingPeriod', 'db_table': "u'booking_periods'"},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'main.contact': {
            'Meta': {'object_name': 'Contact', 'db_table': "u'contacts'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'displayname': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'givenname': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infix': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'mobilephone': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'relation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['main.Relation']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'})
        },
        'main.relation': {
            'Meta': {'object_name': 'Relation', 'db_table': "u'relations'"},
            'active_customer': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'active_supplier': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_by_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'invoice_contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['main.Contact']"}),
            'invoice_email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'invoice_name': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '180'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone1': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'phone2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'postal_address': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'postal_city': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'postal_country': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'postal_zip_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'visit_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '180', 'blank': 'True'}),
            'visit_city': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'visit_country': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'visit_zip_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['accounting']
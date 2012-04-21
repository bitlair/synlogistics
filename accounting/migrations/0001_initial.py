# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'accounts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=24)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('account_type', self.gf('django.db.models.fields.IntegerField')()),
            ('is_readonly', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_balance', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=25, decimal_places=5)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['accounting.Account'])),
        ))
        db.send_create_signal('accounting', ['Account'])

        # Adding model 'Transaction'
        db.create_table(u'transactions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', to=orm['accounting.Account'])),
            ('transfer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['accounting.Account'])),
            ('relation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', null=True, to=orm['main.Relation'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=765, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=25, decimal_places=5, blank=True)),
            ('invoice_number', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('purchase_order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', null=True, to=orm['main.PurchaseOrder'])),
            ('invoice_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invoicing.InvoiceItem'], null=True)),
            ('document', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('accounting', ['Transaction'])

        # Adding M2M table for field related on 'Transaction'
        db.create_table(u'transactions_related', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_transaction', models.ForeignKey(orm['accounting.transaction'], null=False)),
            ('to_transaction', models.ForeignKey(orm['accounting.transaction'], null=False))
        ))
        db.create_unique(u'transactions_related', ['from_transaction_id', 'to_transaction_id'])

        # Adding model 'Vat'
        db.create_table(u'vat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('percent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=25, decimal_places=5, blank=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['accounting.Account'])),
        ))
        db.send_create_signal('accounting', ['Vat'])

    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table(u'accounts')

        # Deleting model 'Transaction'
        db.delete_table(u'transactions')

        # Removing M2M table for field related on 'Transaction'
        db.delete_table('transactions_related')

        # Deleting model 'Vat'
        db.delete_table(u'vat')

    models = {
        'accounting.account': {
            'Meta': {'ordering': "['number']", 'object_name': 'Account', 'db_table': "u'accounts'"},
            '_balance': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '25', 'decimal_places': '5'}),
            'account_type': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_readonly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '24'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['accounting.Account']"})
        },
        'accounting.transaction': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Transaction', 'db_table': "u'transactions'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'to': "orm['accounting.Account']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '25', 'decimal_places': '5', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'document': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoicing.InvoiceItem']", 'null': 'True'}),
            'invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'purchase_order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'null': 'True', 'to': "orm['main.PurchaseOrder']"}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_rel_+'", 'to': "orm['accounting.Transaction']"}),
            'relation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'null': 'True', 'to': "orm['main.Relation']"}),
            'transfer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['accounting.Account']"})
        },
        'accounting.vat': {
            'Meta': {'object_name': 'Vat', 'db_table': "u'vat'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': "orm['accounting.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '25', 'decimal_places': '5', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        'invoicing.invoiceitem': {
            'Meta': {'object_name': 'InvoiceItem', 'db_table': "u'invoice_data'"},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '25', 'decimal_places': '5'}),
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['invoicing.Invoice']"}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoice_data'", 'null': 'True', 'to': "orm['main.Item']"}),
            'period': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoice_data'", 'to': "orm['main.Product']"}),
            'vat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounting.Vat']", 'null': 'True'})
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
            'email': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'givenname': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infix': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'mobilephone': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'relation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['main.Relation']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'})
        },
        'main.internalorder': {
            'Meta': {'object_name': 'InternalOrder', 'db_table': "u'internal_order'"},
            'amount_needed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'internal_orders'", 'to': "orm['main.Relation']"}),
            'customer_reference': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'for_customer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordered_by_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'internal_orders'", 'to': "orm['auth.User']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'internal_orders'", 'to': "orm['main.Product']"}),
            'product_description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'product_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'internal_orders'", 'to': "orm['main.ProductGroup']"}),
            'purchase_price_indication': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '25', 'decimal_places': '5', 'blank': 'True'}),
            'sale_order_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'selling_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '25', 'decimal_places': '5', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'supplier_suggestion': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['main.Relation']"})
        },
        'main.item': {
            'Meta': {'object_name': 'Item', 'db_table': "u'items'"},
            'arrival_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_by_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items_input'", 'to': "orm['auth.User']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['main.Location']"}),
            'purchase_order_data': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['main.PurchaseOrderItem']"}),
            'reserved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reserved_by_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items_reserved'", 'to': "orm['auth.User']"}),
            'reserved_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'reserved_for_relation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items_reserved'", 'to': "orm['main.Relation']"}),
            'serial_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '180'}),
            'sold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'written_off': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'written_off_by_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items_writtenoff'", 'to': "orm['auth.User']"})
        },
        'main.location': {
            'Meta': {'object_name': 'Location', 'db_table': "u'locations'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'postalzip': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'main.product': {
            'Meta': {'object_name': 'Product', 'db_table': "u'products'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'has_own_serials': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_interval': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'invoice_interval_count': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'maximum_stock': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'minimum_stock': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'product_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['main.ProductGroup']"}),
            'product_type': ('django.db.models.fields.IntegerField', [], {}),
            'vat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'null': 'True', 'to': "orm['accounting.Vat']"})
        },
        'main.productgroup': {
            'Meta': {'object_name': 'ProductGroup', 'db_table': "u'product_groups'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'main.purchaseorder': {
            'Meta': {'object_name': 'PurchaseOrder', 'db_table': "u'purchase_orders'"},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_orders'", 'to': "orm['main.Relation']"}),
            'external_order_reference': ('django.db.models.fields.CharField', [], {'max_length': '90', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_method': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'purchasing_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'relation_contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_orders'", 'to': "orm['main.Contact']"})
        },
        'main.purchaseorderitem': {
            'Meta': {'object_name': 'PurchaseOrderItem', 'db_table': "u'purchase_order_data'"},
            'expected_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_data'", 'to': "orm['main.InternalOrder']"}),
            'order_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'purchase_order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'data'", 'to': "orm['main.PurchaseOrder']"}),
            'purchase_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '25', 'decimal_places': '5', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'subproduct': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'purchase_data'", 'to': "orm['main.Subproduct']"}),
            'supplier_has_in_stock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'units_per_pack': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'main.relation': {
            'Meta': {'object_name': 'Relation', 'db_table': "u'relations'"},
            'active_customer': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'active_supplier': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_by_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'invoice_contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['main.Contact']"}),
            'invoice_email': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
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
            'visit_city': ('django.db.models.fields.CharField', [], {'max_length': '180', 'null': 'True', 'blank': 'True'}),
            'visit_country': ('django.db.models.fields.CharField', [], {'max_length': '180', 'null': 'True', 'blank': 'True'}),
            'visit_zip_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        'main.subproduct': {
            'Meta': {'object_name': 'Subproduct', 'db_table': "u'subproducts'"},
            'ean_upc_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '180'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subproducts'", 'to': "orm['main.Product']"})
        }
    }

    complete_apps = ['accounting']
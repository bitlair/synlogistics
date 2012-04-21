# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Relation.visit_zip_code'
        db.alter_column(u'relations', 'visit_zip_code', self.gf('django.db.models.fields.CharField')(default='', max_length=30))

        # Changing field 'Relation.visit_country'
        db.alter_column(u'relations', 'visit_country', self.gf('django.db.models.fields.CharField')(default='', max_length=180))

        # Changing field 'Relation.visit_city'
        db.alter_column(u'relations', 'visit_city', self.gf('django.db.models.fields.CharField')(default='', max_length=180))
    def backwards(self, orm):

        # Changing field 'Relation.visit_zip_code'
        db.alter_column(u'relations', 'visit_zip_code', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'Relation.visit_country'
        db.alter_column(u'relations', 'visit_country', self.gf('django.db.models.fields.CharField')(max_length=180, null=True))

        # Changing field 'Relation.visit_city'
        db.alter_column(u'relations', 'visit_city', self.gf('django.db.models.fields.CharField')(max_length=180, null=True))
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
        'main.container': {
            'Meta': {'object_name': 'Container', 'db_table': "u'containers'"},
            'container_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '180'}),
            'container_template': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'display_contents': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'sold': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'main.containeritem': {
            'Meta': {'object_name': 'ContainerItem', 'db_table': "u'container_data'"},
            'added_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'data'", 'to': "orm['main.Container']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'container_data'", 'to': "orm['main.Item']"})
        },
        'main.containertemplate': {
            'Meta': {'object_name': 'ContainerTemplate', 'db_table': "u'container_templates'"},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Product']", 'symmetrical': 'False'})
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
        'main.inventory': {
            'Meta': {'object_name': 'Inventory', 'db_table': "u'inventories'"},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'main.inventoryitem': {
            'Meta': {'object_name': 'InventoryItem', 'db_table': "u'inventory_data'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'data'", 'to': "orm['main.Inventory']"}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'item'", 'to': "orm['main.Item']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['main.Location']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '25', 'decimal_places': '5', 'blank': 'True'})
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
        'main.productsellingprice': {
            'Meta': {'object_name': 'ProductSellingprice', 'db_table': "u'product_sellingprices'"},
            'commencing_date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '25', 'decimal_places': '5', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sellingprices'", 'to': "orm['main.Product']"}),
            'set_date': ('django.db.models.fields.DateField', [], {})
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
            'visit_city': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'visit_country': ('django.db.models.fields.CharField', [], {'max_length': '180', 'blank': 'True'}),
            'visit_zip_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        },
        'main.subproduct': {
            'Meta': {'object_name': 'Subproduct', 'db_table': "u'subproducts'"},
            'ean_upc_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '180'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subproducts'", 'to': "orm['main.Product']"})
        }
    }

    complete_apps = ['main']
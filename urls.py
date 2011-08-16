from django.conf.urls.defaults import patterns, include, url

import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'main.views.login'),
	url(r'^main/layout$', 'main.views.layout'),
	url(r'^accounting/overview$', 'accounting.views.overview'),
	url(r'^accounting/transactions$', 'accounting.views.transactions'),
	url(r'^accounting/transactiondata', 'accounting.views.transaction_data'),
	url(r'^sales/invoicing$', 'invoicing.views.create'),
	url(r'^sales/subscriptions$', 'invoicing.views.subscriptions'),
	url(r'^sales/subscriptiondata', 'invoicing.views.subscription_data'),
	
	# Main Ajax fields, used in more than one app:
	url(r'^ajax/accountsearch.json$', 'ajax.views.get_accounts'),
	url(r'^ajax/relationsearch.json$', 'ajax.views.get_relations'),
	url(r'^ajax/productsearch.json$', 'ajax.views.get_products'),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	# url(r'^admin/', include(admin.site.urls)),
)

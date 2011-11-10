"""
SynLogistics URL mappings module.
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

from django.conf.urls.defaults import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'main.views.login'),
    url(r'^main/layout$', 'main.views.layout'),
    url(r'^accounting/overview$', 'accounting.views.overview'),
    url(r'^accounting/transactions$', 'accounting.views.transactions_view'),
    url(r'^accounting/transactiondata', 'accounting.views.transaction_data'),
    url(r'^sales/invoicing$', 'invoicing.views.create'),
    url(r'^sales/subscriptions$', 'invoicing.views.subscriptions_view'),
    url(r'^sales/subscriptiondata', 'invoicing.views.subscription_data'),
    
    # Main Ajax fields, used in more than one app:
    url(r'^ajax/accountsearch.json$', 'ajax.views.get_accounts'),
    url(r'^ajax/relationsearch.json$', 'ajax.views.get_relations'),
    url(r'^ajax/productsearch.json$', 'ajax.views.get_products'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

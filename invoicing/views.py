#
# SynLogistics: Invoicing module
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

from random import getrandbits
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login
from django.template import RequestContext 
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from django.db import transaction as db_trans
from decimal import *
from datetime import datetime

from main.models import Subscription, Relation, Product
import settings

@login_required
def create(request):
	c = RequestContext(request, {
		'BASE_URL': settings.BASE_URL,
		'uniquestring':	str(getrandbits(32)),
	})
	c.update(csrf(request))

	return render_to_response('invoicing/create.html', c)

@login_required
def subscriptions(request):
	c = RequestContext(request, {
		'BASE_URL': settings.BASE_URL,
		'uniquestring': str(getrandbits(32)),
	})
	c.update(csrf(request))

	return render_to_response('invoicing/subscriptions.html', c)

#
# This is the AJAX handler for the subscription data in the sales->subscriptions view.
#
@login_required
@db_trans.commit_manually
def subscription_data(request):
	# New subscriptions come in through a POST request
	if request.method == "POST": 
		response = json.loads(request.raw_post_data, parse_float=Decimal)

		# Catch phony record creation request.
		if response['product'] == 0 or response['startdate'] == None:
			return HttpResponse('')

		try:
			# insert the subscription
			subscription = Subscription()
			subscription.product = Product.objects.get(pk=int(response['product']))
			subscription.customer = Relation.objects.get(pk=int(response['customer']))
			subscription.start_date = datetime.strptime(response['startdate'], '%Y-%m-%dT%H:%M:%S')
			if response['enddate']:
				subscription.end_date = datetime.strptime(response['enddate'], '%Y-%m-%dT%H:%M:%S')
			subscription.discount = Decimal(response['discount'])
			subscription.intervals_per_invoice = response['intervals_per_invoice']
			subscription.extra_info = response['extra_info']
			subscription.active = response['active']
			subscription.save()


		except:
			db_trans.rollback()
			raise
		else:
			db_trans.commit()
		
			# The decimal can't be serialized by json
			response['discount'] = str(response['discount'])

			return HttpResponse(json.dumps({ 'success': True, 'data': response }))
	else:
		try:
			# TODO: Allow for filtering here!
			subscriptions = Subscription.objects.all()
		
			response = []
			for subscription in subscriptions:
				response.append({
						'product': subscription.product.id,
						'product_display': subscription.product.name,
						'customer': subscription.customer.id,
						'customer_display': subscription.customer.displayname,
						'startdate': str(subscription.start_date),
						'enddate': str(subscription.end_date),
						'discount': int(subscription.discount*10000)/10000,
						'intervals_per_invoice': subscription.intervals_per_invoice,
						'extra_info': subscription.extra_info,
						'active': subscription.active,
					})

			# This temporary variable is for benefit of django's lazy database retrieval that does 
			# database transactions late, when the json is built
		except:
			db_trans.rollback()
			raise
		else:
			db_trans.commit()
			return HttpResponse(json.dumps({ 'success': True, 'data': response }))
					

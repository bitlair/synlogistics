"""
SynLogistics: Invoicing and subscription views.
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

from random import getrandbits
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from decimal import Decimal
from datetime import datetime

from main.models import Relation, Product
from invoicing.models import Subscription
import settings

@login_required
def create(request):
    """ Displays the create invoice template """

    ctx = RequestContext(request, {
        'BASE_URL': settings.BASE_URL,
        'uniquestring':    str(getrandbits(32)),
    })
    ctx.update(csrf(request))

    return render_to_response('invoicing/create.html', ctx)

@login_required
def subscriptions_view(request):
    """ Displays the invoicing/subscriptions template """

    ctx = RequestContext(request, {
        'BASE_URL': settings.BASE_URL,
        'uniquestring': str(getrandbits(32)),
    })
    ctx.update(csrf(request))

    return render_to_response('invoicing/subscriptions.html', ctx)

@login_required
def subscription_data(request):
    """ AJAX handler for the subscription data in the sales->subscription view. """

    # New subscriptions come in through a POST request
    if request.method == "POST": 
        response = json.loads(request.raw_post_data, parse_float=Decimal)

        # Catch phony record creation request.
        if response['product'] == 0 or response['startdate'] == None:
            return HttpResponse('')

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

        # Make output parseable
        response['customer_display'] = subscription.customer.displayname
        response['product_display'] = subscription.product.name
        response['startdate'] = subscription.start_date.strftime("%Y-%m-%d")
        if response['enddate']:
            response['enddate'] = subscription.end_date.strftime("%Y-%m-%d")

        # The decimal can't be serialized by json
        response['discount'] = str(response['discount'])

        # Give the id to the frontend
        response['id'] = subscription.id

        return HttpResponse(json.dumps({ 'success': True, 'data': response }))

    # Updates come in as PUT subscriptiondata/id
    elif request.method == "PUT":
        response = json.loads(request.raw_post_data, parse_float=Decimal)

        subscription = Subscription.objects.get(pk=response['id'])
        subscription.product = Product.objects.get(pk=int(response['product']))
        subscription.customer = Relation.objects.get(pk=int(response['customer']))
        subscription.start_date = datetime.strptime(response['startdate'], '%Y-%m-%dT%H:%M:%S')

        if response['enddate']:
            subscription.end_date = datetime.strptime(response['enddate'], '%Y-%m-%dT%H:%M:%S')
        else:
            subscription.end_date = None

        subscription.discount = Decimal(response['discount'])
        subscription.intervals_per_invoice = response['intervals_per_invoice']
        subscription.extra_info = response['extra_info']
        subscription.active = response['active']
        subscription.save()

        # Make output parseable
        response['customer_display'] = subscription.customer.displayname
        response['product_display'] = subscription.product.name
        response['startdate'] = subscription.start_date.strftime("%Y-%m-%d")
        if response['enddate']:
            response['enddate'] = subscription.end_date.strftime("%Y-%m-%d")

        # The decimal can't be serialized by json
        response['discount'] = str(response['discount'])

        return HttpResponse(json.dumps({ 'success': True, 'data': response }))
        
    # A delete is done via DELETE subscriptiondata/id
    elif request.method == "DELETE":
        response = json.loads(request.raw_post_data, parse_float=Decimal)

        subscription = Subscription.objects.get(pk=response['id'])
        subscription.delete()

        return HttpResponse(json.dumps({ 'success': True }))
    else:
        # TODO: Allow for filtering here!
        subscriptions = Subscription.objects.all()

        response = []
        for subscription in subscriptions:
            response.append({
                    'id': subscription.id,
                    'product': subscription.product.id,
                    'product_display': subscription.product.name,
                    'customer': subscription.customer.id,
                    'customer_display': subscription.customer.displayname,
                    'startdate': subscription.start_date.strftime("%Y-%m-%d"),
                    'enddate': subscription.end_date.strftime("%Y-%m-%d")
                               if subscription.end_date else None,
                    'discount': int(subscription.discount*10000)/10000,
                    'intervals_per_invoice': subscription.intervals_per_invoice,
                    'extra_info': subscription.extra_info,
                    'active': subscription.active,
                })

        return HttpResponse(json.dumps({ 'success': True, 'data': response }))

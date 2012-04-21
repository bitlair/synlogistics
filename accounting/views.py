"""
SynLogistics accounting overview and transaction management views.
"""
#
# Copyright (C) by Wilco Baan Hofman <wilco@baanhofman.nl> 2011
# Copyright (C) by Rudy Hardeman <zarya@bitlair.nl> 2011
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
from django.contrib.auth.decorators import login_required
from django.template import RequestContext 
from django.http import HttpResponse
from django.utils import simplejson as json
from accounting.models import Account, Transaction
from main.models import Relation
from decimal import Decimal

import settings
from datetime import datetime


# XXX may want to replace this with simplejson
def show_children(children, account_id):
    accounttree_json = "expanded: true, children: ["
    for account in children[account_id]:
        accounttree_json += "{"
        accounttree_json += "id:'"+str(account.id)+"',"
        accounttree_json += "number:'"+account.number+"',"
        accounttree_json += "name:'"+account.name+"',"
        accounttree_json += "description:'"+account.description+"',"
        accounttree_json += "type:'"+account.get_account_type_display()+"',"
        accounttree_json += "balance:'"+str(account.balance)+"',"
        if not account.is_readonly:
            accounttree_json += "iconCls:'icon-readwrite',"
        if account.id in children:
            accounttree_json += show_children(children, account.id)
        else:
            accounttree_json += "leaf: true,"
        accounttree_json += "},"
    accounttree_json += "],"
    return accounttree_json

@login_required
def overview(request):
    """ Account tree overview view function. """

    accounts = Account.objects.all()

    # Build a dictionary with parent_id as key with lists of records as data
    # This is supposed to build a tree by referencing from parent
    children = {}
    for account in accounts:
        if account.parent_id:
            if not account.parent_id in children:
                children[account.parent_id] = []

            children[account.parent_id].append(account)
        else:
            if not 0 in children:
                children[0] = []

            children[0].append(account)

    # Create a recursive json tree of accounts
    # XXX may want to replace this with simplejson
    accounttree_json = '{'
    if 0 in children:
        accounttree_json += show_children(children, 0)
    accounttree_json += '}'

    ctx = RequestContext(request, {
        'BASE_URL': settings.BASE_URL,
        'uniquestring':    str(getrandbits(32)),
        'accounttree_json': accounttree_json,
    })
    ctx.update(csrf(request))

    return render_to_response('accounting/overview.html', ctx)

@login_required
def transactions_view(request):
    """ Transaction view, basically just serves the template """

    ctx = RequestContext(request, {
        'BASE_URL': settings.BASE_URL,
        'uniquestring':    str(getrandbits(32)),
        'account_id': request.POST['account'],
    })
    ctx.update(csrf(request))
    return render_to_response('accounting/transactions.html', ctx)


@login_required
def transaction_data(request):
    """ AJAX handler for transaction data in the transaction view """

    # New transactions come in through a POST request
    if request.method == "POST": 
        response = json.loads(request.raw_post_data, parse_float=Decimal)

        # Catch phony record creation request.
        if response['date'] == None:
            return HttpResponse('')

        # Insert the main transaction
        transaction = Transaction()
        transaction.account = Account.objects.get(pk=int(request.GET['account']))
        transaction.date = datetime.strptime(response['date'], '%Y-%m-%dT%H:%M:%S')
        transaction.transfer = Account.objects.get(pk=int(response['transfer']))
        transaction.description = response['description']
        if response['relation'] != 0:
            transaction.relation = Relation.objects.get(pk=int(response['relation']))
        transaction.amount = Decimal(response['amount'])
        transaction.save()

        response['transfer_display'] = '%s %s' % (transaction.transfer.number, transaction.transfer.name)
        response['id'] = transaction.id
        if transaction.relation != None:
            response['relation_display'] = transaction.relation.name

        return HttpResponse(json.dumps({ 'success': True, 'data': response }))
    
    # Existing transactions come in through a PUT request on /transactiondata/id
    elif request.method == "PUT":
        response = json.loads(request.raw_post_data, parse_float=Decimal)

        transaction = Transaction.objects.get(pk=response['id'])
        transaction.date = datetime.strptime(response['date'], '%Y-%m-%dT%H:%M:%S')
        transaction.transfer = Account.objects.get(pk=int(response['transfer']))
        transaction.description = response['description']
        transaction.amount = Decimal(response['amount'])

        if response['relation']:
            transaction.relation = Relation.objects.get(pk=int(response['relation']))
        transaction.save()


        response['transfer_display'] = '%s %s' % (transaction.transfer.number, transaction.transfer.name)
        if transaction.relation != None:
            response['relation_display'] = transaction.relation.name
        else:
            response['relation_display'] = ''

        return HttpResponse(json.dumps({ 'success': True, 'data': response }))

    # A delete  is done via DELETE /transactiondata/id
    elif request.method == "DELETE":
        response = json.loads(request.raw_post_data, parse_float=Decimal)

        transaction = Transaction.objects.get(pk=response['id'])

        # Delete the related transaction first (There can be only one!)
        assert transaction.related.count() == 1
        for related in transaction.related.all():
            related.delete()
        transaction.delete()

        return HttpResponse(json.dumps({ 'success': True }))

    # Requesting transactions is done via GET /transactiondata?account=..
    else:
        transactions = Transaction.objects.filter(account=request.GET['account'])
        # XXX May want to change this to use simplejson
        response = '{success:true,data:['
        for transaction in transactions:
            response += '{id:%d,' % transaction.id
            response += 'date:"%s",' % transaction.date
            response += 'transfer:%d,' % transaction.transfer.id
            response += 'transfer_display:"%s %s",' % (transaction.transfer.number, transaction.transfer.name)
            response += 'description:"%s",' % transaction.description
            if transaction.relation != None:
                response += 'relation:%d,' % transaction.relation.id
                response += 'relation_display:"%s",' % transaction.relation.name
            else:
                response += 'relation:null,'
                response += 'relation_display:"",'
            response += 'amount:%s},' % transaction.amount
        response += ']}'

        return HttpResponse(response)

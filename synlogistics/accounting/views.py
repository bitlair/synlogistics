from random import getrandbits
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login
from django.template import RequestContext 
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson as json
from main.models import Account, Transaction, Relation

import settings
import pprint
from datetime import datetime

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

def overview(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(settings.LOGIN_URL)
	
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
	accounttree_json = '{'
	if 0 in children:
		accounttree_json += show_children(children, 0)
	accounttree_json += '}'

	c = RequestContext(request, {
		'BASE_URL': settings.BASE_URL,
		'uniquestring':	str(getrandbits(32)),
		'accounttree_json': accounttree_json,
	})
	c.update(csrf(request))

	#accounttree_json = 'Dude<br>'
	#for account in Account.objects.all():
	#	accounttree_json += str(account.balance)+"<br>"
	#return HttpResponse(accounttree_json)

	return render_to_response('accounting/overview.html', c)

def transactions(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(settings.LOGIN_URL)

	# FIXME Remove Hack to make debugging easier
	account = 6
	if 'account' in request.POST:
		account = request.POST['account']
	
	transactions = Transaction.objects.filter(account=account)

	# Preseed arrays
	accounts = {}
	relations = {}
	for transaction in transactions:
		accounts[transaction.transfer.id] = str(transaction.transfer.number) + " " + transaction.transfer.name
		# Relation is not mandatory
		try:
			relations[transaction.relation.id] = str(transaction.relation.name)
		except:
			pass

	c = RequestContext(request, {
		'BASE_URL': settings.BASE_URL,
		'uniquestring':	str(getrandbits(32)),
		'account_id': account,
		'transactions': transactions,
		'accounts': accounts,
		'relations': relations,
	})
	c.update(csrf(request))
	return render_to_response('accounting/transactions.html', c)

def transaction_reader(request):
	if request.method == "POST": 
		response = json.loads(request.raw_post_data)
		if response['date'] != "":
			# insert the main transaction
			transaction = Transaction()
			transaction.account = Account.objects.get(pk=int(request.GET['account']))
			transaction.date = datetime.strptime(response['date'], '%Y-%m-%dT%H:%M:%S')
			transaction.transfer = Account.objects.get(pk=int(response['transfer']))
			transaction.description = response['description']
			transaction.relation = Relation.objects.get(pk=int(response['relation']))
			transaction.amount = response['amount']
			transaction.save()
		
			related = Transaction()
			related.account = Account.objects.get(pk=int(response['transfer']))
			related.date = datetime.strptime(response['date'], '%Y-%m-%dT%H:%M:%S')
			related.transfer = Account.objects.get(pk=int(request.GET['account'])) 
			related.description = response['description']
			related.relation = Relation.objects.get(pk=int(response['relation']))
			related.amount = response['amount']
			related.save()

			transaction.related.add(related)
			transaction.save()

			related.related.add(transaction)
			related.save()
			return HttpResponse('{success: true, data: %s }' % request.raw_post_data)
		else:	
			return HttpResponse('')
	else:
		transactions = Transaction.objects.filter(account=request.GET['account'])
		response = '{success:true,data:['
		for transaction in transactions:
			response += '{id:%d,' % transaction.id
			response += 'date:"%s",' % transaction.date
			response += 'transfer:%d,' % transaction.transfer.id
			response += 'description:"%s",' % transaction.description
			try:
				response += 'relation:%d,' % transaction.relation.id
			except:
				response += 'relation:null,'
			response += 'amount:%d},' % transaction.amount
		response += ']}'
		return HttpResponse(response)		
	
def transaction_writer(request):
	if request.META['REQUEST_METHOD'] == "PUT":
		response = json.loads(request.raw_post_data)
		transaction = Transaction.objects.get(pk=response['id'])
		transaction.date = datetime.strptime(response['date'], '%Y-%m-%dT%H:%M:%S')
		transaction.transfer = Account.objects.get(pk=int(response['transfer']))
		transaction.description = response['description']
		transaction.relation = Relation.objects.get(pk=int(response['relation']))
		transaction.amount = response['amount']
		for related in transaction.related.all():
			related.date = datetime.strptime(response['date'], '%Y-%m-%dT%H:%M:%S')
			related.account = Account.objects.get(pk=int(response['transfer']))
			related.description = response['description']
			related.relation = Relation.objects.get(pk=int(response['relation']))
			related.amount = response['amount']
			related.save()
		transaction.save()
		
		# FIXME Actually do something with the request
		#return HttpResponse(response)
		return HttpResponse('{success: true, data: %s }' % request.raw_post_data)

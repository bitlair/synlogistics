from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

from main.models import Account, Relation

def relations(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(settings.LOGIN_URL)

	# Obscure errors ftw \o/
	if not 'query' in request.GET:
		return HttpResponse("")

	relations = Relation.objects.filter(displayname__icontains=request.GET['query']).order_by('displayname')

	response = "{relations:["
	for relation in relations:
		 response += "{ id:'"+str(relation.id)+"',name:'"+relation.displayname+"'},"
	response += "]}"

	return HttpResponse(response, mimetype='application/json')

def accounts(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(settings.LOGIN_URL)

	# Obscure errors ftw \o/
	if not 'query' in request.GET:
		return HttpResponse("")

	accounts = Account.objects.filter(Q(number__icontains=request.GET['query'])|Q(name__icontains=request.GET['query'])).order_by('number')

	response = "{accounts:["
	for account in accounts:
		 response += "{ id:'"+str(account.id)+"',name:'"+account.number+" "+account.name+"'},"
	response += "]}"

	return HttpResponse(response, mimetype='application/json' )



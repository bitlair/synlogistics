#
# SynLogistics AJAX JSON server interaction for common search boxes, etc.
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



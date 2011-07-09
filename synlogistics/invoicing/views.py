from random import getrandbits
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login
from django.template import RequestContext 
from django.http import HttpResponse, HttpResponseRedirect
import settings

def create(request):
	c = RequestContext(request, {
		'BASE_URL': settings.BASE_URL,
		'uniquestring':	str(getrandbits(32)),
	})
	c.update(csrf(request))

	return render_to_response('invoicing/create.html', c)


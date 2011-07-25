from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login
from django.template import RequestContext 
from django.http import HttpResponseRedirect

import settings

def login(request):
	error = ""
	if 'login' in request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				# Redirect to a success page.
				return HttpResponseRedirect("main/layout")
			else:
				error = "Your account is disabled."
		else:
			error = "Invalid username or password"
	c = RequestContext(request, {
		'error': error,
		'request': request
	})
	c.update(csrf(request))

	return render_to_response('main/login.html', c)

def layout(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(settings.LOGIN_URL)
	
	c = RequestContext(request, {
		'request': request,
		'BASE_URL': settings.BASE_URL
	})
	c.update(csrf(request))

	return render_to_response('main/layout.html', c)

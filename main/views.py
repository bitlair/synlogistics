"""
SynLogistics base login system and layout manager views
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

from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login as auth_login
from django.template import RequestContext 
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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
    ctx = RequestContext(request, {
        'error': error,
        'request': request
    })
    ctx.update(csrf(request))

    return render_to_response('main/login.html', ctx)

@login_required
def layout(request):
    ctx = RequestContext(request, {
        'request': request,
        'BASE_URL': settings.BASE_URL
    })
    ctx.update(csrf(request))

    return render_to_response('main/layout.html', ctx)

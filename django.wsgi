import os
import sys

sys.path.append('/home/http/wilco/')
sys.path.append('/home/http/wilco/synlogistics')

os.environ['DJANGO_SETTINGS_MODULE'] = 'synlogistics.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

import os
import sys

sys.path.append('/usr/share/synlogistics')

os.environ['DJANGO_SETTINGS_MODULE'] = 'synlogistics.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

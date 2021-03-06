# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Bootstrap for running a Django app under Google App Engine.

The site-specific code is all in other files: settings.py, urls.py,
models.py, views.py.  And in fact, only 'settings' is referenced here
directly -- everything else is controlled from there.

"""

# Standard Python imports.
import os
import sys
import logging
# Google App Engine imports.
from google.appengine.ext.webapp import util


# Uninstall Django 0.96.
for k in [k for k in sys.modules if k.startswith('django')]:
  del sys.modules[k]

# Add Django 1.0 archive to the path.
django_path = 'django.zip'
sys.path.insert(0, django_path)

from appengine_django import InstallAppengineHelperForDjango
InstallAppengineHelperForDjango()



# Import the part of Django that we use here.
import django.core.handlers.wsgi

def main():

  # Create a Django application for WSGI.
  application = django.core.handlers.wsgi.WSGIHandler()

  # Run the WSGI CGI handler with that application.
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()


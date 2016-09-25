"""
WSGI config for buono project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buono.settings")

application = get_wsgi_application()

#本番設定
if os.environ.get('PRODUCTION') == 'True':
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(application)

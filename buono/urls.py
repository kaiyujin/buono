from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<generation_id>[0-9]+)/$', views.listForGeneration, name='listForGeneration'),
]

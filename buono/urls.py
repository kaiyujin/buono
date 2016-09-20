from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<generation_id>[0-9]+)/$', views.listForGeneration, name='listForGeneration'),
    url(r'^(?P<generation_id>[0-9]+)/appealPoint/(?P<appealPointId>[0-9]+)/$', views.detail, name='appealPoint'),
    url(r'^(?P<generation_id>[0-9]+)/appealPoint/update/$', views.update, name='appealPointUpdate'),
    url(r'^appealPoint/updated/$', views.updated, name='appealPointUpdated'),
]

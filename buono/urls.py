from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<appealPointId>[0-9]+)/$', views.detail, name='appealPoint'),
    url(r'^update/$', views.update, name='appealPointUpdate'),
    url(r'^addComment/$', views.addComment, name='addComment'),
    url(r'^logout/$', logout ,name="logout"),
]

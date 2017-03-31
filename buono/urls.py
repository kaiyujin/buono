from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<appealPointId>[0-9]+)/$', views.detail, name='appealPoint'),
    url(r'^update/$', views.update, name='appealPointUpdate'),
    url(r'^addComment/$', views.addComment, name='addComment'),
    url(r'^vote/$', views.vote, name='vote'),
    url(r'^logout/$', logout ,name="logout"),
    url(r'^showComment/$', views.showComment ,name="showComment"),
    url(r'^countBuono/$', views.countBuono ,name="countBuono"),
]

from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^$', views.index, name='index1'),
	url(r'^index', views.index, name='index2'),
	url(r'^login', views.login, name='login'),
	url(r'^register', views.register, name='register'),
	url(r'^run',views.run),

]
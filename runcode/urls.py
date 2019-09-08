from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^home', views.home, name='home'),
	url(r'^login', views.login, name='login'),
	url(r'^register', views.register, name='register'),
	url(r'^run',views.run, name='run'),
	url(r'^logout',views.logout, name='logout'),
	url(r'^mypage',views.login_check, name='login_from_mypage'),
	url(r'^profile',views.profile, name='profile'),
	url(r'^services',views.services, name='services'),
	url(r'^manual',views.manual, name='manual'),

]
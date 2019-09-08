from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^keyboard/',views.keyboard),
    url(r'^message',views.answer),
]
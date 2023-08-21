from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('sign-up', views.sign_up),
    path('create-message', views.create_message),
    path('quickstart', views.quickstart),
]
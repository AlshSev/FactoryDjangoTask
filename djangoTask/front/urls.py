from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('sign-up', views.sign_up),
    path('create-post', views.create_post),
]
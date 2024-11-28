from django.urls import path
from . import views


# create urls 
urlpatterns = [
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
]
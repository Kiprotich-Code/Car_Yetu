from django.urls import path
from . import views

# urlpatterns 
urlpatterns = [
    path('', views.index, name='index'),
    path('images_list/', views.images_list, name='images_list'),
]
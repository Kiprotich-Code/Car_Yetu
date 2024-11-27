from django.urls import path
from . import views

# urlpatterns 
urlpatterns = [
    path('', views.index, name='index'),
    path('images_list/', views.images_list, name='images_list'),
    path('image_create/', views.image_create, name='image_create'),
]
from django.urls import path
from . import views

# urlpatterns 
urlpatterns = [
    path('', views.index, name='index'),
    path('images_list/', views.images_list, name='images_list'),
    path('image_create/', views.image_create, name='image_create'),

    # detail 
    path('images/<int:image_id>/', views.image_detail, name='image_detail'),
    path('images/update/<int:image_id>/', views.image_update, name='image_update'),
    path('images/delete/<int:image_id>/', views.image_delete, name='image_delete'),
]
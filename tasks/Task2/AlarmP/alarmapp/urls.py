from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('station/add/', views.add_station, name='add_station'),
    path('station/<int:station_id>/threshold/add/', views.add_threshold, name='add_threshold'),
    path('threshold/<int:threshold_id>/', views.threshold_detail, name='threshold_detail'),
    path('threshold/<int:threshold_id>/edit/', views.edit_threshold, name='edit_threshold'),
    path('threshold/<int:threshold_id>/delete/', views.delete_threshold, name='delete_threshold'),
]

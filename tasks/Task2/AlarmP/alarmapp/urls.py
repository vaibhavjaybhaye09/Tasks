from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Threshold CRUD
    path(
        'threshold/add/<int:station_id>/',
        views.add_threshold,
        name='add_threshold'
    ),

    path(
        'threshold/edit/<int:threshold_id>/',
        views.edit_threshold,
        name='edit_threshold'
    ),

    path(
        'threshold/delete/<int:threshold_id>/',
        views.delete_threshold,
        name='delete_threshold'
    ),
]

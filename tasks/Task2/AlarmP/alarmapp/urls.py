from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('station/add/', views.add_station, name='add_station'),

    path(
        'station/<int:station_id>/value/',
        views.update_value,
        name='update_value'
    ),

    path(
        'station/<int:station_id>/limit/',
        views.update_limit,
        name='update_limit'
    ),
]

from django.contrib import admin
from .models import Station, Threshold


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'current_value')
    search_fields = ('name',)


@admin.register(Threshold)
class ThresholdAdmin(admin.ModelAdmin):
    list_display = ('id', 'station', 'limit_value')
    search_fields = ('station__name',)

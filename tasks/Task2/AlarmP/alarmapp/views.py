from django.shortcuts import render
from .models import Station
from .utils import get_station_status

def dashboard(request):
    stations = Station.objects.prefetch_related('thresholds')

    data = []
    for station in stations:
        thresholds = station.thresholds.all()
        status = get_station_status(station.current_value, thresholds)

        data.append({
            "name": station.name,
            "value": station.current_value,
            "status": status,
            "thresholds": thresholds
        })

    return render(request, "dashboard.html", {"stations": data})

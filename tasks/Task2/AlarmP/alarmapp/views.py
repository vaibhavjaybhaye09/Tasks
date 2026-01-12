from django.shortcuts import render, redirect, get_object_or_404
from .models import Station, Threshold
from .forms import ThresholdForm, StationForm
from .utils import get_station_status

def dashboard(request):
    stations = Station.objects.prefetch_related('thresholds')
    station_data = []
    for station in stations:
        thresholds = list(station.thresholds.all())
        status = get_station_status(station.current_value, thresholds)
        station_data.append({
            'id': station.id,
            'name': station.name,
            'value': station.current_value,
            'status': status,
            'thresholds': thresholds,
        })
    return render(request, 'alarmapp/dashboard.html', {'stations': station_data})

def add_threshold(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    form = ThresholdForm(request.POST or None)
    if form.is_valid():
        threshold = form.save(commit=False)
        threshold.station = station
        threshold.save()
        return redirect('dashboard')
    return render(request, 'alarmapp/threshold_form.html', {'form': form, 'station': station})

def edit_threshold(request, threshold_id):
    threshold = get_object_or_404(Threshold, id=threshold_id)
    form = ThresholdForm(request.POST or None, instance=threshold)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'alarmapp/threshold_form.html', {'form': form})

def delete_threshold(request, threshold_id):
    threshold = get_object_or_404(Threshold, id=threshold_id)
    threshold.delete()
    return redirect('dashboard')

def threshold_detail(request, threshold_id):
    threshold = get_object_or_404(Threshold, id=threshold_id)
    return render(request, 'alarmapp/threshold_detail.html', {'threshold': threshold})

def add_station(request):
    form = StationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'alarmapp/station_form.html', {'form': form})
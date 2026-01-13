from django.shortcuts import render, redirect, get_object_or_404
from .models import Station, Threshold
from .forms import StationForm, ThresholdForm
from django.contrib import messages


# --------------------
# DASHBOARD
# --------------------
def dashboard(request):
    stations = Station.objects.select_related('threshold')

    data = []
    for s in stations:
        alarm = False
        alert = None
        limit = None

        if hasattr(s, 'threshold'):
            limit = s.threshold.limit_value
            if s.current_value > limit:
                alarm = True
                alert = "ALERT! Limit crossed"

        data.append({
            'id': s.id,
            'name': s.name,
            'value': s.current_value,
            'limit': limit,
            'alarm': alarm,
            'alert': alert,
        })

    return render(request, 'alarmapp/dashboard.html', {
        'stations': data
    })


# --------------------
# ADD STATION
# --------------------
def add_station(request):
    form = StationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'alarmapp/station_form.html', {
        'form': form
    })


# --------------------
# UPDATE CURRENT VALUE
# --------------------
def update_value(request, station_id):
    station = get_object_or_404(Station, id=station_id)

    if request.method == 'POST':
        value = int(request.POST.get('current_value', 0))
        if value >= 0:
            station.current_value = value
            station.save()
        return redirect('dashboard')

    return render(request, 'alarmapp/update_value.html', {
        'station': station
    })


# --------------------
# UPDATE THRESHOLD (LIMIT)
# --------------------
def update_limit(request, station_id):
    station = get_object_or_404(Station, id=station_id)

    threshold, _ = Threshold.objects.get_or_create(
        station=station,
        defaults={'limit_value': 1}   # ✅ IMPORTANT
    )

    form = ThresholdForm(request.POST or None, instance=threshold)
    if form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'alarmapp/update_limit.html', {
        'form': form,
        'station': station
    })

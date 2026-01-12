def get_station_status(current_value, thresholds):
    for t in thresholds:
        if t.status_type == 'WRONG' and current_value >= t.limit_value:
            return 'WRONG'
    return 'RIGHT'
8
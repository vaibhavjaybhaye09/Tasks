def get_station_status(current_value, thresholds):
    """
    Return 'WRONG' if any threshold with status_type == 'WRONG' has limit_value <= current_value.
    Otherwise return 'RIGHT'.
    """
    for t in thresholds:
        if t.status_type == 'WRONG' and current_value >= t.limit_value:
            return 'WRONG'
    return 'RIGHT'
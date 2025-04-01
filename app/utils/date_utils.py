from datetime import datetime,date

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%dT%H:%M').date()
    except ValueError:
        raise ValueError("Data no formato invalido. Utilize o formato yyyy-mm-ddTHH:MM")

def format_date(date_obj):
    if isinstance(date_obj, datetime):
        return date_obj.strftime('%Y-%m-%dT%H:%M')
    return date_obj 

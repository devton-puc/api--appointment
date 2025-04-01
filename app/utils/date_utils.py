from datetime import datetime,date

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S').date()
    except ValueError:
        raise ValueError("Data no formato invalido. Utilize o formato yyyy-mm-ddTHH:MM:SS")

def format_date(date_obj):
    if isinstance(date_obj, datetime):
        return date_obj.strftime('%Y-%m-%dT%H:%M:%S')
    return date_obj 

import pytz
from datetime import datetime, timedelta

class Set_DateTime:

    def define_datime_now():
        tz = pytz.timezone('America/Sao_Paulo')
        sp_time = datetime.now(tz)
        return sp_time.strftime("%d/%m/%Y %H:%M:%S")
    
    def define_days_timedelta(date, days):
        parsed_date = datetime.strptime(date, '%d/%m/%Y')
        new_date = parsed_date + timedelta(days=days)
        return new_date.strftime("%d/%m/%Y")


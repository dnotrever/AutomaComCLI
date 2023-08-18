import pytz
from datetime import datetime

class Datetime_Now:

    def define_datime_now():
        tz = pytz.timezone('America/Sao_Paulo')
        sp_time = datetime.now(tz)
        return sp_time.strftime("%d/%m/%Y %H:%M:%S")


import datetime
from datetime import date
current_date = date.today()
current_day = current_date.strftime('%d')
current_month = current_date.strftime('%m')
tomorrow_date = current_date + datetime.timedelta(days=1)
tomorrow_day = tomorrow_date.strftime('%d')
tomorrow_month = tomorrow_date.strftime('%m')
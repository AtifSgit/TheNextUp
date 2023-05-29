from datetime import date, timedelta, timezone
today = date.today()
month = today.month
year = today.year
dates = []
current_date = date(year, month, 1)
last_day = date(year, month, 1) + timedelta(days=31)
while current_date.month == month:
    dates.append(current_date.strftime('%d/%m/%Y'))
    current_date += timedelta(days=1)
    if current_date == last_day:
        break
print(dates)
print(today)
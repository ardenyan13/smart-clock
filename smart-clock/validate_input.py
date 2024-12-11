import re
from datetime import datetime

# pattern for time (2 digits for both hour and minute)
time_pattern = r'^\d{2}$'

# pattern for date (MM/DD/YY)
date_pattern = r'^\d{2}/\d{2}/\d{2}$'

def is_hour_valid(time):
    # check if the hour is 2 digits and 1 <= time <= 12
    return re.match(time_pattern, time) and 1 <= int(time) <= 12 

def is_minute_valid(time):
    # check if the minute is 2 digits and 0 <= time <= 59
    return re.match(time_pattern, time) and 0 <= int(time) <= 59

def is_date_valid(date):
    # check if the date is correct and 1 <= month <= 12 and 1 <= day <= 31
    if re.match(date_pattern, date):
        try:
            datetime.strptime(date, "%m/%d/%y")
            return True
        except ValueError:
            return False
    return False
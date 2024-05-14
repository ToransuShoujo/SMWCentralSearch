from datetime import datetime

days_in_month = [31, 28, 31, 30, 31, 30, 31, 30, 31, 30, 31, 30, 31]


def datetime_to_dict(date):
    return {
        'sec': 0,
        'min': 0,
        'hour': 0,
        'month_day': date.day,
        'month': date.month - 1,
        'year': date.year - 1900,
        'week_day': date.weekday() + 1,
        'year_day': get_year_day(date),
        'daylight_savings': 0
    }


def get_year_day(date):
    year_day = 0

    for i in range(1, date.month):
        year_day = year_day + days_in_month[i]
    year_day = year_day + date.day
    return year_day

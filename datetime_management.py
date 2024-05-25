from datetime import datetime, timezone, timedelta
import pytz

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


def dict_to_datetime(dictionary, time="00:00:00"):
    date = datetime(dictionary.get('year') + 1900, dictionary.get('month') + 1, dictionary.get('month_day'))
    if time is None:
        time = "00:00:00"
    time = time.split(':')
    print(f"{time[0]}:{time[1]}:{time[2]}")
    date = date.replace(hour=int(time[0]), minute=int(time[1]), second=int(time[2]))
    print(date)
    return date


def get_year_day(date):
    year_day = 0

    for i in range(1, date.month):
        year_day = year_day + days_in_month[i]
    year_day = year_day + date.day
    return year_day


def convert_to_timestamp(unformatted_time, time_type):
    if time_type == "smwc":
        smwc_time_naive = datetime.strptime(unformatted_time, "%Y-%m-%d %H:%M:%S %p")
        if 'PM' in unformatted_time:
            smwc_time_naive = smwc_time_naive + timedelta(hours=12)
        smwc_time_aware = smwc_time_naive.replace(tzinfo=pytz.timezone('GMT'))
        smwc_time_utc = smwc_time_aware.astimezone(pytz.UTC)
        smwc_timestamp = smwc_time_utc.timestamp()
        return smwc_timestamp
    elif time_type == "cloudflare":
        cloudflare_time_naive = datetime.strptime(unformatted_time, "%a, %d %b %Y %H:%M:%S GMT")
        cloudflare_time_aware = cloudflare_time_naive.replace(tzinfo=pytz.timezone('GMT'))
        cloudflare_time_utc = cloudflare_time_aware.replace(tzinfo=pytz.UTC)
        cloudflare_timestamp = cloudflare_time_utc.timestamp()
        return cloudflare_timestamp
    elif time_type == "datetime":
        dt_time_aware = unformatted_time.replace(tzinfo=datetime.now().astimezone().tzinfo)
        dt_time_utc = dt_time_aware.astimezone(pytz.UTC)
        dt_timestamp = dt_time_utc.timestamp()
        return dt_timestamp
    else:
        raise Exception("Unknown time passed to convert_to_timestamp function.\nValid types: smwc, cloudflare")


def timestamp_to_readable(timestamp):
    current_tzinfo = datetime.now().astimezone().tzinfo

    timestamp_datetime = datetime.fromtimestamp(timestamp)
    datetime_aware = timestamp_datetime.astimezone(current_tzinfo)
    return datetime_aware.strftime("%Y-%m-%d %H:%M:%S")
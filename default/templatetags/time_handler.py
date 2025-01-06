from django import template
import datetime
from django.utils import timezone
from django.conf import settings
import pytz

register = template.Library() 

def format(input, until=True):
    res = "in "
    if not until:
        res = ""

    order = ["y", "m", "d", "h"]
    words = {"h": "hour", "d": "day", "y": "year", "m": "month"}

    looped = 0

    for unit in order:
        if unit in input:
            looped += 1
            value = input[unit]
            word = words[unit]
            word += "s" if value > 1 else ""

            if unit == "h" and (value == 0 or (value == 1 and "mi" in input and input["mi"] < 0)):
                res += "<"
                value = max(1, value)

            res += f"{value} {word}"

            if looped < len(input) and (looped < len(input)-1 and "mi" in input):
                res += ", "

    if not until:
        res += " ago"

    return res


@register.filter(name='time_until') 
def time_until(date, time=None):
    now = datetime.datetime.now()

    h = None
    if not time:
        h = date.hour - now.hour
    else:
        h = time.hour - now.hour

    m = date.month - now.month
    d = date.day - now.day
    y = date.year - now.year

    res = {}

    if (h >= 0 and (m == 0 and d == 0 and y == 0)):
        res["h"] = h
    if (m > 0):
        res["m"] = m
    if (d > 0 and y == 0):
        res["d"] = d
    if (y > 0):
        res["y"] = y

    if (h <= 1 and (m == 0 and d == 0 and y == 0)):
        res["mi"] = time.minute - now.minute

    return format(res)


@register.filter(name='time_passed') 
def time_passed(date, time=None):
    now = datetime.datetime.now()

    h = None
    if not time:
        h = now.hour - date.hour
    else:
        h = now.hour - time.hour

    m = now.month - date.month
    d = now.day - date.day
    y = now.year - date.year

    res = {}

    if (h >= 0 and (m == 0 and d == 0 and y == 0)):
        res["h"] = h
    if (m > 0):
        res["m"] = m
    if (d > 0 and y == 0):
        res["d"] = d
    if (y > 0):
        res["y"] = y

    return format(res, False)


@register.filter(name="time_until_or_passed")
def time_until_or_passed(date, time=None):
    if time_until(date, time) != "in ":
        return time_until(date, time)
    else:
        return time_passed(date, time) 


@register.filter(name="calculate_end_time")
def calculate_end_time(date_time, duration):
    new_time = date_time+duration
    
    new_time = timezone.localtime(new_time, pytz.timezone('America/Chicago'))

    return new_time.time()

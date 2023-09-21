
from adafruit_pcf8563.pcf8563 import PCF8563

def set_time():
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2023, 9, 21, 19, 50, 0, 3, -1, -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    print("Setting time to:", t)  # uncomment for debugging
    rtc.datetime = t
    print()

def print_time();

    if rtc.datetime_compromised:
        print("RTC unset")
    else:
        print("RTC reports time is valid")
        t = rtc.datetime
        # print(t)     # uncomment for debugging
        print(
            "The date is {} {}/{}/{}".format(
                days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
            )
        )
        print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
    

from datetime import datetime, time, date


def in_range_time(start_hm, end_hm):
    now = datetime.now().time()
    t_start = time(*start_hm)
    t_end = time(*end_hm)

    if t_start <= t_end:
        return t_start <= now <= t_end
    else:
        return now >= t_start or now <= t_end

def is_weekend():
    today = date.today()
    return today.weekday() >= 5

if __name__ == "__main__":
    res = in_range_time((8,0),(10,0))
    print(res)

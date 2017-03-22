from utils.scheduler import Scheduler


def check_new_day(func):
    def wrapper(*args, **kwargs):
        Scheduler().new_day_cleaner()
        func(*args, **kwargs)

    return wrapper

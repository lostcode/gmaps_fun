import functools


def catch_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            import traceback
            print(traceback.format_exc())
    return wrapper


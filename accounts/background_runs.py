import time

from datetime import datetime

try:
    import uwsgi
    from uwsgidecorators import spool

    SPOOL_OK = uwsgi.SPOOL_OK
    SPOOL_RETRY = uwsgi.SPOOL_RETRY
    SPOOL_IGNORE = uwsgi.SPOOL_IGNORE
except (ImportError, ModuleNotFoundError):
    from functools import wraps

    SPOOL_OK = -2
    SPOOL_RETRY = -1
    SPOOL_IGNORE = 0

    uwsgi = None

    def spool(*decorator_args, **decorator_kwargs):
        def decorator(func):
            @wraps(func)
            def wrapper_func(*args, **kwargs):
                func(*args, **kwargs)
            return wrapper_func
        return decorator


@spool(pass_arguments=True)
def log_user_changes(user_obj, **kwargs):

    with open('users.txt', 'a') as file:
        file.write(f'{user_obj.get_full_name()} has been Updated his profile at {datetime.now()}\n')
    time.sleep(10)
    return SPOOL_OK

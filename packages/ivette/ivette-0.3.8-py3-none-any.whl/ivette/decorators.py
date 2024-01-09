import functools
import sys
import time
import httpcore
import httpx

from ivette.utils import print_color


import warnings


def http_request(func):
    def wrapper(*args, **kwargs):
        max_retries = 5  # Set your maximum number of retries here
        retries = 0
        while True:
            try:
                return func(*args, **kwargs)
            except (
                httpx.ConnectTimeout,
                httpx.ReadTimeout,
                httpx.ConnectError,
                httpx.RemoteProtocolError,
                httpcore.RemoteProtocolError,
                httpx.WriteError,
                httpcore.WriteError
            ):
                retries += 1
                if retries > max_retries:
                    warnings.warn(
                        f"Connection warning: {func.__name__} failed after {max_retries} retries.")
                time.sleep(2)
                continue
    return wrapper


def main_process(exit_message):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (KeyboardInterrupt, SystemExit) as e:
                print_color(f"{exit_message}", "34")
                sys.exit()
        return wrapper
    return decorator

import functools
import time
from functools import wraps


def timeit(func: callable):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def log_decorator(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Starting function '{func.__name__}'...")
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in function '{func.__name__}': {e}")
                raise e
            finally:
                end_time = time.time()
                elapsed_time = end_time - start_time
                logger.info(f"Finished function '{func.__name__}' in {elapsed_time:.4f} seconds")
            
            return result
        return wrapper
    return decorator

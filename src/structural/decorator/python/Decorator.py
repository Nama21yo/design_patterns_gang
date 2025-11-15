import logging
import functools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

@log_calls
def greet(name):
    return f"Hi, {name}!"

add(2, 3)
greet("Alice")

# INFO:__main__:Calling add with args: (2, 3), kwargs: {}
# INFO:__main__:add returned: 5
# INFO:__main__:Calling greet with args: ('Alice',), kwargs: {}
# INFO:__main__:greet returned: Hi, Alice!

# Why Use Decorators for Logging?
# Separation of concerns: Keep your main function uncluttered by logging code.

# Consistency: Add logging to many functions or methods with one line (@log_calls).

# Reusability: The decorator can be reused and extended easily with new logging logic.

# Decorators are one of Python's most powerful features for adding cross-cutting concerns like logging without repeatedly modifying source functions. If you want to log exceptions, add timing, or nest multiple decorators, you can combine or extend these patterns easily

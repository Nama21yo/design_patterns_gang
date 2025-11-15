# Python's `@` Decorator Syntax Explained

The `@` symbol in Python is **syntactic sugar** for function decorators. A decorator is a function that wraps another function, allowing you to add **extra behavior** before or after the original function runs—**without modifying its source code**.[1][2][5][6]

---

## How the `@` Works

- The `@decorator` syntax above a function definition is short for:
  `func = decorator(func)`
- When you use `@`, you pass your function to the decorator, which returns a wrapped version (usually called `wrapper`).

## Step-by-Step Example

Let's start without `@` to see what's really happening:

```python
def add_greeting(func):
    def wrapper():
        print("Hello!")
        func()
        print("Have a nice day!")
    return wrapper

def say_name():
    print("I'm Alice.")

# Decorating manually
say_name = add_greeting(say_name)

say_name()
```

**Output:**

```
Hello!
I'm Alice.
Have a nice day!
```

Now, do the same thing _with_ `@`:

```python
@add_greeting
def say_name():
    print("I'm Alice.")

say_name()
```

**This has exactly the same effect!**

---

## Decorators With Arguments

Most real-world functions take arguments, so your decorator needs to handle them:

```python
def print_args(func):
    def wrapper(*args, **kwargs):
        print(f"Arguments: {args}, {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@print_args
def greet(name, punctuation="!"):
    print(f"Hi, {name}{punctuation}")

greet("Alice", punctuation=".")
```

**Output:**

```
Arguments: ('Alice',), {'punctuation': '.'}
Hi, Alice.
```

---

## Real Example: Timing a Function

Below, we log how long a function takes using a decorator:

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_square(x):
    time.sleep(1)
    return x * x

slow_square(7)
```

---

## Takeaways

- The `@decorator` is just a shorthand for wrapping a function.
- Decorators add behavior (logging, timing, access control, etc.) **before and/or after** the original function runs.
- You can _stack_ decorators (use multiple `@` lines) for layered effects.[8]

If you'd like, I can show function-based decorators for your pizza example, or how to chain several decorators together!

[1](https://www.geeksforgeeks.org/python/decorators-in-python/)
[2](https://www.programiz.com/python-programming/decorator)
[3](https://realpython.com/primer-on-python-decorators/)
[4](https://www.datacamp.com/tutorial/decorators-python)
[5](https://www.w3schools.com/python/python_decorators.asp)
[6](https://book.pythontips.com/en/latest/decorators.html)
[7](https://peps.python.org/pep-0318/)
[8](https://www.youtube.com/watch?v=U-G-mSd4KAE)
[9](https://www.reddit.com/r/learnpython/comments/1h4vb1q/can_someone_explain_to_me_how_do_decorators_work/)
[10](https://www.freecodecamp.org/news/python-decorators-explained/)

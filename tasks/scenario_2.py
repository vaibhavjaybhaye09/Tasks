import time

def log_execution_time(func):
    def wrapper(n):
        start = time.time()
        result = func(n)
        end = time.time()
        print("Time taken:", end - start, "seconds")
        return result
    return wrapper


@log_execution_time
def calculate_sum(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


calculate_sum(1000000)

def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Example usage: print first N Fibonacci numbers
num = int(input("Enter the number of Fibonacci numbers to generate: "))
fib = fibonacci_generator()
for _ in range(num):
    print(next(fib))
# Find sum of even valued terms in Fibonacci sequence less than 4M

even_fib = 2
x = 1
y = 2
while y < 4000000:
    if (x + y) % 2 == 0:
        even_fib += x + y
    temp = x
    x = y
    y = temp + y
print(even_fib)

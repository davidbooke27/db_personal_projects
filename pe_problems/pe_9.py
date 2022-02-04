# Find pythagorean triple for which a + b + c == 1000
import math


def py_trip(num):
    for a in range(1, num):
        for b in range(a + 1, num):
            max_val = math.ceil(math.sqrt(a ** 2 + b ** 2))
            for c in range(b + 1, max_val + 1):
                if (a ** 2) + (b ** 2) == c ** 2 and a + b + c == num:
                    return [a, b, c], a * b * c


def py_trip_2(num):
    for a in range(1, num):
        for b in range(a + 1, num):
            c = math.sqrt(a**2+b**2)
            if a + b + c == num:
                return [a,b,c], a*b*c


print(py_trip_2(1000))

# Find the 10001st prime number
import math


def is_prime(num):
    if num % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True


# Returns the nth prime number (i.e. the 8th prime number if 8 is given as argument)
def nth_prime(num):
    # Start counter at 1 since 2 is prime, and we'll only be checking odd numbers
    prime_counter = 1
    curr_num = 3
    while prime_counter < num:
        if is_prime(curr_num):
            prime_counter += 1
        curr_num += 2
    return curr_num - 2


print(nth_prime(10001))

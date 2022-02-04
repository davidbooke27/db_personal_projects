# Largest palindrome made from product of two three-digit numbers

def is_palindrome(num):
    num = str(num)
    mid_idx = len(num) // 2
    first_half = num[:mid_idx]
    second_half = num[::-1][:mid_idx]
    if first_half == second_half:
        return True
    return False


def largest_pal():
    max_pal = 0
    for i in range(1, 1000):
        for j in range(i, 1000):
            if is_palindrome(i * j) and i * j > max_pal:
                max_pal = i * j
    return max_pal


print(largest_pal())

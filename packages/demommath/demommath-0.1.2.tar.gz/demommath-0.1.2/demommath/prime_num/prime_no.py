def is_prime(num):
    if num <= 1:
        return False
    elif num == 2:
        return True
    elif num % 2 == 0:
        return False
    else:
        # Check for factors up to the square root of the number
        for i in range(3, int(num**0.5) + 1, 2):
            if num % i == 0:
                return False
        return True

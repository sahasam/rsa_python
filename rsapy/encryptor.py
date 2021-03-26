"""!
@file
encryptor.py

This is where the encryption magic happens...
"""
from random import randint

def is_prime(b:int) -> bool:
    """!
    @brief helper function to verify if a number is prime.
    implements a probabalistic algorithm by Solovay and Strassen.
    The probability of a false positive is practically negligible.

    @param num number to verify primality
    @return true if b is extremely likely to be prime else false.
    """
    for _ in range(100):
        a = randint(1, b-1)
        if not (gcd(a, b) == 1 and pow(a, (b-1), b) == 1):
            return False
    return True



def gcd(a:int, b:int)->int:
    """!
    @brief implementation of binary gcd algorithm as a
    helper function.

    credit to https://radiusofcircle.blogspot.com/2016/10/binary-gcd-algorithm-implementation.html

    @param a first number
    @param b second number
    @return greatest common divisor
    """
    if a == b:
        return a
    elif a == 0:
        return b
    elif b == 0:
        return a

    # a is even
    if a & 1 == 0:
        if b & 1 == 0:
            return 2*gcd(a>>1, b>>1)
        else:
            return gcd(a>>1, b)
    # a is odd
    else:
        if b & 1 == 0:
            return gcd(a, b >> 1)
        elif a > b and b & 1 != 0:
            return gcd((a-b) >> 1, b)
        else:
            return gcd((b-a) >> 1, a)


def generate_primes():
    """!
    @brief Generate a large number N that is the product of
    two 100 digit prime numbers, e and d

    @return (N, e, d) where e and d are large prime numbers whose
            product is N
    """
    # generate a random 100 digit odd number.
    range_start = 10**(99) # 1 with 99 zeros
    range_end = 10**(100)-1 # 100 9's

    # generate a first 100 digit prime number
    finished = False
    e = 0
    while(not finished):
        e = randint(range_start, range_end)
        finished = is_prime(e)

    # generate a second prime number that is far from e
    i = 2
    d = 0
    finished = False
    while not finished:
        d = i * e + 1
        finished = is_prime(d)
        i += 2

    return (e * d, e, d)


def main():
    print("This is the end...")

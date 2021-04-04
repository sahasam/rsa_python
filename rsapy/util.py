"""!
@file
util.py

Helper functions for encryption
"""
from random import randint
import sys
import os

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
    while b:
        a, b = b , a % b
    return a


def generate_primes(size=32):
    """!
    @brief Generate a large number N that is the product of
    two 100 digit prime numbers, $$ p*q = N $$.
    @param size number of bits in prime. Defaults to 32 bytes or 256 bits.
    @return (N, p, q) where p and q are large prime numbers whose
            product is N
    """
    # generate a random 100 digit odd number.
    range_start = 10**(99) # 1 with 99 zeros
    range_end = 10**(100)-1 # 100 9's

    primes = [0, 0]
    for i in range(2):
        # generate a temporary 100 digit random prime number
        finished = False
        tmp = 0
        while(not finished):
            tmp = int.from_bytes(os.urandom(128),sys.byteorder)
            finished = is_prime(tmp)

        # find a prime number k that has tmp so that
        # k - 1 has a large prime factor
        j = 2
        finished = False
        while not finished:
            primes[i] = j * tmp + 1
            finished = is_prime(primes[i])
            j += 2

    return (primes[0] * primes[1], primes[0], primes[1])
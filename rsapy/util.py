"""!
@file
util.py

Helper functions for encryption
"""
from random import randint
import sys
import time
import math
import matplotlib.pyplot as plt
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

        if not (pow(a, (b-1), b) == 1):
            return False
    return True



def gcd(a:int, b:int)->int:
    """!
    @brief implementation of gcd algorithm

    @param a first number
    @param b second number
    @return greatest common divisor
    """
    while b:
        a, b = b , a % b
    return a


def generate_primes(size:int = 256):
    """!
    @brief Generate a large number N that is the product of
    two 100 digit prime numbers, $$ p*q = N $$.
    @param size number of bits in prime. Defaults to 256 bits.
    @return (N, p, q) where p and q are large prime numbers whose
            product is N
    """
    # generate a random 100 digit odd number.
    primes = [0, 0]
    for i in range(2):
        finished = False
        tmp = 0
        is_prime_times = []
        while(not finished):
            tmp = int.from_bytes(os.urandom(math.ceil(size/8)),sys.byteorder)
            start = time.time()
            finished = is_prime(tmp)
            is_prime_times.append(time.time() - start)

        # find a prime number k that has tmp so that
        # k - 1 has a large prime factor
        j = 2
        finished = False
        while not finished:
            primes[i] = j * tmp + 1
            finished = is_prime(primes[i])
            j += 2

    plt.hist(is_prime_times[:-1], bins=20)
    plt.savefig("output.png")
    return (primes[0] * primes[1], primes[0], primes[1])

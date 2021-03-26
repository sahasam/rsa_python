## @file
#  encryptor.py
#
#  This is where the encryption magic happens...
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
        a = randint(1, num-1)
        if not (gcd(a, b) == 1 and jacobi(a, b) == pow(a, ((b-1)/2), b)):
            return False

    return True

def jacobi(a:int, b:int) -> int:
    """!
    @brief calculate the Jacobi. Helper function in determining if a
    number is prime or not

    @param a first number
    @param b second number
    @return J(a, b)
    """
    if a == 1:
        return 1

    if a%2 == 0:
        return jacobi(a/2, b) * (-1)**((b**(2)-1)/8)
    else:
        return jacobi(b % a, a) * (-1)**((a-1)*(b-1)/4)


def gcd(a, b):
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
    elif v == 0:
        return a

    # u is even
    if a & 1 == 0:
        if b & 1 == 0:
            return 2*gcd(a>>1, b>>1)
        else:
            return gcd(a>>1, b)
    # u is odd
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

    finished = False
    num = 0

    while(!finished) {
        # generate random 100 digit number
        num = randint(range_start, range_end)
        finished = isPrime(num)
    }




def main():
    print("This is the end...")

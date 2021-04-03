# Testing file for methods in rsapy.encryptor.py

import unittest
from rsapy.encryptor import *
from rsapy.util import *

class TestEncryptor(unittest.TestCase):
    def test_gcd(self):
        """Test gcd helper function"""
        self.assertEqual(gcd(20, 4), 4)
        self.assertEqual(gcd(20, 12), 4)
        self.assertEqual(gcd(20, 15), 5)
        self.assertEqual(gcd(20, 17), 1)
        self.assertEqual(gcd(20, 20), 20)

    def test_is_prime(self):
        """Test prime checking"""
        self.assertEqual(is_prime(4), False)
        self.assertEqual(is_prime(31), True)
        self.assertEqual(is_prime(2), True)
        self.assertEqual(is_prime(100), False)
        self.assertEqual(is_prime(2074722246773485207821695222107608587480996474721117292752992589912196684750549658310084416732550077), True)
        self.assertEqual(is_prime(2074722246773485207821695222107608587480996474721117292752992589912196684750549658310084416732550072), False)

    def test_generate_primes(self):
        """Test generation of prime numbers"""
        n, e, d = generate_primes()
        self.assertEqual(e*d, n)
        self.assertEqual(is_prime(e), True)
        self.assertEqual(is_prime(d), True)

    def test_generate_keys(self):
        n, p, q, totient, e, d = generate_keys()
        self.assertEqual(p * q, n)
        self.assertEqual(d, pow(e, -1, totient))
        self.assertEqual(e, pow(d, -1, totient))
        self.assertEqual(is_prime(p), True)
        self.assertEqual(is_prime(q), True)
        self.assertEqual(gcd(d, totient), 1)
        self.assertEqual(gcd(e, totient), 1)

class TestKeys(unittest.TestCase):
    def test_RSAKeyPair(self):
        n, p, q, totient, e, d = generate_keys()

        prk = RSAPrivateKey(n, d)
        pbk = RSAPublicKey(n, e)
        rsa_kp = RSAKeyPair(prk, pbk)
        print(str(prk))
        print(str(pbk))
        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()

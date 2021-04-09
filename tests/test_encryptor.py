# Testing file for methods in rsapy.encryptor.py

import unittest
import os, sys
from rsapy.encryptor import *
from rsapy.util import *

class TestUtil(unittest.TestCase):
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
        n, e, d = generate_primes(16)
        self.assertEqual(e*d, n)
        self.assertEqual(is_prime(e), True)
        self.assertEqual(is_prime(d), True)

        n, e, d = generate_primes(128)
        self.assertEqual(e*d, n)
        self.assertEqual(is_prime(e), True)
        self.assertEqual(is_prime(d), True)

class TestEncryptor(unittest.TestCase):
    def test_generate_keys(self):
        rkp = generate_keys()

        message = 150
        encr = rkp.encrypt(message)
        decr = rkp.decrypt(encr)
        self.assertEqual(decr, message)

        rkp = generate_keys(size=64)
        message = int.from_bytes(os.urandom(60), sys.byteorder)
        encr = rkp.encrypt(message)
        decr = rkp.decrypt(encr)
        self.assertEqual(decr, message)

    def test_file_io(self):
        rkp = generate_keys(64)
        rkp.private_key.write_to_file("private.pem")
        rkp.public_key.write_to_file("public.pem")

        pubkey = RSAPublicKey.from_file("public.pem")
        self.assertEqual(rkp.public_key, pubkey)

        privkey =  RSAPrivateKey.from_file("private.pem")
        self.assertEqual(rkp.private_key, privkey)


if __name__ == "__main__":
    unittest.main()

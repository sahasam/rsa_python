# Testing file for methods in rsapy.encryptor.py

import unittest
import os, sys
from filecmp import cmp
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
        encr = rkp._encrypt(message)
        decr = rkp._decrypt(encr)
        self.assertEqual(decr, message)

        rkp = generate_keys(size=512)
        message = int.from_bytes(os.urandom(60), sys.byteorder)
        encr = rkp._encrypt(message)
        decr = rkp._decrypt(encr)
        self.assertEqual(decr, message)

    def test_file_io(self):
        rkp = generate_keys(512)
        priv_key_file = os.path.join(os.path.dirname(__file__), "private.pem")
        pub_key_file = os.path.join(os.path.dirname(__file__), "public.pem")
        rkp.private_key.write_to_file(priv_key_file)
        rkp.public_key.write_to_file(pub_key_file)

        pubkey = RSAPublicKey.from_file(pub_key_file)
        self.assertEqual(rkp.public_key, pubkey)

        privkey =  RSAPrivateKey.from_file(priv_key_file)
        self.assertEqual(rkp.private_key, privkey)

    def test_file_encryption(self):
        rkp = generate_keys(512)
        testfile = os.path.join(os.path.dirname(__file__), "testfile.txt")
        testfile_encr = os.path.join(os.path.dirname(__file__), "testfile.encr")
        outfile = os.path.join(os.path.dirname(__file__), "outfile.txt")
        rkp.encrypt_file(testfile,testfile_encr)
        rkp.decrypt_file(testfile_encr,outfile)

        self.assertEqual(cmp(testfile, outfile), True)


    def test_file_encryption_2(self):
        rkp = generate_keys(512)
        testfile = os.path.join(os.path.dirname(__file__), "test-img.png")
        testfile_encr = os.path.join(os.path.dirname(__file__), "test-img.encr")
        outfile = os.path.join(os.path.dirname(__file__), "test-img-out.png")

        self.assertRaises(OverflowError, rkp.encrypt_file, testfile, testfile_encr)
        self.assertRaises(OverflowError, rkp.decrypt_file, testfile, testfile_encr)

if __name__ == "__main__":
    unittest.main()

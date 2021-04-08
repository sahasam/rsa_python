"""!
@file
encryptor.py This is where the encryption magic happens...  """
from rsapy.util import generate_primes
import base64
import time
import asn1


class RSAPrivateKey:
    """!
    @brief Private Key encapsulation class
    """
    def __init__(self, modulus:int, exponent:int, size:int):
        self.n = modulus
        self.d = exponent
        self.size = size

    def from_file(filename:str):
        """!
        @brief read a private key to a file
        @param filename filename string of file with key
        @return RSAPrivateKey instance
        """
        f = open(filename, 'r')
        n = (int)(f.readline())
        d = (int)(f.readline())
        f.close()
        return RSAPrivateKey(modulus=n, exponent=d)

    def use(self, block:int):
        """!
        @brief use the key
        @return unscrambled message
        """
        return pow(block, self.d, self.n)

    def __str__(self):
        """!
        @brief string representation of private key.
        Can be written to a file to be used later with from_file(filename)
        @return string representation of private key
        """
        return f"{self.n}\n{self.d}\n"

    def write_to_file(self, filename:str):
        """!
        @brief write private key to file.
        @param filename name of file to write to
        """
        try:
            f = open(filename, 'wb+')
            f.write(b'-----BEGIN PRIVATE KEY-----\n')

            # write base64 encoded key
            encoder = asn1.Encoder()
            encoder.start()
            encoder.write(self.n)
            encoder.write(self.d)

            encoded = base64.b64encode(encoder.output())
            while(len(encoded) > 64):
                f.write(encoded[:64] + b'\n')
                encoded = encoded[64:]
            f.write(encoded + b'\n')
            f.write(b'-----END PRIVATE KEY-----\n')
        except OSError as e:
            print(e)
            raise
        finally:
            f.close()


class RSAPublicKey:
    """!
    @brief Public Key encapsulation class
    """
    def __init__(self, modulus:int, exponent:int, size:int):
        self.n = modulus
        self.e = exponent
        self.size = size

    def from_file(filename:str):
        """!
        @brief read a public key from a file
        @param filename filename string of file with key
        @return RSAPublicKey instance
        """
        f = open(filename, 'r')
        n = (int)(f.readline())
        e = (int)(f.readline())
        f.close()
        return RSAPublicKey(modulus=n, exponent=e)

    def use(self, block:int):
        """!
        @brief use the key
        @return scrambled message
        """
        # TODO check message size
        return pow(block, self.e, self.n)

    def __str__(self):
        """!
        @brief string representation of a public key
        Can be written to a file to be used later with from_file(filename)
        @return string representation of private key
        """
        return f"{self.n}\n{self.e}\n"

    def write_to_file(self, filename:str):
        try:
            f = open(filename, 'wb+')
            f.write(b'-----BEGIN PUBLIC KEY-----\n')

            # write base64 encoded key
            encoder = asn1.Encoder()
            encoder.start()
            encoder.write(self.n)
            encoder.write(self.e)

            encoded = base64.b64encode(encoder.output())
            while(len(encoded) > 64):
                f.write(encoded[:64] + b'\n')
                encoded = encoded[64:]
            f.write(encoded + b'\n')
            f.write(b'-----END PRIVATE KEY-----\n')
        except OSError as e:
            print(e)
            raise
        finally:
            f.close()


class RSAKeyPair:
    """!
    @brief class to encapsulate Key Pair functions.

    Can encrypt messages, decrypt messages, and create
    signatures.
    """

    def __init__(self, private:RSAPrivateKey, public:RSAPublicKey):
        """!
        @brief Create a RSAKeyPair object

        @param private RSAPrivateKey instance
        @param public RSAPublicKey instance
        @param size number of bytes per prime
        """
        assert private.size == public.size
        self.private_key = private
        self.public_key = public

    def encrypt(self, message:int) -> int:
        return self.public_key.use(message)

    def decrypt(self, message:int) -> int:
        return self.private_key.use(message)

    def get_private_key(self):
        """!
        @brief return private key prime.
        @return (d, n)
        """
        return self.private_key

    def get_public_key(self):
        """!
        @brief return public key.
        @return (e, n)
        """
        return self.public_key


def generate_keys(size:int = 32):
    """!
    @brief generate an RSAKeyPair for encryption and decyrption

    @return RSAKeyPair instance
    """
    n, p, q = generate_primes(size)
    totient = (p-1) * (q-1)
    e = 65537 #2^16 + 1
    d = pow(e, -1, totient) # mod inverse

    privateKey = RSAPrivateKey(modulus=n, exponent=d, size=size)
    publicKey = RSAPublicKey(modulus=n, exponent=e, size=size)
    return RSAKeyPair(privateKey, publicKey)


def main():
    print("Main method")

"""!
@file
encryptor.py This is where the encryption magic happens...  """
from rsapy.util import generate_primes


class RSAPrivateKey:
    """!
    @brief Private Key encapsulation class
    """
    def __init__(self, modulus:int, exponent:int):
        self.n = modulus
        self.d = exponent

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

    def use(message):
        """!
        @brief use the key
        @return unscrambled message
        """
        pass

    def __str__(self):
        """!
        @brief string representation of private key.
        Can be written to a file to be used later with from_file(filename)
        @return string representation of private key
        """
        return f"{self.n}\n{self.d}\n"


class RSAPublicKey:
    """!
    @brief Public Key encapsulation class
    """
    def __init__(self, modulus, exponent):
        self.n = modulus
        self.e = exponent

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

    def use(message):
        """!
        @brief use the key
        @return scrambled message
        """
        pass

    def __str__(self):
        """!
        @brief string representation of a public key
        Can be written to a file to be used later with from_file(filename)
        @return string representation of private key
        """
        return f"{self.n}\n{self.e}\n"

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
        """
        # TODO: check that public and private key are a proper pair
        self.private_key = private
        self.public_key = public

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


def generate_keys():
    """!
    @brief generate an RSAKeyPair for encryption and decyrption

    @return RSAKeyPair instance
    """
    n, p, q = generate_primes()
    totient = (p-1) * (q-1)
    e = 65537 #2^16 + 1
    d = pow(e, -1, totient) # mod inverse

    return (n, p, q, totient, e, d)


def main():
    print("Main method")

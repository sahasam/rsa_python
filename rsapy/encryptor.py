"""!
@file
encryptor.py This is where the encryption magic happens...  """
from rsapy.util import generate_primes
import base64
import time
import asn1

class KeyNotFoundError(Exception):
    pass

class RSAKey:
    def __init__(self, modulus:int, exponent:int):
        """!
        @brief init function to create a RSAKey
        """
        self.n = modulus
        self.e = exponent

    def __str__(self):
        """!
        @brief string representation of a public key
        Can be written to a file to be used later with from_file(filename)
        @return string representation of private key
        """
        return f"{self.n}\n{self.e}\n"

    def __eq__(self, other):
        """!
        @brief compare two keys
        Compares the modulus and exponent. If they are not the same, returns false
        @param other RSAKey to compare to
        @return whether two keys are the same
        """
        return (other.n == self.n and other.e == self.e)

    def use(self, block:int) -> int:
        """!
        @brief use the key
        @return input with cryptographic function applied.
        """
        return pow(block, self.e, self.n)

    def _get_b64_encode(self) -> bytes:
        encoder = asn1.Encoder()
        encoder.start()
        encoder.write(self.n)
        encoder.write(self.e)
        encoded = base64.b64encode(encoder.output())
        return encoded

    def write_to_file(self, filename:str):
        pass



class RSAPrivateKey (RSAKey):
    """!
    @brief Private Key encapsulation class
    """

    def from_file(filename:str):
        start_string = b'-----BEGIN PRIVATE KEY-----\n'
        end_string = b'-----END PRIVATE KEY-----\n'

        f = open(filename, 'rb')
        lines = f.readlines()
        f.close()

        try:
            start_index = lines.index(start_string)
            end_index = lines.index(end_string)
        except ValueError as e:
            raise KeyNotFoundError(f"private key not found in '{filename}'")

        encoded_str = b''
        for i in range(start_index+1, end_index):
            encoded_str += lines[i][:-1]

        b64_decoded = base64.b64decode(encoded_str)
        decoder = asn1.Decoder()
        decoder.start(b64_decoded)
        tag, n = decoder.read()
        tag, e = decoder.read()

        return RSAPrivateKey(modulus=int(n), exponent=int(e))

    def write_to_file(self, filename:str):
        """!
        @brief write private key to file.
        @param filename name of file to write to
        """
        try:
            f = open(filename, 'wb+')
            f.write(b'-----BEGIN PRIVATE KEY-----\n')

            # write base64 encoded key
            encoded = self._get_b64_encode()
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



class RSAPublicKey(RSAKey):
    """!
    @brief Public Key encapsulation class
    """
    def from_file(filename:str):
        """!
        @brief read a public key from a file
        @param filename filename string of file with key
        @return RSAPublicKey instance
        """
        start_string = b'-----BEGIN PUBLIC KEY-----\n'
        end_string = b'-----END PUBLIC KEY-----\n'

        f = open(filename, 'rb')
        lines = f.readlines()
        f.close()

        try:
            start_index = lines.index(start_string)
            end_index = lines.index(end_string)
        except ValueError as e:
            raise KeyNotFoundError(f"public key not found in '{filename}'")

        encoded_str = b''
        for i in range(start_index+1, end_index):
            encoded_str += lines[i][:-1]

        b64_decoded = base64.b64decode(encoded_str)
        decoder = asn1.Decoder()
        decoder.start(b64_decoded)
        tag, n = decoder.read()
        tag, e = decoder.read()


        f.close()
        return RSAPublicKey(modulus=int(n), exponent=int(e))

    def write_to_file(self, filename:str):
        """!
        @brief write private key to file.
        @param filename name of file to write to
        """
        try:
            f = open(filename, 'wb+')
            f.write(b'-----BEGIN PUBLIC KEY-----\n')

            # write base64 encoded key
            encoded = self._get_b64_encode()
            while(len(encoded) > 64):
                f.write(encoded[:64] + b'\n')
                encoded = encoded[64:]
            f.write(encoded + b'\n')
            f.write(b'-----END PUBLIC KEY-----\n')
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

    privateKey = RSAPrivateKey(modulus=n, exponent=d)
    publicKey = RSAPublicKey(modulus=n, exponent=e)
    return RSAKeyPair(privateKey, publicKey)


def main():
    print("Main method")

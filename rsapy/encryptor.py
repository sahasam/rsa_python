"""!
@file
encryptor.py This is where the encryption magic happens...  """
from rsapy.util import generate_primes
import sys
import math
import base64
import time
import asn1

class KeyNotFoundError(Exception):
    pass

class RSAKey:
    """
    @brief parent class for Private and Public Keys.

    Not meant to be used directly
    """
    def __init__(self, modulus:int, exponent:int):
        """!
        @brief init function to create a RSAKey
        """
        self.n = modulus
        self.e = exponent

    def __str__(self):
        """!
        @brief string representation of a public key
        can be used for testing purposes
        @return string representation of private key
        """
        return f"{self.n}\n{self.e}"

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
        """!
        @brief get base64 interpretation of key

        Encodes modulus and exponent (in that order) to ASN.1
        Takes the resulting bytes and translates them to base64

        @return bytes representing base64 string
        """
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

    def _decrypt(self, message:int) -> int:
        """!
        @brief convert a normal int to encrypted using public key

        message must be contained in less than, or the same amount, of bits
        used to represent the modulus. Otherwise, information loss will occur.

        @param message int to convert
        @return ciphertext in int form
        """
        max_block_size = math.ceil(self.n.bit_length() / 8)
        if math.ceil(message.bit_length()/8) > max_block_size:
            raise OverflowError

        return self.use(message)

    def decrypt_file(self, infilename:str, outfilename:str):
        """!
        @brief decrypt a file and save the decyrpted version to a file

        @param infilename filename of file to decrypt
        @param outfilename filename of output file
        """
        try:
            infile = open(infilename, 'rb')
            outfile = open(outfilename, 'wb+')

            file_data = infile.read()
            max_block_size = math.ceil(self.n.bit_length() / 8)

            # decrypt int
            file_data_int = int.from_bytes(file_data, sys.byteorder)
            decr_data_int = self._decrypt(file_data_int)

            # convert decrypted int -> bytes for output
            num_decr_bytes = math.ceil(decr_data_int.bit_length()/8)
            outfile.write(decr_data_int.to_bytes(num_decr_bytes, sys.byteorder))
        finally:
            infile.close()
            outfile.close()

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

    def _encrypt(self, message:int) -> int:
        """!
        @brief convert a normal int to encrypted using public key

        message must be contained in less than, or the same amount, of bits
        used to represent the modulus. Otherwise, information loss will occur.

        @param message int to convert
        @return ciphertext in int form
        """
        max_block_size = math.ceil(self.n.bit_length() / 8)
        if math.ceil(message.bit_length()/8) > max_block_size:
            raise OverflowError
        return self.use(message)

    def encrypt_file(self, infilename:str, outfilename:str):
        """!
        @brief encrypt a file and save encrypted version to a file

        @param infilename filename of file to encrypt
        @param outfilename filename of output file
        """
        try:
            infile = open(infilename, 'rb')
            outfile = open(outfilename, 'wb+')

            # read file data
            file_data = infile.read()

            max_block_size = math.ceil(self.n.bit_length() / 8)

            # encrypt file data
            file_data_int = int.from_bytes(file_data, sys.byteorder)
            encr_data_int = self._encrypt(file_data_int)
            if( math.ceil(encr_data_int.bit_length()/8)> max_block_size ):
                raise OverflowError("encrypted data is too large for key size")

            # write ciphertext to file
            num_encr_bytes = math.ceil(encr_data_int.bit_length()/8)
            outfile.write(encr_data_int.to_bytes(num_encr_bytes, sys.byteorder))
        finally:
            infile.close()
            outfile.close()


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
        assert private.n == public.n
        self.private_key = private
        self.public_key = public
        self.max_block_size = math.ceil(public.n.bit_length()/8)

    def _decrypt(self, message:int) -> int:
        return self.private_key._decrypt(message)

    def decrypt_file(self, infilename:str, outfilename:str):
        self.private_key.decrypt_file(infilename, outfilename)

    def _encrypt(self, message:int) -> int:
        return self.public_key._encrypt(message)

    def encrypt_file(self, infilename:str, outfilename:str):
        self.public_key.encrypt_file(infilename, outfilename)

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


def generate_keys(size:int = 256):
    """!
    @brief generate an RSAKeyPair for encryption and decyrption
    @param size number of bits in modulus
    @return RSAKeyPair instance
    """
    n, p, q = generate_primes(size)
    totient = (p-1) * (q-1)
    e = 65537 #2^16 + 1
    d = pow(e, -1, totient) # mod inverse

    privateKey = RSAPrivateKey(modulus=n, exponent=d)
    publicKey = RSAPublicKey(modulus=n, exponent=e)
    return RSAKeyPair(privateKey, publicKey)

"""
rsapy

A python implementation of RSA encryption.

Usage:
    crypt (--keygen | --encrypt=<efile> | --decrypt=<dfile>) [options]

Options:
    -h, --help
    -k, --keygen                    generate a key
    -d <dfile>, --decrypt=<dfile>   decrypt a file
    -e <efile>, --encrypt=<efile>   encrypt a file
    -o <ofile>, --output=<ofile>    output file [default: output.encr]
    -s <size>, --keysize=<size>     specify key size [default: 128]
    -b <pbfile>, --public <pbfile>  specify public key output location [default: public.pem]
    -p <pfile>, --private <pfile>   specify private key output location [default: private.pem]
"""

from docopt import docopt
from rsapy import __version__
from rsapy.encryptor import generate_keys, RSAPublicKey, RSAPrivateKey
import time

def main():
    args = docopt(__doc__, version=f"rsapy version {__version__}", options_first = True)
    if (args['--keygen']):
        print("generating key")
        print(f"keysize: {args['--keysize']}")
        print(f"publicfile: {args['--public']}")
        print(f"privatefile: {args['--private']}")

        start_time = time.time()
        rkp = generate_keys(size=int(args['--keysize']))
        rkp.private_key.write_to_file(args['--private'])
        rkp.public_key.write_to_file(args['--public'])
        print(f"Finished keygen in {round(time.time() - start_time, 3)}s")
    elif (args['--encrypt']):
        print("encrypting file")
        print(f"inputfile: {args['--encrypt']}")
        print(f"publicfile: {args['--public']}")
        print(f"outfile: {args['--output']}")

        start_time = time.time()
        public_key = RSAPublicKey.from_file(args['--public'])
        public_key.encrypt_file(args['--encrypt'], args['--output'])
        print(f"Finished encrypting in {round(time.time() - start_time, 3)}s")
    elif (args['--decrypt']):
        print("decrypting file")
        print(f"inputfile: {args['--decrypt']}")
        print(f"privatefile: {args['--private']}")
        print(f"outfile: {args['--output']}")

        start_time = time.time()
        private_key = RSAPrivateKey.from_file(args['--private'])
        private_key.decrypt_file(args['--decrypt'], args['--output'])

        print(f"Finished decrypting in {round(time.time() - start_time, 3)}s")





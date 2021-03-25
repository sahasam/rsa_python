"""
rsapy

A python implementation of RSA encryption.

Usage:
    rsapy <command> [<args>...]

Option:
    -h, --help
"""

from docopt import docopt
from rsapy import __version__

def main():
    args = docopt(__doc__, version=f"rsapy version {__version__}", options_first = True)

    if args["<command>"] == "encrypt" :
        from rsapy.encryptor import main
        main()

